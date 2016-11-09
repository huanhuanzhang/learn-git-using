//
// Copyright (C) 2011-15 DyND Developers
// BSD 2-Clause License, see LICENSE.txt
//

#pragma once

#include <typeinfo>

#include <dynd/array.hpp>
#include <dynd/kernels/ckernel_prefix.hpp>
#include <dynd/types/substitute_typevars.hpp>

namespace dynd {
namespace nd {

  template <typename PrefixType, typename SelfType>
  struct kernel_prefix_wrapper : PrefixType {
    constexpr size_t size() const { return sizeof(SelfType); }

    /**
     * Returns the child kernel immediately following this one.
     */
    DYND_CUDA_HOST_DEVICE ckernel_prefix *get_child(intptr_t offset)
    {
      return ckernel_prefix::get_child(kernel_builder::aligned_size(offset));
    }

    /**
     * Returns the child kernel immediately following this one.
     */
    DYND_CUDA_HOST_DEVICE ckernel_prefix *get_child()
    {
      return ckernel_prefix::get_child(reinterpret_cast<SelfType *>(this)->size());
    }

    template <size_t I>
    std::enable_if_t<I == 0, ckernel_prefix *> get_child()
    {
      return get_child();
    }

    template <size_t I>
    std::enable_if_t<(I > 0), ckernel_prefix *> get_child()
    {
      const size_t *offsets = get_offsets();
      return ckernel_prefix::get_child(offsets[I - 1]);
    }

    /**
     * Returns a pointer to the list of child offsets.
     */
    size_t *get_offsets() { return reinterpret_cast<size_t *>(this + 1); }

    /**                                                                        \
     * Initializes an instance of this ckernel in-place according to the       \
     * kernel request. This calls the constructor in-place, and initializes    \
     * the base function and destructor.                                       \
     */
    template <typename... A>
    static SelfType *init(PrefixType *rawself, kernel_request_t DYND_UNUSED(kernreq), A &&... args)
    {
      /* Call the constructor in-place. */
      SelfType *self = new (rawself) SelfType(args...);
      self->destructor = &SelfType::destruct;

      return self;
    }

    /**
     * The ckernel destructor function, which is placed in
     * the ckernel_prefix destructor.
     */
    static void destruct(ckernel_prefix *self) { reinterpret_cast<SelfType *>(self)->~SelfType(); }

    static void resolve_dst_type(char *DYND_UNUSED(static_data), char *DYND_UNUSED(data), ndt::type &dst_tp,
                                 intptr_t DYND_UNUSED(nsrc), const ndt::type *DYND_UNUSED(src_tp),
                                 intptr_t DYND_UNUSED(nkwd), const array *DYND_UNUSED(kwds),
                                 const std::map<std::string, ndt::type> &tp_vars)
    {
      dst_tp = ndt::substitute(dst_tp, tp_vars, true);
    }

    static void instantiate(char *DYND_UNUSED(static_data), char *DYND_UNUSED(data), kernel_builder *ckb,
                            const ndt::type &DYND_UNUSED(dst_tp), const char *DYND_UNUSED(dst_arrmeta),
                            intptr_t DYND_UNUSED(nsrc), const ndt::type *DYND_UNUSED(src_tp),
                            const char *const *DYND_UNUSED(src_arrmeta), kernel_request_t kernreq,
                            intptr_t DYND_UNUSED(nkwd), const array *DYND_UNUSED(kwds),
                            const std::map<std::string, ndt::type> &DYND_UNUSED(tp_vars))
    {
      ckb->emplace_back<SelfType>(kernreq);
    }
  };

  /**
   * Some common shared implementation details of a CRTP
   * (curiously recurring template pattern) base class to help
   * create kernels.
   *
   * For most ckernels, the structure is not known beyond that
   * the ckernel_prefix is at the beginning. In some, such
   * as the reduction ckernel, more is known, in which case
   * CKP may be overriden.
   */
  template <typename SelfType, size_t... N>
  struct base_kernel;

/**
 * This is a helper macro for this header file. It's the memory kernel requests
 * (kernel_request_host is the only one without CUDA enabled) to appropriate
 * function qualifiers in the variadic arguments, which tell e.g. the CUDA
 * compiler to build the functions for the GPU device.
 *
 * The classes it generates are the base classes to use for defining ckernels
 * with a single and strided kernel function.
 */
#define BASE_KERNEL(KERNREQ, ...)                                                                                      \
  template <typename SelfType>                                                                                         \
  struct base_kernel<SelfType> : kernel_prefix_wrapper<ckernel_prefix, SelfType> {                                     \
    static const kernel_request_t kernreq = kernel_request_single;                                                     \
                                                                                                                       \
    typedef kernel_prefix_wrapper<ckernel_prefix, SelfType> parent_type;                                               \
                                                                                                                       \
    /** Initializes just the ckernel_prefix function member. */                                                        \
    template <typename... A>                                                                                           \
    static SelfType *init(ckernel_prefix *rawself, kernel_request_t kernreq, A &&... args)                             \
    {                                                                                                                  \
      SelfType *self = parent_type::init(rawself, kernreq, std::forward<A>(args)...);                                  \
      switch (kernreq) {                                                                                               \
      case kernel_request_call:                                                                                        \
        self->function = reinterpret_cast<void *>(call_wrapper);                                                       \
        break;                                                                                                         \
      case kernel_request_single:                                                                                      \
        self->function = reinterpret_cast<void *>(single_wrapper);                                                     \
        break;                                                                                                         \
      case kernel_request_strided:                                                                                     \
        self->function = reinterpret_cast<void *>(strided_wrapper);                                                    \
        break;                                                                                                         \
      default:                                                                                                         \
        DYND_HOST_THROW(std::invalid_argument,                                                                         \
                        "expr ckernel init: unrecognized ckernel request " + std::to_string(kernreq));                 \
      }                                                                                                                \
                                                                                                                       \
      return self;                                                                                                     \
    }                                                                                                                  \
                                                                                                                       \
    void call(array *DYND_UNUSED(dst), array *const *DYND_UNUSED(src))                                                 \
    {                                                                                                                  \
      std::stringstream ss;                                                                                            \
      ss << "void call(array *dst, array *const *src) is not implemented in " << typeid(SelfType).name();              \
      throw std::runtime_error(ss.str());                                                                              \
    }                                                                                                                  \
                                                                                                                       \
    __VA_ARGS__ static void call_wrapper(ckernel_prefix *self, array *dst, array *const *src)                          \
    {                                                                                                                  \
      reinterpret_cast<SelfType *>(self)->call(dst, src);                                                              \
    }                                                                                                                  \
                                                                                                                       \
    __VA_ARGS__ void single(char *DYND_UNUSED(dst), char *const *DYND_UNUSED(src))                                     \
    {                                                                                                                  \
      std::stringstream ss;                                                                                            \
      ss << "void single(char *dst, char *const *src) is not implemented in " << typeid(SelfType).name();              \
      throw std::runtime_error(ss.str());                                                                              \
    }                                                                                                                  \
                                                                                                                       \
    __VA_ARGS__ static void DYND_EMIT_LLVM(single_wrapper)(ckernel_prefix * self, char *dst, char *const *src)         \
    {                                                                                                                  \
      reinterpret_cast<SelfType *>(self)->single(dst, src);                                                            \
    }                                                                                                                  \
                                                                                                                       \
    __VA_ARGS__ static void strided_wrapper(ckernel_prefix *self, char *dst, intptr_t dst_stride, char *const *src,    \
                                            const intptr_t *src_stride, size_t count)                                  \
    {                                                                                                                  \
      reinterpret_cast<SelfType *>(self)->strided(dst, dst_stride, src, src_stride, count);                            \
    }                                                                                                                  \
                                                                                                                       \
    static const volatile char *DYND_USED(ir);                                                                         \
  };                                                                                                                   \
                                                                                                                       \
  template <typename SelfType>                                                                                         \
  const volatile char *DYND_USED(base_kernel<SelfType>::ir) = NULL;                                                    \
                                                                                                                       \
  template <typename SelfType>                                                                                         \
  struct base_kernel<SelfType, 0> : base_kernel<SelfType> {                                                            \
    void call(array *dst, array *const *DYND_UNUSED(src))                                                              \
    {                                                                                                                  \
      reinterpret_cast<SelfType *>(this)->single(const_cast<char *>(dst->cdata()), nullptr);                           \
    }                                                                                                                  \
                                                                                                                       \
    __VA_ARGS__ void strided(char *dst, intptr_t dst_stride, char *const *DYND_UNUSED(src),                            \
                             const intptr_t *DYND_UNUSED(src_stride), size_t count)                                    \
    {                                                                                                                  \
      for (size_t i = 0; i != count; ++i) {                                                                            \
        reinterpret_cast<SelfType *>(this)->single(dst, NULL);                                                         \
        dst += dst_stride;                                                                                             \
      }                                                                                                                \
    }                                                                                                                  \
  };                                                                                                                   \
                                                                                                                       \
  template <typename SelfType, size_t N>                                                                               \
  struct base_kernel<SelfType, N> : base_kernel<SelfType> {                                                            \
    void call(array *dst, array *const *src)                                                                           \
    {                                                                                                                  \
      char *src_data[N];                                                                                               \
      for (size_t i = 0; i < N; ++i) {                                                                                 \
        src_data[i] = const_cast<char *>(src[i]->cdata());                                                             \
      }                                                                                                                \
      reinterpret_cast<SelfType *>(this)->single(const_cast<char *>(dst->cdata()), src_data);                          \
    }                                                                                                                  \
                                                                                                                       \
    __VA_ARGS__ void strided(char *dst, intptr_t dst_stride, char *const *src, const intptr_t *src_stride,             \
                             size_t count)                                                                             \
    {                                                                                                                  \
      char *src_copy[N];                                                                                               \
      memcpy(src_copy, src, sizeof(src_copy));                                                                         \
      for (size_t i = 0; i != count; ++i) {                                                                            \
        reinterpret_cast<SelfType *>(this)->single(dst, src_copy);                                                     \
        dst += dst_stride;                                                                                             \
        for (size_t j = 0; j < N; ++j) {                                                                               \
          src_copy[j] += src_stride[j];                                                                                \
        }                                                                                                              \
      }                                                                                                                \
    }                                                                                                                  \
  };

  BASE_KERNEL(kernel_request_host);

#undef BASE_KERNEL

} // namespace dynd::nd
} // namespace dynd

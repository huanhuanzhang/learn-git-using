//
// Copyright (C) 2011-15 DyND Developers
// BSD 2-Clause License, see LICENSE.txt
//

#pragma once

#include <dynd/kernels/base_kernel.hpp>

namespace dynd {
namespace nd {

  struct view_kernel : base_kernel<view_kernel, 1> {
    static const kernel_request_t kernreq = kernel_request_call;

    void call(array *dst, array *const *src)
    {
      const ndt::type &dst_tp = dst->get_type();
      if (!dst_tp.is_builtin()) {
        dst_tp.extended()->arrmeta_copy_construct(dst->get()->metadata(), src[0]->get()->metadata(),
                                                  intrusive_ptr<memory_block_data>(src[0]->get(), true));
      }
      dst->get()->data = src[0]->get()->data;

      dst->get()->owner = src[0]->get()->owner ? src[0]->get()->owner : intrusive_ptr<memory_block_data>(src[0]->get(), true);
    }

    static void resolve_dst_type(char *DYND_UNUSED(static_data), char *DYND_UNUSED(data), ndt::type &dst_tp,
                                 intptr_t DYND_UNUSED(nsrc), const ndt::type *src_tp, intptr_t DYND_UNUSED(nkwd),
                                 const array *DYND_UNUSED(kwds),
                                 const std::map<std::string, ndt::type> &DYND_UNUSED(tp_vars))
    {
      dst_tp = src_tp[0];
    }
  };

} // namespace dynd::nd
} // namespace dynd

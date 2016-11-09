#pragma once
// Symbol visibility macros
#if defined(_WIN32) || defined(__CYGWIN__)
#if defined(_MSC_VER)
#pragma warning( disable : 4251 )
#else
#pragma GCC diagnostic ignored "-Wattributes"
#endif
#if defined(DYND_EXPORT)
// Building the library
#define DYND_API __declspec(dllexport)
#else
// Importing the library
#if 1
#define DYND_API __declspec(dllimport)
#define DYND_USING_DLL
#else
#define DYND_API
#define DYND_USING_STATIC_LIB
#endif
#endif // defined(DYND_EXPORT)
#define DYND_INTERNAL
#else
#define DYND_API
#define DYND_INTERNAL __attribute__ ((visibility ("hidden")))
#endif // End symbol visibility macros.

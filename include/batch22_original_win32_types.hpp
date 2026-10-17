#pragma once
// Original x64 OPTIONAL Win32 API function-pointer ABI candidates ONLY.
// Not the original developer C++ and not a functional native ASIO replacement.
#include <cstddef>
#include <cstdint>
#include <type_traits>
#if defined(_WIN32)
#define B22_API __stdcall
#else
#define B22_API
#endif
namespace original_batch22 {
using Ptr=void*;using BOOL32=std::int32_t;using INT32=std::int32_t;using DWORD32=std::uint32_t;
using GetProcessWindowStation=Ptr (B22_API *)();
using GetUserObjectInformationA=BOOL32 (B22_API *)(Ptr,INT32,Ptr,DWORD32,DWORD32*);
using GetActiveWindow=Ptr (B22_API *)();
using GetLastActivePopup=Ptr (B22_API *)(Ptr);
using MessageBoxA=INT32 (B22_API *)(Ptr,const char*,const char*,DWORD32);
using InitializeCriticalSectionAndSpinCount=BOOL32 (B22_API *)(Ptr,DWORD32);
using InitializeCriticalSection=void (B22_API *)(Ptr);
static_assert(sizeof(void*)==8 && sizeof(BOOL32)==4 && sizeof(DWORD32)==4);
static_assert(std::is_pointer_v<GetProcessWindowStation> && std::is_pointer_v<MessageBoxA>);
}
#undef B22_API

#pragma once
// Faithful-ORIGIN pure arithmetic, NOT a native ASIO driver / DLL.
// ABI-compatible fixed-width Win64 candidate data fields. External callbacks
// are intentionally NEVER executed in this library or its tests.
#include <cstddef>
#include <cstdint>

namespace asio_original_runtime {
constexpr std::uint32_t msvc_cpp_exception_code = 0xE06D7363u;
constexpr std::uint32_t eh_frame_magic = 0x19930520u;

// RVA 0x10642 uses mov eax,[...], zero-extending the dword into RAX before ADD.
constexpr std::uint64_t add_zero_extended_rva(std::uint64_t base, std::uint32_t offset) noexcept {
    return base + static_cast<std::uint64_t>(offset);
}
// RVAs 0x1073C, 0x183A5, 0x183DA, 0x18EA5 use MOVSXD.
constexpr std::uint64_t add_signed_relative32(std::uint64_t base, std::int32_t relative) noexcept {
    return base + static_cast<std::uint64_t>(static_cast<std::int64_t>(relative));
}
// RVA 0x1D066 -> 0x14320 -> 0x14340 -> 0x1D06E observed RAX passthrough.
constexpr std::uint64_t pass_through_callback(std::uint64_t callback_address) noexcept {
    return callback_address;
}

struct EHExceptionCandidate {
    std::uint32_t code;
    std::uint8_t opaque04[0x14];
    std::uint32_t parameter_count;
    std::uint8_t opaque1c[0x4];
    std::uint32_t magic_version;
    std::uint8_t opaque24[0xC];
    std::uint64_t throw_info;
    std::uint64_t module_base;
};
static_assert(offsetof(EHExceptionCandidate,parameter_count)==0x18);
static_assert(offsetof(EHExceptionCandidate,magic_version)==0x20);
static_assert(offsetof(EHExceptionCandidate,throw_info)==0x30);
static_assert(offsetof(EHExceptionCandidate,module_base)==0x38);
static_assert(sizeof(EHExceptionCandidate)==0x40);

struct CRTThreadStateCandidate {
    std::uint8_t pre_d0[0xD0];
    std::uint64_t callback_d0;
    std::uint8_t gap_d8[8];
    std::uint64_t callback_e0;
    std::uint8_t gap_e8[0x130-0xE8];
    std::uint64_t image_base_130;
};
static_assert(offsetof(CRTThreadStateCandidate,callback_d0)==0xD0);
static_assert(offsetof(CRTThreadStateCandidate,callback_e0)==0xE0);
static_assert(offsetof(CRTThreadStateCandidate,image_base_130)==0x130);
static_assert(sizeof(CRTThreadStateCandidate)==0x138);
static_assert(sizeof(std::uint32_t)==4 && sizeof(std::uint64_t)==8);

constexpr bool is_cpp_throw_code(std::uint32_t code) noexcept {
    return code == msvc_cpp_exception_code;
}
constexpr bool has_eh4_metadata(std::uint32_t code, std::uint32_t count,
                               std::uint32_t magic) noexcept {
    return code==msvc_cpp_exception_code && count>=3 && magic>0x19930522u;
}
}

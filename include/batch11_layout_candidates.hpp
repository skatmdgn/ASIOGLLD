#pragma once
// Hypothetical x64 object layouts inferred from instruction offsets.
// Unknown fields remain unknown. This is NOT original source or a complete ABI.
#include <cstddef>
#include <cstdint>
namespace original_asio_research {
struct Channels {
 std::uint32_t unknown00;
 std::int32_t maximum_frames;            // +0x04
 std::int32_t sample_width;              // +0x08
 std::int32_t channel_count;             // +0x0c
 std::int32_t* cursors;                 // +0x10
 std::uint8_t** channel_data;            // +0x18
};
struct CaptureRing {
 std::int32_t frame_offset;              // +0x00
 std::int32_t advanced_blocks;           // +0x04
 std::uint32_t unknown08;                // +0x08
 std::int32_t buffer_index;              // +0x0c
 std::uint32_t unknown10;                // +0x10
 std::int32_t interleave_channels;       // +0x14
 std::int32_t frames_per_block;          // +0x18
 std::int32_t bytes_per_sample;          // +0x1c
 std::int32_t buffer_count;              // +0x20
 std::uint32_t unknown24;                // +0x24
 Channels** buffers;                     // +0x28
};
static_assert(sizeof(void*)==8);
static_assert(offsetof(Channels,cursors)==0x10);
static_assert(offsetof(Channels,channel_data)==0x18);
static_assert(sizeof(Channels)==0x20);
static_assert(offsetof(CaptureRing,interleave_channels)==0x14);
static_assert(offsetof(CaptureRing,frames_per_block)==0x18);
static_assert(offsetof(CaptureRing,buffer_count)==0x20);
static_assert(offsetof(CaptureRing,buffers)==0x28);
static_assert(sizeof(CaptureRing)==0x30);
} // namespace

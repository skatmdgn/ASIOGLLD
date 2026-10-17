#pragma once
// STATIC reverse-engineering candidate only. Not original Steinberg C++ source.
#include <cstddef>
#include <cstdint>
namespace batch13 {
struct WaveFormat40 {
 std::uint16_t formatTag,channels;
 std::uint32_t samplesPerSec,avgBytesPerSec;
 std::uint16_t blockAlign,bitsPerSample,cbSize,validBits;
 std::uint32_t channelMask;
 std::uint8_t subtype[16];
};
#pragma pack(push,1)
struct FormatSnapshot {void* next;void* unknown08;std::uint32_t rate;WaveFormat40 format;std::uint32_t unknown3c;};
struct DepthNode {void* next;void* unknown08;std::uint16_t bits;std::uint8_t unknown12[6];};
struct ChannelNode {void* next;void* unknown08;std::uint16_t channels;std::uint8_t unknown12[6];DepthNode* depths;};
struct RateNode {void* next;void* unknown08;std::uint32_t rate;std::uint32_t unknown14;ChannelNode* channels;};
#pragma pack(pop)
static_assert(sizeof(void*)==8);
static_assert(sizeof(WaveFormat40)==40);
static_assert(offsetof(FormatSnapshot,format)==0x14);
static_assert(sizeof(FormatSnapshot)==0x40);
static_assert(sizeof(DepthNode)==0x18 && offsetof(DepthNode,bits)==0x10);
static_assert(sizeof(ChannelNode)==0x20 && offsetof(ChannelNode,depths)==0x18);
static_assert(sizeof(RateNode)==0x20 && offsetof(RateNode,channels)==0x18);
}

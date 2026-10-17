#pragma once
// Candidate ORIGINAL-ASIO compatible Win64 ABI layout, NOT original Steinberg C++ source.
#include <cstddef>
#include <cstdint>
namespace asio_batch12 {
using WinLong=std::int32_t;
struct ClockSource { WinLong index,associatedChannel,associatedGroup,isCurrentSource; char name[32]; };
struct ChannelInfo { WinLong channel,isInput,isActive,channelGroup,type; char name[32]; };
struct Callbacks {void* bufferSwitch;void* sampleRateDidChange;void* asioMessage;void* bufferSwitchTimeInfo;};
static_assert(sizeof(void*)==8 && sizeof(WinLong)==4);
static_assert(offsetof(ClockSource,name)==0x10 && sizeof(ClockSource)==0x30);
static_assert(offsetof(ChannelInfo,type)==0x10 && offsetof(ChannelInfo,name)==0x14 && sizeof(ChannelInfo)==0x34);
static_assert(offsetof(Callbacks,asioMessage)==0x10 && offsetof(Callbacks,bufferSwitchTimeInfo)==0x18);
}

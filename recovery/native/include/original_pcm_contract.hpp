#pragma once
// Original *normal-input semantics* from RVAs 0x23F0, 0x24C0, 0x2900,
// 0x2B5F..0x2B88; this is not a WASAPI renderer or complete ASIO DLL.
// All safety checks here are PRECONDITION GUARDS of the standalone model;
// they are not claims that the original checked these pointers/buffer sizes.
#include <cstddef>
#include <cstdint>
namespace asio_original_pcm {
inline bool supported_width(std::size_t width) {return width==1 || width==2 || width==4;}
// Original 0x23F0: channel-packed source -> one interleaved destination lane.
inline bool scatter_one_lane(std::uint8_t* dst,std::size_t dst_bytes,
                             const std::uint8_t* src,std::size_t src_bytes,
                             std::size_t width,std::size_t channels,
                             std::size_t frames,std::size_t lane) {
 if (!supported_width(width)||!frames)return true; // original no-op on unsupported/empty
 if (!dst||!src||channels==0||lane>=channels || frames>SIZE_MAX/width/channels ||
     src_bytes<frames*width || dst_bytes<frames*width*channels)return false;
 for(std::size_t frame=0;frame<frames;++frame)
  for(std::size_t byte=0;byte<width;++byte)
   dst[(frame*channels+lane)*width+byte]=src[frame*width+byte];
 return true;
}
// Original 0x24C0: selected lane -> channel-packed output at frame offset.
inline bool gather_one_lane(std::uint8_t* dst,std::size_t dst_bytes,
                            const std::uint8_t* src,std::size_t src_bytes,
                            std::size_t width,std::size_t channels,std::size_t frames,
                            std::size_t lane,std::size_t dest_frame_offset=0) {
 if (!supported_width(width)||!frames)return true;
 if (!dst||!src||channels==0||lane>=channels||frames>SIZE_MAX/width/channels||
     dest_frame_offset>SIZE_MAX/width-frames ||
     src_bytes<frames*width*channels || dst_bytes<(dest_frame_offset+frames)*width)return false;
 for(std::size_t frame=0;frame<frames;++frame)
  for(std::size_t byte=0;byte<width;++byte)
   dst[(dest_frame_offset+frame)*width+byte]=src[(frame*channels+lane)*width+byte];
 return true;
}
// Original 0x2900 special-case 2-channel/16-bit capture, non-ring-wrapping.
inline bool capture_stereo_16(std::uint8_t* left,std::uint8_t* right,std::size_t each_size,
                              const std::uint8_t* interleaved,std::size_t len,
                              std::size_t dest_offset_frames=0){
 if (len%4!=0)return false;
 std::size_t frames=len/4;
 if (frames>SIZE_MAX/2 || dest_offset_frames>SIZE_MAX/2-frames ||
     (frames && (!left||!right||!interleaved)) || each_size<2*(frames+dest_offset_frames))return false;
 for(std::size_t i=0;i<frames;++i){
  std::size_t o=2*(dest_offset_frames+i);
  left[o]=interleaved[4*i];left[o+1]=interleaved[4*i+1];
  right[o]=interleaved[4*i+2];right[o+1]=interleaved[4*i+3];
 }
 return true;
}
struct CapturePosition {std::int32_t frame_offset,buffer_index,completed_blocks;};
// Original signed division + at most ONE conditional subtraction for offset
// and buffer index. Full invalid/corrupt/negative state NOT modeled.
inline CapturePosition advance_normal(CapturePosition p,std::int32_t consumed,
                                       std::int32_t frames_per_block,std::int32_t buffers){
 if (consumed<0||frames_per_block<=0||buffers<=0||p.frame_offset<0||p.frame_offset>=frames_per_block||
     p.buffer_index<0||p.buffer_index>=buffers)return p;
 std::int32_t q=consumed/frames_per_block,r=consumed%frames_per_block;
 std::int64_t f=static_cast<std::int64_t>(p.frame_offset)+r;
 if(f>=frames_per_block){f-=frames_per_block;++q;}
 std::int64_t idx=static_cast<std::int64_t>(p.buffer_index)+q;
 if(idx>=buffers)idx-=buffers; // NOT %buffers; matches machine conditional subtraction
 return {static_cast<std::int32_t>(f),static_cast<std::int32_t>(idx),
         static_cast<std::int32_t>(p.completed_blocks+static_cast<std::int64_t>(q))};
}
}

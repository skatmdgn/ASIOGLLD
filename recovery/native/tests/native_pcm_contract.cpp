#include "original_pcm_contract.hpp"
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
using namespace asio_original_pcm;
int main(){
 for(std::size_t width: {1u,2u,4u}){
  for(std::size_t chans: {1u,2u,3u,8u}){
   for(std::size_t lane=0;lane<chans;++lane){
    std::array<std::uint8_t,64> source{};
    for(unsigned i=0;i<64;++i)source[i]=static_cast<std::uint8_t>((i*17+lane)%256);
    std::array<std::uint8_t,512> dst{};
    dst.fill(0xee);
    assert(scatter_one_lane(dst.data(),dst.size(),source.data(),source.size(),width,chans,13,lane));
    std::array<std::uint8_t,64> back{};back.fill(0x77);
    assert(gather_one_lane(back.data(),back.size(),dst.data(),dst.size(),width,chans,13,lane));
    for(std::size_t i=0;i<13*width;++i)assert(back[i]==source[i]);
   }
  }
 }
 std::array<std::uint8_t,8> l{},r{};
 std::array<std::uint8_t,12> data={1,0,2,0,254,255,3,0,4,0,5,0};
 assert(capture_stereo_16(l.data(),r.data(),8,data.data(),12));
 assert(l[0]==1&&l[2]==254&&l[3]==255&&l[4]==4);
 assert(r[0]==2&&r[2]==3&&r[4]==5);
 assert(!capture_stereo_16(l.data(),r.data(),8,data.data(),11));
 assert(!gather_one_lane(l.data(),8,data.data(),12,4,2,4,1));
 assert(scatter_one_lane(l.data(),8,data.data(),12,3,2,1,0));
 assert(advance_normal({7,4,10},13,10,5).buffer_index==1);
 assert(advance_normal({0,1,0},100,10,5).buffer_index==6);
 assert(advance_normal({7,3,0},3,10,5).completed_blocks==1);
 std::cout<<"PASS: native original-normal PCM semantics; width1/2/4; no ASIO DLL built\n";
}

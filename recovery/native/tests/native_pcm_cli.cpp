// Test-only bridge of C++ original-normal PCM implementation to synthetic Python model.
// NEVER opens/loads/initializes ASIO/Windows DLL or writes user audio.
#include "original_pcm_contract.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <cstdlib>
#include <cstdint>
using namespace asio_original_pcm;
static std::vector<std::uint8_t> parse(const std::string& x){
 std::vector<std::uint8_t> z;
 if(x.size()%2)return {};
 for(size_t i=0;i<x.size();i+=2)z.push_back(static_cast<std::uint8_t>(std::stoul(x.substr(i,2),nullptr,16)));
 return z;
}
static void printhex(const std::vector<std::uint8_t>& z){
 const char* digits="0123456789abcdef";
 for(std::uint8_t v:z)std::cout<<digits[v>>4]<<digits[v&0xf];
 std::cout<<'\n';
}
int main(int argc,char** argv){
 if(argc!=9)return 2;
 std::string mode(argv[1]);size_t width=std::stoul(argv[2]),channels=std::stoul(argv[3]),
 frames=std::stoul(argv[4]),lane=std::stoul(argv[5]),offset=std::stoul(argv[6]);
 auto src=parse(argv[7]),dst=parse(argv[8]);
 bool good=false;
 if(mode=="scatter")good=scatter_one_lane(dst.data(),dst.size(),src.data(),src.size(),width,channels,frames,lane);
 else if(mode=="gather")good=gather_one_lane(dst.data(),dst.size(),src.data(),src.size(),width,channels,frames,lane,offset);
 else return 3;
 if(!good)return 1;
 printhex(dst);return 0;
}

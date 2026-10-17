#include "original_runtime_callback_contract.hpp"
#include <cassert>
#include <cstdint>
#include <limits>
#include <iostream>
using namespace asio_original_runtime;
static_assert(add_zero_extended_rva(0x180000000ull, 0x300)==0x180000300ull);
static_assert(add_signed_relative32(0x180000000ull,-0x200)==0x17ffffe00ull);
static_assert(pass_through_callback(0x1122334455667788ull)==0x1122334455667788ull);
static_assert(is_cpp_throw_code(msvc_cpp_exception_code));
int main(){
  assert(add_zero_extended_rva(0x180000000ull,0xffffffffu)==0x27fffffffull);
  assert(add_signed_relative32(0x180000000ull,-1)==0x17fffffffull);
  assert(add_signed_relative32(0x180000000ull,0x7fffffff)==0x1ffffffffull);
  assert(add_signed_relative32(0x180000000ull,std::numeric_limits<std::int32_t>::min())==0x100000000ull);
  assert(add_zero_extended_rva(0ull,0u)==0ull);
  assert(pass_through_callback(0ull)==0ull);
  assert(is_cpp_throw_code(0xe06d7363u) && !is_cpp_throw_code(0xe06d7362u));
  assert(has_eh4_metadata(0xe06d7363u,3u,0x19930523u));
  assert(!has_eh4_metadata(0xe06d7363u,2u,0x19930523u));
  assert(!has_eh4_metadata(0xe06d7363u,3u,0x19930522u));
  assert(!has_eh4_metadata(0u,3u,0x19930523u));
  CRTThreadStateCandidate s{};
  s.callback_d0=0xdeadbeefull;s.callback_e0=0x1234ull;s.image_base_130=0x180000000ull;
  assert(s.callback_d0==0xdeadbeefull && s.callback_e0==0x1234ull);
  assert(add_signed_relative32(s.image_base_130,-24)==0x17fffffe8ull);
  std::cout << "PASS: 14 original arithmetic/guard model assertions, no callbacks executed\n";
}

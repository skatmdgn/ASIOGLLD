#!/usr/bin/env python3
"""SHA-pinned original Win64 runtime-pointer proof; readonly, stdlib, no driver loading."""
import hashlib,struct,sys
from pathlib import Path
SHA="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd"
NAMES={0x1eba8:b'EncodePointer\x00',0x1ebb8:b'KERNEL32.DLL\x00',
 0x1ebc8:b'DecodePointer\x00',0x1ece0:b'CorExitProcess\x00',0x1ecf0:b'mscoree.dll\x00'}
CODE_POINTERS={0x20d38:0x174b0,0x20d50:0x17ac0}
def check(path):
 b=Path(path).read_bytes()
 if len(b)!=173056 or hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Not exact original')
 pe=struct.unpack_from('<I',b,0x3c)[0];coff=pe+4;opt=pe+24
 if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\x00\x00' or struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('Win64 PE required')
 base=struct.unpack_from('<Q',b,opt+24)[0];sects=[]
 sh=opt+struct.unpack_from('<H',b,coff+16)[0]
 for j in range(struct.unpack_from('<H',b,coff+2)[0]):
  o=sh+j*40;_,a,n,offset=struct.unpack_from('<IIII',b,o+8);sects.append((a,n,offset))
 def read(a,n):
  for start,size,off in sects:
   if start<=a and a+n<=start+size:return b[off+a-start:off+a-start+n]
  raise ValueError('Unmapped RVA '+hex(a))
 for a,value in NAMES.items():
  if read(a,len(value))!=value:raise AssertionError('API/CLR string '+hex(a))
 for a,dest in CODE_POINTERS.items():
  if struct.unpack('<Q',read(a,8))[0]!=base+dest:raise AssertionError('Static pointer '+hex(a))
 for call,slot in [(0xf678,0x20d38),(0x1068c,0x20d50)]:
  opcode=read(call,6)
  if opcode[:2]!=b'\xff\x15' or call+6+struct.unpack('<i',opcode[2:])[0]!=slot:
   raise AssertionError('RIP relative call '+hex(call))
 print('PASS original SHA, 5 original API/CLR names, 2 exact static runtime CALL targets')
 print('STATIC ONLY, NO original-vs-replica Windows parity.')
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python batch21_runtime_spotcheck.py ORIGINAL.dll')
 check(sys.argv[1])

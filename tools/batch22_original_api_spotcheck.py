#!/usr/bin/env python3
"""Portable read-only ORIGINAL Win64 PE SHA/optional-API name spotcheck, stdlib.
Full indirect-call dataflow audit is in the separate Batch22 companion ZIP.
"""
import hashlib,struct,sys
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
API={
 0x10FB2:('GetProcessWindowStation',0x1ED00,0x10F4D,0xFF),
 0x10FD5:('GetUserObjectInformationA',0x1ED18,0x10F29,0x41),
 0x1102E:('GetActiveWindow',0x1ED50,0x10EB5,0xFF),
 0x11051:('GetLastActivePopup',0x1ED38,0x10ED4,0xFF),
 0x1107B:('MessageBoxA',0x1ED60,0x10E94,0xFF),
 0x13CA4:('InitializeCriticalSectionAndSpinCount',0x1F780,0x13C68,0xFF),
}
def verify(path):
 b=Path(path).read_bytes()
 if len(b)!=173056 or hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Not the exact original Win64 DLL')
 pe=struct.unpack_from('<I',b,0x3c)[0];coff=pe+4;opt=coff+20
 if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\x00\x00' or struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('Expected Win64 PE')
 sh=opt+struct.unpack_from('<H',b,coff+16)[0];sections=[]
 for i in range(struct.unpack_from('<H',b,coff+2)[0]):
  p=sh+40*i;_,r,n,o=struct.unpack_from('<IIII',b,p+8);sections.append((r,n,o))
 def read(r,n):
  for a,size,off in sections:
   if a<=r and r+n<=a+size:return b[off+r-a:off+r-a+n]
  raise ValueError('Unmapped RVA '+hex(r))
 for call,(name,literal,site,prefix) in API.items():
  if read(literal,len(name)+1)!=(name+'\0').encode():raise AssertionError('API name mismatch')
  if read(call,1)!=bytes([prefix]):raise AssertionError('Indirect CALL prefix mismatch')
  op=read(site,7)
  if op[:3]!=b'\x48\x8d\x15' or site+7+struct.unpack('<i',op[3:])[0]!=literal:
   raise AssertionError('Original RIP string-address LEA mismatch at '+hex(site))
 print('PASS exact original SHA, 6 API names + 6 RIP-relative references + 6 indirect calls')
 print('STATIC ONLY: not Windows execution, Ghidra full decompile or runtime parity')
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python batch22_original_api_spotcheck.py ORIGINAL.dll')
 verify(sys.argv[1])

#!/usr/bin/env python3
"""Original x64 SHA-pinned compact COM ABI/import checker. No DLL loading.
Detailed 188 opcode/operand site verifier is in the privately shared Batch18 ZIP.
"""
import hashlib,struct,sys
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
VTS={0x208c8:(0x5ec0,0x5e80,0x5e90,0x5f70,0x5fa0,0x5fa0,0x5fa0,0x5fa0),
     0x209a8:(0x5ec0,0x5e80,0x8ef0,0x8f20,0x8f20,0x8f20,0x8f20,0x5fa0)}
def inspect(path):
 b=Path(path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Original SHA mismatch')
 pe=struct.unpack_from('<I',b,0x3c)[0];coff=pe+4;opt=pe+24
 if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\x00\x00' or struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('Expected x64 PE')
 base=struct.unpack_from('<Q',b,opt+24)[0]
 sh=opt+struct.unpack_from('<H',b,coff+16)[0];sections=[]
 for i in range(struct.unpack_from('<H',b,coff+2)[0]):
  q=sh+40*i;_,va,size,offset=struct.unpack_from('<IIII',b,q+8);sections.append((va,size,offset))
 def read(r,n):
  for va,size,off in sections:
   if va<=r and r+n<=va+size:return b[off+r-va:off+r-va+n]
  raise ValueError('Unmapped RVA '+hex(r))
 for r,vt in VTS.items():
  for i,expect in enumerate(vt):
   if struct.unpack('<Q',read(r+8*i,8))[0]-base!=expect:raise AssertionError('Notification vtable '+hex(r)+':'+str(i))
 imp_rva=struct.unpack_from('<I',b,opt+112+8)[0];imports={}
 for i in range(256):
  oft,_,_,name,iat=struct.unpack('<IIIII',read(imp_rva+20*i,20))
  if not any((oft,name,iat)):break
  for j in range(1024):
   v=struct.unpack('<Q',read((oft or iat)+8*j,8))[0]
   if not v:break
   fn=('ordinal_'+str(v&65535)) if v>>63 else read(v+2,200).split(b'\0',1)[0].decode('ascii','replace')
   imports[iat+8*j]=fn
 if 'CoUninitialize' in imports.values():raise AssertionError('Unexpected static CoUninitialize import')
 if imports.get(0x1e4d0)!='CoInitializeEx' or imports.get(0x1e4d8)!='CoCreateInstance':raise AssertionError('Wrong COM IAT')
 if read(0x6803,2)!=bytes.fromhex('33d2') or read(0x6805,2)!=bytes.fromhex('33c9'):raise AssertionError('CoInitializeEx arguments changed')
 if read(0x6807,2)!=b'\xff\x15':raise AssertionError('CoInitializeEx indirect call changed')
 if 0x680d+struct.unpack('<i',read(0x6809,4))[0]!=0x1e4d0:raise AssertionError('IAT address changed')
 if read(0x680d,4)!=bytes.fromhex('488d7e10'):raise AssertionError('Expected no result branch immediately after CoInitializeEx')
 return {'SHA256':SHA,'listener_vtable_slots':16,'CoUninitialize_static_import':False,'runtime_parity':'NOT_TESTED'}
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python batch18_original_spotcheck.py ORIGINAL.dll')
 print(inspect(sys.argv[1]))

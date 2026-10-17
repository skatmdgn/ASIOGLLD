#!/usr/bin/env python3
"""Read-only ASIOGLLD original COM class-factory metadata verification."""
import hashlib,struct,uuid,sys
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
CLSID='52ebae30-47e4-483f-b87b-770314306005'
def main(p):
 b=Path(p).read_bytes()
 if hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Unexpected original DLL SHA-256')
 pe=struct.unpack_from('<I',b,0x3c)[0];coff=pe+4;opt=coff+20
 if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\0\0' or struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('Not AMD64 PE')
 sh=opt+struct.unpack_from('<H',b,coff+16)[0];regions=[]
 for j in range(struct.unpack_from('<H',b,coff+2)[0]):
  o=sh+40*j; _,rva,sz,raw=struct.unpack_from('<IIII',b,o+8);regions.append((rva,sz,raw))
 def read(r,n):
  for a,s,o in regions:
   if a<=r and r+n<=a+s:return b[o+r-a:o+r-a+n]
  raise ValueError('Unmapped RVA 0x%x'%r)
 guid=str(uuid.UUID(bytes_le=read(0x26690,16)))
 if guid!=CLSID:raise AssertionError('Unexpected CLSID '+guid)
 assert str(uuid.UUID(bytes_le=read(0x205f8,16)))=='00000000-0000-0000-c000-000000000046'
 assert str(uuid.UUID(bytes_le=read(0x1e560,16)))=='00000001-0000-0000-c000-000000000046'
 assert read(0x216c,5)==bytes.fromhex('b918000000')
 assert read(0x153a,5)==bytes.fromhex('b9d0000000')
 assert read(0x10d5,5)==bytes.fromhex('e846500000')
 assert read(0x215c,5)==bytes.fromhex('b811010480')
 assert read(0x210f,5)==bytes.fromhex('b802400080')
 assert read(0x219f,5)==bytes.fromhex('b80e000780')
 print('PASS 9/9: original COM CLSID, standard IIDs, allocations, errors, constructor call')
 print('Original CLSID:',guid)
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python verify_com_factory.py ORIGINAL_asioglld.dll')
 main(sys.argv[1])

#!/usr/bin/env python3
"""Read-only fixed-RVA evidence checker for the user-provided original DLL.
Python 3 stdlib. Static signatures only; not a decompiler or parity test.
"""
from pathlib import Path
import argparse,hashlib,struct
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
SITES={
 0x66cf:'4c8d0dda9a0100',0x66d6:'4c8d05539d0100',0x66dd:'488d156ca10100',
 0x66e9:'e8525e0000',0x66ee:'b918010000',0x6767:'48c7c101000080',
 0x6773:'ff158f780100',0x6795:'ff1575780100',0xb41c:'4c8d0dad020000',
 0xb42e:'ff15fc2f0100',0xb6ed:'83ea2b',0xb6f9:'81eae5000000',
 0xb711:'83ea01',0xb71a:'83fa03',0xb723:'ba42040000',
 0xb736:'ff15042d0100',0xb74d:'4883f80a',0xb758:'b964000000',
 0xb76b:'488d0d464d0100',0xb775:'eb05',0xb77c:'894204',
 0xb7e2:'410fb7f0',0xb7e6:'81fe44040000',0xb810:'81ee3c040000',
 0xb8bf:'830901',0xb8c4:'8321fe',0xbafd:'83c902',
 0xbb04:'83e1fd',0xb9aa:'ff15a02a0100',0xba5d:'ff15ed290100'
}
def verify(path):
 b=Path(path).read_bytes()
 sha=hashlib.sha256(b).hexdigest()
 if sha!=SHA:raise ValueError('Unexpected original SHA-256: '+sha)
 if b[:2]!=b'MZ':raise ValueError('Not MZ')
 pe=struct.unpack_from('<I',b,0x3c)[0]
 if b[pe:pe+4]!=b'PE\x00\x00':raise ValueError('Not PE')
 coff=pe+4;opt=coff+20
 if struct.unpack_from('<H',b,coff)[0]!=0x8664 or struct.unpack_from('<H',b,opt)[0]!=0x20b:
  raise ValueError('Expected x64 PE32+')
 sh=opt+struct.unpack_from('<H',b,coff+16)[0]
 sections=[]
 for i in range(struct.unpack_from('<H',b,coff+2)[0]):
  p=sh+40*i
  _,rva,size,raw=struct.unpack_from('<IIII',b,p+8)
  sections.append((rva,size,raw))
 def loc(r,n):
  for start,size,raw in sections:
   if start<=r and r+n<=start+size:return raw+r-start
  raise ValueError('Unmapped original RVA: '+hex(r))
 failures=[]
 for r,expected in SITES.items():
  wanted=bytes.fromhex(expected)
  if b[loc(r,len(wanted)):loc(r,len(wanted))+len(wanted)]!=wanted:failures.append(hex(r))
 a=struct.unpack_from('<III',b,loc(0x204b8,12))
 if a!=(10,50,100):failures.append('buffer preset table')
 print('Phase 1 original static evidence:',len(SITES)-len(failures),
       '/',len(SITES),'opcodes; preset table',a)
 if failures:raise AssertionError('Mismatch: '+str(failures))
 print('PASS. Original unchanged. This does NOT establish full or runtime parity.')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('original_dll',type=Path)
 a=p.parse_args()
 verify(a.original_dll)

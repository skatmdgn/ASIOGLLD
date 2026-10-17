#!/usr/bin/env python3
"""Read-only Batch13 original DLL format-capability audit.
Python 3 stdlib + GNU objdump. Never loads or writes the original DLL.
For ALL 116 raw opcode pins / complete CFG graph, use Batch13 companion ZIP.
"""
import argparse,hashlib,re,struct,subprocess
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
TABLES={
 0x26640:('<IIII',(44100,48000,96000,0)),
 0x204c4:('<HH',(2,0)),
 0x204c8:('<I',(3,)),
 0x204dc:('<HH',(16,0)),
}
EDGES={0x6b6e:0x7d00,0x6b84:0x7d00,0x6b97:0x7d00,0x6baa:0x7d00,
0x2e02:0x48d0,0x2e0a:0x30c0,0x6985:0x48d0,0x698d:0x30c0,
0x6ae0:0x48d0,0x6ae8:0x30c0,0x7f67:0xc400,0x8006:0xc400,
0x805c:0xc400,0x80bc:0xc400,0x2f86:0x4ea0,0x2f9a:0x4e50,
0x2faf:0x4e20,0x2fdc:0x4ea0,0x2ff0:0x4e50,0x3005:0x4e20}
INS=re.compile(r'^\s*([0-9a-f]{9,}):\s*(?:[0-9a-f]{2}\s+)+\s*([a-z][a-z0-9]*)\s*(.*)$')
def inspect(path):
 p=Path(path);b=p.read_bytes()
 if hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Original DLL SHA mismatch')
 pe=struct.unpack_from('<I',b,0x3c)[0];coff=pe+4;opt=pe+24
 if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\x00\x00' or struct.unpack_from('<H',b,coff)[0]!=0x8664:
  raise ValueError('Expected x64 PE32+')
 image=struct.unpack_from('<Q',b,opt+24)[0];sh=opt+struct.unpack_from('<H',b,coff+16)[0]
 secs=[]
 for k in range(struct.unpack_from('<H',b,coff+2)[0]):
  x=sh+40*k;_,r,sz,off=struct.unpack_from('<IIII',b,x+8);secs.append((r,sz,off))
 def read(r,n):
  for start,size,off in secs:
   if start<=r and r+n<=start+size:return b[off+r-start:off+r-start+n]
  raise ValueError('RVA unmapped '+hex(r))
 for r,(fmt,want) in TABLES.items():
  if struct.unpack(fmt,read(r,struct.calcsize(fmt)))!=want:raise AssertionError('Table '+hex(r))
 result=subprocess.run(['objdump','-d','-M','intel',str(p)],text=True,capture_output=True,check=True)
 inst={}
 for line in result.stdout.splitlines():
  m=INS.match(line)
  if m:inst[int(m[1],16)-image]=(m[2],m[3])
 for r,target in EDGES.items():
  op,operand=inst.get(r,('',''))
  if op!='call' or not re.match(r'^0x[0-9a-f]+',operand) or int(operand.split()[0],16)-image!=target:
   raise AssertionError('Direct edge '+hex(r))
 assert inst[0x7f59][0]=='call' and '[rax+0x38]' in inst[0x7f59][1]
 assert inst[0x7f5c]==('test','eax,eax') and inst[0x7f5e][0]=='jne'
 assert inst[0x7f64]==('lea','ecx,[rax+0x40]')
 for r,n in {0x8001:32,0x8057:32,0x80b7:24}.items():
  assert inst[r]==('mov','ecx,0x%x'%n)
 print('PASS original SHA, 4 original tables, 20 direct calls, IAudioClient strict S_OK and 4 node allocations')
 print('STATIC ONLY: no original Windows runtime, no replica, no parity')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('original_dll');a=ap.parse_args();inspect(a.original_dll)

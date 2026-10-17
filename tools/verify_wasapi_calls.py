#!/usr/bin/env python3
"""Read-only, byte-level COM/WASAPI callsite verifier for original ASIOGLLD.
Requires GNU objdump; does not modify/install DLL or claim runtime parity."""
import argparse, hashlib, json, re, struct, subprocess, uuid
from pathlib import Path

EXPECTED='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
# RVA, COM interface, expected method, vtable byte offset
CALLS=[
(0x38E6,'IMMDevice','Activate',0x18),
(0x390C,'IAudioClient','GetDevicePeriod',0x48),
(0x39BF,'IAudioClient','GetDevicePeriod',0x48),
(0x39D3,'IAudioClient','GetStreamLatency',0x28),
(0x3B0C,'IAudioClient','Initialize',0x18),
(0x3B28,'IAudioClient','GetStreamLatency',0x28),
(0x3B7A,'IAudioClient','GetBufferSize',0x20),
(0x3BC5,'IAudioClient','GetService',0x70),
(0x3BE2,'IAudioClient','GetService',0x70),
(0x3C00,'IAudioClient','Reset',0x60),
(0x3C2E,'IAudioClient','SetEventHandle',0x68),
(0x40D7,'IAudioRenderClient','GetBuffer',0x18),
(0x424B,'IAudioRenderClient','ReleaseBuffer',0x20),
(0x4479,'IAudioClient','GetCurrentPadding',0x30),
(0x44EA,'IAudioCaptureClient','GetNextPacketSize',0x28),
(0x4580,'IAudioCaptureClient','GetBuffer',0x18),
(0x45D5,'IAudioCaptureClient','ReleaseBuffer',0x20)]
GUIDS={
0x20608:'1cb9ad4c-dbfa-4c32-b178-c2f568a703b2',
0x20618:'f294acfc-3146-4483-a7bf-addca7c260e2',
0x20628:'c8adbd64-e71e-48a0-a4de-185c395cd317',
0x20638:'cd63314f-3fba-4a1b-812c-ef96358728e7',
0x20918:'bcde0395-e52f-467c-8e3d-c4579291692e',
0x20928:'a95664d2-9614-4f35-a746-de8db63617e6'}
def run(src):
 data=src.read_bytes();sha=hashlib.sha256(data).hexdigest()
 if sha!=EXPECTED:raise ValueError('Unexpected DLL SHA256: '+sha)
 nt=struct.unpack_from('<I',data,0x3c)[0]
 assert data[:2]==b'MZ' and data[nt:nt+4]==b'PE\x00\x00'
 coff=nt+4;op=coff+20
 assert struct.unpack_from('<H',data,coff)[0]==0x8664
 base=struct.unpack_from('<Q',data,op+24)[0]
 sh=op+struct.unpack_from('<H',data,coff+16)[0]
 sections=[]
 for i in range(struct.unpack_from('<H',data,coff+2)[0]):
  p=sh+i*40;vsz,rva,rawsz,raw=struct.unpack_from('<IIII',data,p+8)
  sections.append((rva,max(vsz,rawsz),raw))
 def offset(rva):
  for start,size,raw in sections:
   if start<=rva<start+size:return raw+rva-start
  raise ValueError('RVA outside PE sections')
 guids=[]
 for rva,expected in GUIDS.items():
  actual=str(uuid.UUID(bytes_le=data[offset(rva):offset(rva)+16]))
  guids.append({'rva':hex(rva),'expected':expected,'actual':actual,'match':expected==actual})
 result=subprocess.run(['objdump','-d','-M','intel',str(src)],text=True,capture_output=True,check=True)
 instruction={}
 pat=re.compile(r'^\s*([0-9a-f]+):\s*(?:[0-9a-f]{2}\s+)+\s*([a-z][a-z0-9]*)\s*(.*)$')
 for line in result.stdout.splitlines():
  m=pat.match(line)
  if m:instruction[int(m.group(1),16)]=(m.group(2),m.group(3))
 calls=[]
 for rva,iface,method,slot in CALLS:
  op,rest=instruction.get(base+rva,('',''))
  match=op=='call' and bool(re.search(r'\[\w+\+0x'+format(slot,'x')+r'\]',rest))
  calls.append({'rva':hex(rva),'interface':iface,'method':method,'slot':hex(slot),'match':match})
 passed=all(x['match'] for x in calls) and all(x['match'] for x in guids)
 return {'source_sha256':sha,'status':'PASS' if passed else 'FAIL',
         'verified_com_callsite_count':sum(x['match'] for x in calls),
         'verified_guid_count':sum(x['match'] for x in guids),
         'calls':calls,'guids':guids,
         'limitations':['Static callsite and GUID match only; NOT full program analysis or runtime parity']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('dll',type=Path)
 p.add_argument('--out',type=Path,default=Path('local_output/verified_wasapi.json'))
 a=p.parse_args();d=run(a.dll);a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
 print(d['status'],d['verified_com_callsite_count'],'COM calls,',d['verified_guid_count'],'GUIDs')
 if d['status']!='PASS':raise SystemExit(1)

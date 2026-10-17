#!/usr/bin/env python3
"""Original-only Phase 1 read-only audit: settings, coverage, UI resources.
Python 3 stdlib + GNU objdump. NEVER edits or loads the original DLL.
"""
import argparse,collections,hashlib,json,re,struct,subprocess
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
BASE=0x180000000
KEYS={'PollMode':0x20808,'ExclusiveMode':0x20818,
      'UserDefinedBufferSize':0x20828,'BufferDuration':0x20840,
      'SampleRate':0x201d0,'ExclusiveModeChannels':0x20450,
      'SharedModeChannels':0x20468,'ExclusiveModeBitsPerSample':0x20480,
      'SharedModeBitsPerSample':0x204a0}
CHECK={0x612d:'c741200a000000',0x6134:'c7412444ac0000',
       0x613b:'c7417001000000',0x6174:'e837050000',
       0x61a4:'488d155da60100',0x624f:'834b7002',0x6255:'836370fd',
       0x6280:'488d1591a50100',0x632b:'834b7001',0x6331:'836370fe',
       0x6354:'488d15cda40100',0x63ff:'834b7004',0x6405:'836370fb',
       0x6430:'488d1509a40100',0x64d7:'894320',
       0x6501:'488d15c89c0100',0x65ac:'894324',
       0x794a:'488d15c78e0100',0x7992:'488d158f8e0100',
       0x79cc:'488d156d8e0100',0x7a06:'488d15c3870100',
       0xb550:'488d15c1520100',0x10d5:'e846500000'}
RX=re.compile(r'^\s*([0-9a-f]{8,}):\s*(?:[0-9a-f]{2}\s+)+\s*([a-z][a-z0-9]*)\s*(.*)$')
def inspect(dll):
 b=Path(dll).read_bytes(); sha=hashlib.sha256(b).hexdigest()
 if sha!=SHA:raise ValueError('Wrong original DLL SHA256: '+sha)
 nt=struct.unpack_from('<I',b,0x3c)[0]
 if b[:2]!=b'MZ' or b[nt:nt+4]!=b'PE\0\0':raise ValueError('Not PE')
 coff=nt+4;opt=nt+24
 if struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('Not AMD64')
 sec=[];sh=opt+struct.unpack_from('<H',b,coff+16)[0]
 for i in range(struct.unpack_from('<H',b,coff+2)[0]):
  p=sh+40*i; v,rv,sz,raw=struct.unpack_from('<IIII',b,p+8)
  sec.append((b[p:p+8].rstrip(b'\0').decode(),rv,sz,raw))
 def at(r):
  for _,rv,sz,raw in sec:
   if rv<=r<rv+sz:return raw+r-rv
  raise ValueError('Unmapped RVA 0x%x'%r)
 for key,rva in KEYS.items():
  if b[at(rva):].split(b'\0')[0].decode('ascii')!=key:raise AssertionError(key)
 verified={hex(r):b[at(r):at(r)+len(bytes.fromhex(op))].hex()==op for r,op in CHECK.items()}
 rva,size=struct.unpack_from('<II',b,opt+112+3*8)
 pdata=[struct.unpack_from('<III',b,at(rva)+12*i)[:2] for i in range(size//12)]
 out=subprocess.run(['objdump','-d','-M','intel',str(dll)],capture_output=True,text=True,check=True).stdout
 inst={};branches=collections.defaultdict(list);refs=collections.defaultdict(list)
 for line in out.splitlines():
  m=RX.match(line)
  if not m:continue
  a=int(m[1],16)-BASE;op=m[2];arg=m[3];inst[a]=(op,arg)
  z=re.search(r'# 0x([0-9a-f]+)',arg)
  if z:
   trg=int(z[1],16)-BASE
   for k,v in KEYS.items():
    if v==trg:refs[k].append('0x%X'%a)
  if op!='call':continue
  z=re.match(r'(0x[0-9a-f]{8,})\b',arg)
  if z:
   target=int(z[1],16)-BASE
   if 0x1000<=target<0x1d000:branches[target].append(a)
 def in_pdata(a):return any(s<=a<e for s,e in pdata)
 unmapped=[{'rva':'0x%X'%a,'callers':len(cs)} for a,cs in sorted(branches.items()) if not in_pdata(a)]
 # Enumerate raw resources (resource tree is not the GUI behavior itself).
 res_rva,_=struct.unpack_from('<II',b,opt+112+2*8);base=at(res_rva)
 resources=[]
 def visit(rel,path):
  off=base+rel; named,numbered=struct.unpack_from('<HH',b,off+12)
  for i in range(named+numbered):
   name,loc=struct.unpack_from('<II',b,off+16+i*8)
   if name&0x80000000:
    x=base+(name&0x7fffffff);n=struct.unpack_from('<H',b,x)[0]
    label=b[x+2:x+2+n*2].decode('utf-16-le','replace')
   else:label=name
   if loc&0x80000000:visit(loc&0x7fffffff,path+[label])
   else:
    data_rva,sz,_,_=struct.unpack_from('<IIII',b,base+loc)
    resources.append({'path':path+[label],'rva':'0x%X'%data_rva,'bytes':sz})
 visit(0,[])
 return {'original_sha256':sha,'settings':{'constructor_rva':'0x6120','defaults':{'BufferDuration':10,'SampleRate':44100,'flags':1},
   'flags':{'bit0':'ExclusiveMode','bit1':'PollMode','bit2':'UserDefinedBufferSize'},
   'registry_key_xrefs':dict(refs)},
   'config_opcodes':{'passed':sum(verified.values()),'total':len(verified),'details':verified},
   'coverage':{'pdata_ranges':len(pdata),'decoded_rows':len(inst),'unique_direct_call_targets':len(branches),
    'outside_pdata':len(unmapped),'candidates':unmapped},'resources':resources,
   'limits':'Static only: no complete reconstruction, Windows runtime traces, replica or parity.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('original_dll',type=Path)
 p.add_argument('--output',type=Path,default=Path('local_output/recovery_stage4.json'))
 a=p.parse_args();r=inspect(a.original_dll)
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print('settings opcodes',r['config_opcodes']['passed'],'/',r['config_opcodes']['total'],
       'unwind',r['coverage']['pdata_ranges'],'unlisted calls',r['coverage']['outside_pdata'],
       'resource entries',len(r['resources']))
 if r['config_opcodes']['passed']!=r['config_opcodes']['total']:raise SystemExit(1)

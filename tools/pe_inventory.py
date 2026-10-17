#!/usr/bin/env python3
"""ASIOGLLD reproducible, READ-ONLY inventory.
Run: python tools/pe_inventory.py C:\path\asioglld.dll
Needs Python 3 stdlib; optional objdump for disassembly xrefs (reported separately).
Does not write to the original and includes no DLL bytes in generated JSON.
"""
import collections, datetime, hashlib, json, struct, sys
from pathlib import Path

def read_u16(b,p): return struct.unpack_from('<H',b,p)[0]
def read_u32(b,p): return struct.unpack_from('<I',b,p)[0]
def read_u64(b,p): return struct.unpack_from('<Q',b,p)[0]

def inspect(path):
    b=Path(path).read_bytes()
    if b[:2]!=b'MZ':raise ValueError('Not MZ')
    nt=read_u32(b,0x3c)
    if b[nt:nt+4]!=b'PE\x00\x00':raise ValueError('Not PE')
    coff=nt+4; opt=coff+20
    if read_u16(b,coff)!=0x8664 or read_u16(b,opt)!=0x20b:raise ValueError('Requires PE32+ x64')
    nsec=read_u16(b,coff+2); base=read_u64(b,opt+24)
    sh=opt+read_u16(b,coff+16)
    sec=[]
    for i in range(nsec):
        p=sh+i*40
        name=b[p:p+8].split(b'\0')[0].decode('ascii','replace')
        vs,vr,rawsize,raw=struct.unpack_from('<IIII',b,p+8)
        sec.append(dict(name=name,rva=vr,virtual_size=vs,raw_size=rawsize,file_offset=raw))
    def off(r):
        for s in sec:
            if s['rva']<=r<s['rva']+max(s['virtual_size'],s['raw_size']):
                pos=s['file_offset']+r-s['rva']
                return pos if pos<len(b) else None
        return None
    def string(r):
        p=off(r)
        return b[p:p+256].split(b'\0')[0].decode('ascii','replace') if p is not None else None
    dirs=opt+112
    def entry(i):return struct.unpack_from('<II',b,dirs+8*i)
    imports=[]; r,size=entry(1); p=off(r)
    if p is not None:
        for k in range(300):
            oft,ts,chain,namer,ft=struct.unpack_from('<IIIII',b,p+k*20)
            if not any((oft,ts,chain,namer,ft)):break
            t=off(oft or ft)
            if t is None:continue
            for j in range(1024):
                v=read_u64(b,t+j*8)
                if not v:break
                nm=('ordinal:'+str(v&65535)) if v>>63 else string(v+2)
                imports.append(dict(dll=string(namer),name=nm,iat_rva=ft+j*8))
    fns=[]; r,size=entry(3);p=off(r)
    if p is not None:
        for k in range(size//12):
            beg,end,u=struct.unpack_from('<III',b,p+12*k)
            if 0<beg<end: fns.append(dict(rva=beg,end_rva=end,unwind_rva=u))
    exports=[];r,size=entry(0);p=off(r)
    if p is not None:
        v=struct.unpack_from('<IIHHIIIIIII',b,p)
        ordinalbase,nfunc,nnames,funcs,names,ordinals=v[5:11]
        for j in range(nnames):
            i=read_u16(b,off(ordinals)+2*j)
            exports.append(dict(name=string(read_u32(b,off(names)+4*j)),rva=read_u32(b,off(funcs)+4*i),ordinal=ordinalbase+i))
    rtti=[]
    for s in sec:
        if s['name'] not in ('.rdata','.data'):continue
        lo=s['file_offset'];hi=lo+s['raw_size']
        for p in range(lo+8,hi-32,8):
            ptr=read_u64(b,p-8)-base
            col=off(ptr)
            if col is None or ptr<0:continue
            try:sig,offset,cdoff,td,cd,selfr=struct.unpack_from('<IIIIII',b,col)
            except struct.error:continue
            if sig!=0 or selfr!=0 or offset>256:continue
            name=string(td+16)
            if not name or not name.startswith('.?A'):continue
            x=read_u64(b,p)
            if not(0x1000<=x-base<=0x1d000):continue
            count=0
            while p+8*count+8<=hi and 0x1000<=read_u64(b,p+8*count)-base<=0x1d000:count+=1
            if count>=3:
                rv=s['rva']+(p-lo)
                rtti.append(dict(vtable_rva=rv,type_descriptor=name,object_offset=offset,entries=[hex(read_u64(b,p+i*8)-base) for i in range(count)]))
    return dict(source_sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),
        image_base=hex(base),pe_timestamp_utc=datetime.datetime.fromtimestamp(read_u32(b,coff+4),datetime.timezone.utc).isoformat(),
        sections=sec,imports=imports,exports=exports,pdata_unwind_ranges=fns,
        rtti_vtables=sorted(rtti,key=lambda x:x['vtable_rva']),
        warnings=['Unwind ranges are not all code functions.','Candidate vtables need semantic validation.','This tool does not recover C++ source or prove a performance improvement.'])

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: pe_inventory.py ORIGINAL_asioglld.dll')
    result=inspect(sys.argv[1])
    print(json.dumps(result,ensure_ascii=False,indent=2))

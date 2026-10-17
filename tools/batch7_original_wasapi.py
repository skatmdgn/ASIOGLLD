#!/usr/bin/env python3
"""Batch7 static original-WASAPI proof, NOT a replacement driver.
Python stdlib, original DLL read-only; output is static-evidence only.
"""
from pathlib import Path
import argparse,hashlib,struct,json
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
SITES={
0x3aa7:'4d69c910270000',0x3aae:'4180fd01',0x3ab9:'0f94c2',
0x3acd:'751c',0x3ade:'4c894c2420',0x3ae3:'41b800000400',
0x3af5:'4d03c9',0x3afd:'4c89742420',0x3b02:'4533c0',
0x3b0c:'ff5018',0x3b9d:'4439b380000000',0x3bad:'4c8d4338',
0x3bba:'4c8d4330',0x3bc5:'ff5070',0x3be2:'ff5070',
0x3c00:'ff5060',0x3c15:'ff150da60100',0x3c2e:'41ff5068',
0x3c4d:'ff5010',0x3c60:'ff5010',0x3c73:'ff5010',
0x434f:'ff5210',0x45e6:'ff5210',
0x46d5:'ff5020',0x46f1:'ff5018',
0x9552:'ff5010',0x9565:'ff5010',0x9578:'ff5010',
0x95a8:'ff5010',0x88b4:'ff5030',
}
def evidence(path):
    b=Path(path).read_bytes();digest=hashlib.sha256(b).hexdigest()
    if digest!=SHA:raise ValueError('Original SHA-256 does not match')
    if b[:2]!=b'MZ':raise ValueError('MZ expected')
    pe=struct.unpack_from('<I',b,0x3c)[0]
    if b[pe:pe+4]!=b'PE\x00\x00':raise ValueError('PE expected')
    coff=pe+4;opt=pe+24;sh=opt+struct.unpack_from('<H',b,coff+16)[0]
    if struct.unpack_from('<H',b,coff)[0]!=0x8664:raise ValueError('x64 expected')
    sections=[]
    for i in range(struct.unpack_from('<H',b,coff+2)[0]):
        p=sh+i*40;vs,va,sz,raw=struct.unpack_from('<IIII',b,p+8)
        sections.append((va,sz,raw))
    def raw(r,n):
        for va,sz,base in sections:
            if va<=r and r+n<=va+sz:return b[base+r-va:base+r-va+n]
        raise ValueError('RVA not mapped '+hex(r))
    failed=[hex(r) for r,w in SITES.items() if raw(r,len(w)//2).hex()!=w]
    # Check IAT names using the original PE import directory (no software execution).
    imp_rva=struct.unpack_from('<I',b,opt+112+8)[0]
    def cstr(r):return raw(r,256).split(b'\0')[0].decode('ascii','replace')
    imports={}
    for j in range(100):
        oft,_,_,dll,iat=struct.unpack('<IIIII',raw(imp_rva+j*20,20))
        if not(oft or dll or iat):break
        for k in range(1024):
            v=struct.unpack('<Q',raw((oft or iat)+k*8,8))[0]
            if not v:break
            imports[iat+8*k]=('ordinal_'+str(v&65535)) if v>>63 else cstr(v+2)
    required={0x1e228:'CreateEventA',0x1e220:'CloseHandle',0x1e4a8:'timeGetTime'}
    bad_import={hex(k):[imports.get(k),v] for k,v in required.items() if imports.get(k)!=v}
    return {'SHA256':digest,'opcode_matches':len(SITES)-len(failed),'opcode_total':len(SITES),
       'opcode_mismatches':failed,'IAT_matches':len(required)-len(bad_import),
       'IAT_total':len(required),'IAT_mismatches':bad_import,'runtime_parity':'NOT_TESTED'}
def initialize_args(duration_ms,exclusive,upstream_flag_zero):
    hns=duration_ms*10000
    if exclusive and upstream_flag_zero:
        return {'shareMode':1,'flags':0x40000,'buffer':hns,'period':hns}
    return {'shareMode':int(exclusive),'flags':0,'buffer':hns*2,'period':0}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('dll',type=Path);a=ap.parse_args()
    d=evidence(a.dll);print(json.dumps(d,indent=2))
    if d['opcode_mismatches'] or d['IAT_mismatches']:raise SystemExit(1)

#!/usr/bin/env python3
"""READ-ONLY: verify 30 original ASIOGLLD callback/thread opcode sites.
Python 3 standard library. Does not decompile, modify or install any driver.
"""
from pathlib import Path
import hashlib, struct, sys
HASH = 'e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
SITES = {
0x1750:'e86b780000',0x1852:'4869d240420f00',0x185c:'4c0fafc7',
0x1ce2:'48897c2420',0x1ce7:'e8c4750000',
0x9011:'be02000000',0x903e:'e8ddafffff',0x904e:'e8bd050000',
0x9053:'4883ee01',0x9412:'488b442460',0x9417:'48894510',
0x9454:'4c8d0525fbffff',0x946c:'ff15764d0100',
0x8f9b:'e910080000',0x988a:'488b4d18',0x9890:'ff1572480100',
0x9916:'e865aaffff',0x992a:'e8f1a6ffff',
0x9947:'443b642470',0x994c:'750b',0x9954:'e8b7fcffff',
0x9714:'e837760000',0x9729:'c7442450070000',
0x9757:'488b4310',0x9760:'8b5308',0x9768:'41b801000000',
0x976e:'ff5018',0x9771:'48830301',0x9775:'397308',0x977c:'897308',
}
def validate(path):
    binary=Path(path).read_bytes()
    digest=hashlib.sha256(binary).hexdigest()
    if digest!=HASH: raise ValueError('Unexpected original SHA256: '+digest)
    if binary[:2]!=b'MZ':raise ValueError('Not PE/MZ')
    pe=struct.unpack_from('<I',binary,0x3c)[0]
    if binary[pe:pe+4]!=b'PE\x00\x00':raise ValueError('Invalid PE')
    coff=pe+4;opt=coff+20
    if struct.unpack_from('<H',binary,coff)[0]!=0x8664 or struct.unpack_from('<H',binary,opt)[0]!=0x20b:
        raise ValueError('Not x64 PE32+')
    sh=opt+struct.unpack_from('<H',binary,coff+16)[0]
    regions=[]
    for i in range(struct.unpack_from('<H',binary,coff+2)[0]):
        x=sh+i*40;virtual,va,rawsz,raw=struct.unpack_from('<IIII',binary,x+8)
        regions.append((va,rawsz,raw))
    def file_offset(rva):
        for va,rawsz,raw in regions:
            if va<=rva<va+rawsz:return raw+rva-va
        raise ValueError('RVA not mapped: 0x%x'%rva)
    misses=[]
    for rva,opcode in SITES.items():
        want=bytes.fromhex(opcode)
        at=file_offset(rva)
        if binary[at:at+len(want)]!=want:misses.append('0x%x'%rva)
    print('Original SHA-256 verified; opcode sites: %d/%d' %
          (len(SITES)-len(misses),len(SITES)))
    if misses:raise AssertionError('Mismatches: '+', '.join(misses))
    print('STATIC MATCH ONLY. No assertion of actual runtime parity.')
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python verify_callback_bytes.py path/to/asioglld.dll')
    validate(sys.argv[1])

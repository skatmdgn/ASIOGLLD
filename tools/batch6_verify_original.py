#!/usr/bin/env python3
"""Batch 6 read-only original-ASIOGLLD ABI check. No installation, no patching.
The more extensive static CFG and callsite analyzer is in the companion Batch 6 ZIP.
"""
import argparse,hashlib,json,struct
from pathlib import Path
SHA="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd"
VTABLE_RVA=0x202F8
IASIO=[0x1050,0x1060,0x1070,0x16B0,0x1650,0x1690,0x16A0,0x1740,0x1770,
 0x1910,0x1930,0x1C50,0x1AD0,0x1AA0,0x1960,0x1BD0,0x1C00,0x17E0,
 0x1C10,0x1C90,0x1D40,0x1DC0,0x5FA0,0x5FA0]
PORT_SIGS={
0x68A6:"b9f8000000",0x68F2:"c7406044ac0000",0x691F:"c780a000000002000000",
0x6929:"c780a400000002000000",0x6933:"c780a800000010000000",
0x693D:"c780ac00000010000000",0x697B:"c7406440000000",
0x2CB0:"84d2",0x2CB4:"8b81a0000000",0x2CBB:"8b81a4000000",
0x2CD0:"84d2",0x2CD4:"8b81a8000000",0x2CDB:"8b81ac000000",
0x2CF4:"8b81a8000000",0x2CFA:"c1f803",0x2CFE:"8b81ac000000",0x2D04:"c1f803",
0x3CEA:"8b81a0000000",0x3CF2:"8b81a4000000",
0x8F89:"488b4148",0x8F8D:"8b5070",0x8F90:"d1ea",0x8F92:"f6c201",
0x8F95:"7409",0x8F9B:"e910080000",0x8FA0:"4c8d05b1790100",
0x8FA7:"488d15ba790100",0x8FB3:"ff15f7530100",
0x191A:"8b4148",0x191F:"8b414c",0x1941:"8b413c",0x1944:"03c0",
0x1964:"f2480f2cc1",0x1852:"4869d240420f00",0x18E0:"498bc0",
0x9689:"4869ff40420f00",0x9729:"c744245007000000",0x976E:"ff5018"
}
def main(path):
 b=Path(path).read_bytes()
 sha=hashlib.sha256(b).hexdigest()
 if sha!=SHA:raise ValueError("Unexpected DLL SHA256: "+sha)
 nt=struct.unpack_from("<I",b,0x3c)[0]
 if b[:2]!=b"MZ" or b[nt:nt+4]!=b"PE\x00\x00":raise ValueError("Bad PE")
 coff=nt+4; opt=nt+24
 if struct.unpack_from("<H",b,coff)[0]!=0x8664:raise ValueError("Not x64")
 image_base=struct.unpack_from("<Q",b,opt+24)[0]
 sec=[]
 sh=opt+struct.unpack_from("<H",b,coff+16)[0]
 for i in range(struct.unpack_from("<H",b,coff+2)[0]):
  p=sh+40*i;virtual,rva,size,raw=struct.unpack_from("<IIII",b,p+8)
  sec.append((rva,size,raw))
 def at(rva,size):
  for base,length,off in sec:
   if base<=rva and rva+size<=base+length:return b[off+rva-base:off+rva-base+size]
  raise ValueError("Unmapped RVA "+hex(rva))
 actual=[struct.unpack("<Q",at(VTABLE_RVA+i*8,8))[0]-image_base for i in range(24)]
 unmatched=[i for i,(got,want) in enumerate(zip(actual,IASIO)) if got!=want]
 bad_opcode=[hex(r) for r,h in PORT_SIGS.items() if at(r,len(h)//2).hex()!=h]
 rva,size=struct.unpack_from("<II",b,opt+112+3*8)
 unwind=size//12
 text=b[at(0x20968,48)] if False else at(0x20968,47)
 if not text.startswith(b"Notification Thread is currently not supported."):
  raise AssertionError("Unsupported thread message missing")
 result={"sha256":sha,"original_bytes":len(b),"unwind_entries":unwind,
  "asio_slots_matched":24-len(unmatched),"asio_slots_total":24,
  "port_worker_opcodes_matched":len(PORT_SIGS)-len(bad_opcode),
  "port_worker_opcodes_total":len(PORT_SIGS),
  "mismatched_slots":unmatched,"mismatched_opcodes":bad_opcode,
  "parity":"NOT_TESTED","optimization":"NONE"}
 print(json.dumps(result,indent=2))
 if unmatched or bad_opcode:raise SystemExit(1)
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("original_dll",type=Path)
 main(parser.parse_args().original_dll)

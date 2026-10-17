#!/usr/bin/env python3
"""Static original ASIOGLLD verifier; original DLL is never loaded or modified.
Use with original SHA-pinned 173056-byte file. Python 3 stdlib only.
RVA/opcode snapshots do NOT prove runtime target, compatibility or parity.
"""
import argparse,csv,hashlib,struct
from pathlib import Path
EXPECTED="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd"
ROOT=Path(__file__).resolve().parents[1]
def verify(path):
 data=Path(path).read_bytes()
 digest=hashlib.sha256(data).hexdigest()
 if digest!=EXPECTED:raise ValueError("Original SHA mismatch: "+digest)
 if data[:2]!=b"MZ":raise ValueError("MZ signature missing")
 pe=struct.unpack_from("<I",data,0x3c)[0]
 if data[pe:pe+4]!=b"PE\x00\x00":raise ValueError("PE signature missing")
 coff=pe+4;opt=coff+20
 if struct.unpack_from("<H",data,coff)[0]!=0x8664:raise ValueError("AMD64 image required")
 start=opt+struct.unpack_from("<H",data,coff+16)[0]
 sections=[]
 for i in range(struct.unpack_from("<H",data,coff+2)[0]):
  o=start+40*i
  virtual,rva,length,raw=struct.unpack_from("<IIII",data,o+8)
  sections.append((rva,length,raw))
 def content(rva,n):
  for base,size,offset in sections:
   if base<=rva and rva+n<=base+size:
    return data[offset+rva-base:offset+rva-base+n]
  raise ValueError("Unmapped RVA "+hex(rva))
 checks=0
 for name,expected_rows in [
  ("BATCH9_LAST59.csv",59),("BATCH9_FACTORY_PINS.csv",18)
 ]:
  with (ROOT/"analysis"/name).open(newline="",encoding="utf8") as f:rows=list(csv.DictReader(f))
  if len(rows)!=expected_rows:raise ValueError("Unexpected baseline rows in "+name)
  for row in rows:
   rva=int(row["rva"],16);opcode=bytes.fromhex(row["original_opcode_hex"])
   if content(rva,len(opcode))!=opcode:raise AssertionError("Opcode mismatch at "+hex(rva))
   checks+=1
 print(f"PASS {checks}/{checks} exact original byte signatures")
 print("Only static signatures confirmed; runtime target identities/replica parity NOT checked.")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("original_dll");a=p.parse_args()
 verify(a.original_dll)

#!/usr/bin/env python3
"""Batch11: read-only original function anchors, direct calls, FP constants.
Original SHA checks bytes; this tool does NOT establish runtime equivalence.
The companion Batch11 ZIP retains the 124 individual exact-byte opcode baseline.
"""
import hashlib,re,struct,subprocess,sys
from pathlib import Path
SHA="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd"
EDGES={0x2AF3:0x2900,0x2B40:0x2750,0x4221:0x23F0,
       0x42FA:0x24C0,0x45C2:0x2A90,0x44AC:0x4610}
ANCHORS={
  "PCM_PACKED_TO_INTERLEAVED":"23F0 2418 2443 2470 24A0",
  "PCM_INTERLEAVED_TO_PACKED":"24C0 24E0 2530 2560 2590",
  "CAPTURE_SCATTER":"2750 27AA 27DB 2820 2842 2870 2883",
  "CAPTURE_STEREO16":"2900 2980 29E2 29EE 29F3 2A05",
  "CAPTURE_RING":"2A90 2ADA 2AE2 2AF3 2B40 2B5F 2B62 2B65 2B7F",
  "PORT_CLOCK":"4610 4628 46D5 46F1 4703",
  "ASIO_SAMPLE_POSITION":"17E0 1852 185C 189C 18D0",
  "TIMEINFO_CALLBACK":"9610 9694 96D0 9707 9729 976E 977C",
}
if len(sys.argv)!=2:raise SystemExit("Usage: python tools/batch11_original_checks.py original.dll")
p=Path(sys.argv[1]);b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!=SHA:raise SystemExit("Wrong original DLL SHA")
pe=struct.unpack_from("<I",b,0x3c)[0];op=pe+24
if b[:2]!=b"MZ" or b[pe:pe+4]!=b"PE\x00\x00":raise SystemExit("Invalid PE")
base=struct.unpack_from("<Q",b,op+24)[0]
sh=op+struct.unpack_from("<H",b,pe+4+16)[0];sections=[]
for i in range(struct.unpack_from("<H",b,pe+4+2)[0]):
 q=sh+i*40;_,rva,sz,raw=struct.unpack_from("<IIII",b,q+8);sections.append((rva,sz,raw))
def rawat(r,n):
 for a,sz,o in sections:
  if a<=r and r+n<=a+sz:return b[o+r-a:o+r-a+n]
 raise ValueError("Unmapped RVA "+hex(r))
d=subprocess.run(["objdump","-d","-M","intel",str(p)],text=True,capture_output=True,check=True).stdout
rx=re.compile(r"^\s*([0-9a-f]{8,}):\s*((?:[0-9a-f]{2}\s+)+)\s*([a-z][a-z0-9]*)\s*(.*)$")
ins={}
for l in d.splitlines():
 m=rx.match(l)
 if m:ins[int(m[1],16)-base]=(bytes.fromhex(m[2]),m[3],m[4])
pins=[int(x,16) for group in ANCHORS.values() for x in group.split()]
assert len(pins)==len(set(pins))
for r in pins:
 if r not in ins:raise AssertionError("missing original instruction "+hex(r))
 v=ins[r][0]
 if rawat(r,len(v))!=v:raise AssertionError("raw opcode mismatch "+hex(r))
for caller,target in EDGES.items():
 assert ins[caller][1]=="call" and ("0x%x"%(base+target)) in ins[caller][2]
for r,expected in [(0x20A98,9.223372036854776e18),(0x20AA0,1.0),(0x20AB0,-1e9)]:
 assert struct.unpack("<d",rawat(r,8))[0]==expected
print("PASS: %d essential original instruction anchors, 6 CALLs, 3 doubles" % len(pins))
print("STATIC only. Full 124 fixed-byte pins remain in Batch11 ZIP.")

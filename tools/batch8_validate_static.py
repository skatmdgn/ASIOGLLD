#!/usr/bin/env python3
"""Original-only abbreviated check of 75 new static COM callsite proposals.
Input: local, unmodified SHA-pinned ASIOGLLD.dll. Requires GNU objdump.
This does NOT prove receiver identity at runtime or original/replica parity.
For detailed register provenance use the companion Batch8 analysis ZIP.
"""
import csv,hashlib,re,subprocess,sys
from pathlib import Path
SHA='e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd'
if len(sys.argv)!=2:raise SystemExit('Usage: python tools/batch8_validate_static.py /path/to/asioglld.dll')
binary=Path(sys.argv[1])
if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:raise SystemExit('Wrong original SHA256')
csv_file=Path(__file__).resolve().parents[1]/'analysis/BATCH8_NEW_CALLS.csv'
with csv_file.open(newline='',encoding='utf8') as f: rows=list(csv.DictReader(f))
if len(rows)!=75 or len(set(x['call_rva'] for x in rows))!=75:raise SystemExit('Invalid reference table')
o=subprocess.run(['objdump','-d','-M','intel',str(binary)],capture_output=True,text=True,check=True).stdout
rx=re.compile(r'^\s*([0-9a-f]{9,}):\s*(?:[0-9a-f]{2}\s+)+\s*([a-z][a-z0-9]*)\s*(.*)$')
ins={}
for line in o.splitlines():
    m=rx.match(line)
    if m: ins[int(m[1],16)-0x180000000]=(m[2],m[3])
issues=[]
for r in rows:
    call=int(r['call_rva'],16);ev=int(r['receiver_evidence_rva'],16);slot=int(r['vtable_slot'],16)
    op,arg=ins.get(call,('',''))
    s=re.match(r'QWORD PTR \[[a-z0-9]+(?:\+0x([0-9a-f]+))?\]$',arg)
    measured=int(s[1],16) if s and s[1] else (0 if s else None)
    if op!='call' or measured!=slot or ev>=call or ev not in ins or ins[ev][0] not in ('mov','lea'):
        issues.append(r['call_rva'])
print('SHA verified; method/slot and nearby load anchor: %d/%d' % (len(rows)-len(issues),len(rows)))
if issues:raise SystemExit('Mismatches: '+', '.join(issues))
print('STATIC EVIDENCE ONLY. Receiver type and behavior need Windows tracing.')

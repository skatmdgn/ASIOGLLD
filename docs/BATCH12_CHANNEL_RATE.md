# Batch 12: Original channel information and sample-rate algorithms

## ChannelInfo helper 0x86D0, invoked at IASIO::getChannelInfo 0x1C22

Any nonzero ChannelInfo.isInput (+4) selects input linked list config+0x48, zero selects output linked list config+0x50. For each port, select exclusive channel count port+0xA0 or shared count port+0xA4 depending on config+0x70 bit0. Sum channel counts until global channel index is within the cumulative range. Format the name with original format string "%.28ws %d" at RVA 0x20888, using port+0x90 UTF-16 friendly name or UTF-16 "Unknown" at RVA 0x20788; suffix is GLOBAL channel index+1, not per-port index.

The original first sets isActive=1 and channelGroup=0, then selects exclusive bits/sample at port+0xA8 or shared bits/sample at +0xAC. 16/24/32 bits map to ASIO sample types 0x10/0x11/0x12 respectively. Unsupported width returns false AFTER earlier writes, so wrapper returns ASE_NotPresent(-1000) with potentially partially modified structure.

## Port-specific rate validation

Both IASIO::canSampleRate 0x1AD0 and config helper 0x85D0 traverse the two port linked lists. Only ports with status+0x64 bit1 set are eligible. Status bit6 bypasses list comparison (meaning of bit6 remains unknown); other eligible ports search linked frequency entries at port+0x58 (exclusive) or +0x50 (shared), matching requested INTEGER rate against entry+0x10. Return success only when eligible count equals supported count. Empty eligible list therefore permits vacuous 0==0 success in the static algorithm; actual host reachability is NOT proven.

IASIO::canSampleRate does not update config. setSampleRate truncates input double, immediately returns success if it equals cached CAsio+0x44; otherwise 0x85D0 validates and updates config+0x24 FIRST. Failure to construct registry helper 0x66B0 then returns ASE_NoClock(-995), but config+0x24 may already be modified. If helper exists but key handle is null, RegSetValueExA is skipped, yet the success path can still call ASIOCallbacks.asioMessage(3=kAsioResetRequest). Registry and callback return values are ignored; original cached CAsio+0x44 is not directly updated in this routine.

Model limitations: normal bounded integer inputs only; Windows SSE invalid/NaN conversion, GUI side effects, real device state and exact UTF-16 formatter outcomes are NOT verified by the independent Python model. This is not a replacement driver. Full local source/evidence and tests in Batch12 ZIP.

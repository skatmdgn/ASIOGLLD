"""Bounded original clock arithmetic model, NOT original source or runtime parity."""
import math
U64=(1<<64)-1
def sample_position(block_count,frames_per_block):
 return block_count*frames_per_block & U64
def corrected_ns(start_ms,cursor,frames,samples,sample_rate):
 if sample_rate<=0:raise ValueError("positive sample rate required")
 raw=(cursor+2*frames-samples)*(1.0/sample_rate)*(-1_000_000_000.0)
 if not -(1<<63)<=raw<(1<<63):raise OverflowError("SSE extreme case unmodeled")
 return (start_ms*1_000_000+math.trunc(raw)) & U64
def clock_position_frames(rate,position,frequency):
 if frequency<=0:raise ValueError("zero frequency requires original error path")
 return ((rate*position)&U64)//frequency

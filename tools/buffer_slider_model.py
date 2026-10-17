"""STATIC pseudocode for original ASIOGLLD x64 RVA 0xB280 / 0xB310.
Not the original C++ source; not a compiled replacement or a runtime parity test.
"""
PRESETS=(10,50,100)

def duration_to_position(duration:int,custom_mode:bool)->int:
    if custom_mode:
        return min(100,max(10,duration))
    for i,v in enumerate(PRESETS):
        if duration==v:
            return i
    for i in range(1,len(PRESETS)):
        midpoint=(PRESETS[i-1]+PRESETS[i])//2
        if duration<midpoint:
            return i-1
        if duration<=PRESETS[i]:
            return i
    # Original 0xB301 XOR EAX,EAX when above all presets
    return 0

def position_to_duration(position:int,custom_mode:bool)->int:
    if custom_mode:
        return min(100,max(10,position))
    if 0<=position<=2:
        return PRESETS[position]
    return 10

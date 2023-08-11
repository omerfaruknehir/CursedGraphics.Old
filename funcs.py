def tides(tick, min_val, max_val):
    return max_val - abs((tick - min_val) % (2 * (max_val - min_val)) - (max_val - min_val))

import math

def smooth_tides(tick, min_val, max_val):
    normalized_tick = (tick - min_val) % (2 * (max_val - min_val))
    angle = (normalized_tick / (max_val - min_val)) * (2 * math.pi)
    
    sine_wave = math.sin(angle)
    smoothed_position = min_val + (sine_wave + 1) * 0.5 * (max_val - min_val)
    
    return smoothed_position
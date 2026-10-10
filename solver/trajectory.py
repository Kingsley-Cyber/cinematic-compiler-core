"""Root trajectory between consecutive key poses of one entity (derived from authored pos, never authored)."""

import math


def segment(from_key, to_key):
    displacement = [round(b - a, 6) + 0.0 for a, b in zip(from_key["pos"], to_key["pos"], strict=True)]
    distance = round(math.sqrt(sum(d * d for d in displacement)), 6)
    duration = round(to_key["t"] - from_key["t"], 6)
    speed = round(distance / duration, 6) if duration > 0 else None
    return {"displacement": displacement, "distance": distance, "duration": duration, "speed": speed}

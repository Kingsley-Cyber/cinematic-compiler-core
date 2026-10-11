"""Camera geometry for S16 (derived, never authored): aim point, camera position, axis side, frame size, screen x.

Kernel frame: +Y up; +X is the performer's left when facing +Z. Azimuth is the world heading from the aim point to
the camera (degrees from +Z toward +X); elevation lifts the camera above the aim point; roll (dutch) is ignored for
placement. Entity positions are the S06 positions at the shot's first beat (or the entity's first anchor when it is
not placed yet), so a shot is placed from where the action starts.
"""

import math

UP = (0.0, 1.0, 0.0)


def _sub(a, b):
    return [x - y for x, y in zip(a, b, strict=True)]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def _unit(v):
    length = math.sqrt(_dot(v, v))
    return [x / length for x in v]


def rounded(values):
    return [round(v, 6) + 0.0 for v in values]


def aim(target, positions, axis, height):
    if target == "midpoint":
        base = [(a + b) / 2 for a, b in zip(positions[axis[0]], positions[axis[1]], strict=True)]
    else:
        base = positions[target]
    return [base[0], base[1] + height, base[2]]


def camera_position(aim_point, distance, elevation_deg, azimuth_deg):
    el, az = math.radians(elevation_deg), math.radians(azimuth_deg)
    return [aim_point[0] + distance * math.sin(az) * math.cos(el), aim_point[1] + distance * math.sin(el),
            aim_point[2] + distance * math.cos(az) * math.cos(el)]


def side(camera, first, second, on_axis_m):
    """Side of the line first -> second the camera stands on (left = an observer at `first` facing `second`)."""
    dx, dz = second[0] - first[0], second[2] - first[2]
    length = math.hypot(dx, dz)
    if length == 0:
        return "none"
    offset = (dz * (camera[0] - first[0]) - dx * (camera[2] - first[2])) / length
    if abs(offset) < on_axis_m:
        return "on_axis"
    return "left" if offset > 0 else "right"


def fov_degrees(focal_mm, sensor_mm):
    return [round(2 * math.degrees(math.atan(size / 2 / focal_mm)), 6) for size in sensor_mm]


def frame_height(distance, focal_mm, sensor_mm):
    return round(sensor_mm[1] * distance / focal_mm, 6)


def screen_x(camera, aim_point, point, focal_mm, sensor_mm):
    """Horizontal screen position, -1 (left edge) .. +1 (right edge); None when the point is behind the camera."""
    forward = _unit(_sub(aim_point, camera))
    right = _unit(_cross(forward, UP))
    offset = _sub(point, camera)
    depth = _dot(offset, forward)
    if depth <= 0:
        return None
    return round(_dot(offset, right) / (depth * sensor_mm[0] / 2 / focal_mm), 6) + 0.0


def azimuth_change(a, b):
    return round(abs((a - b + 180) % 360 - 180), 6)


def heading_to(origin, target):
    """World heading (degrees from +Z toward +X) from one point to another, on the ground plane."""
    return math.degrees(math.atan2(target[0] - origin[0], target[2] - origin[2]))

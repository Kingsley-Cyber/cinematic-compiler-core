"""S17 renderer for live_action: the shared LBN projection with the frame parts under `frames` (no anime block)."""

from renderers.anime_renderer import _anime, project


def render(envelope, frame_parts):
    return project(envelope, frame_parts, "frames", lambda labels, cover: _anime(frame_parts, labels))

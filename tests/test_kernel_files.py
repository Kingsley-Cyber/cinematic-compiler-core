"""Kernel files load through their schemas; the kernel hash moves when any hashed kernel file changes."""

import shutil

import pytest
from conftest import ROOT

from kernel import kernel_files
from planner import modality

pytestmark = pytest.mark.unit


def test_conventions_record_the_owner_q6_decision():
    rotation = kernel_files.load("conventions")["rotation_convention"]
    assert (rotation["euler_order"], rotation["kind"], rotation["handedness"]) == ("XYZ", "intrinsic", "right")
    assert rotation["turns"] == {"flip": "X", "spin": "Y", "cartwheel": "Z"}


def test_state_vocabulary_is_closed_and_loads():
    vocabulary = kernel_files.load("state_vocabulary")
    assert set(vocabulary["actor_properties"]) == {"support", "posture", "possession", "condition", "location"}
    assert set(vocabulary["prop_properties"]) == {"holder", "location"}


def test_kernel_hash_moves_with_any_hashed_file(tmp_path):
    for name in kernel_files.HASHED:
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / name, tmp_path / name)
    assert kernel_files.kernel_hash(tmp_path) == kernel_files.kernel_hash()
    for name in kernel_files.HASHED:
        original = (tmp_path / name).read_bytes()
        (tmp_path / name).write_bytes(original + b"\n")
        assert kernel_files.kernel_hash(tmp_path) != kernel_files.kernel_hash()
        (tmp_path / name).write_bytes(original)


def test_genre_schemas_give_fps_defaults_and_duration_budgets():
    assert [modality.default_fps(g) for g in ("anime", "live_action", "ugc_ad")] == [24, 24, 30]
    assert all(modality.duration_budget(g) > 0 for g in ("anime", "live_action", "ugc_ad"))

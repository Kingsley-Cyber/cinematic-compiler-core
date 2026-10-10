"""M1 example: the courtyard fight compiles through S07 byte-for-byte against the current kernel."""

import json

import pytest
from conftest import ROOT

from compiler.examples import check_all, compile_example
from kernel.canonical import canonical_json
from kernel.kernel_files import kernel_hash

pytestmark = pytest.mark.integration
FOLDER = ROOT / "examples" / "wizard_vs_acrobat"


def test_example_recompiles_byte_for_byte_with_the_current_kernel():
    expected = (FOLDER / "envelope.json").read_text(encoding="utf-8")
    assert canonical_json(compile_example(FOLDER)) == expected
    assert json.loads(expected)["provenance"]["kernel_hash"] == kernel_hash()
    assert check_all() == []


def test_example_covers_every_built_group():
    envelope = json.loads((FOLDER / "envelope.json").read_text(encoding="utf-8"))
    for group in ("entities", "surfaces", "constraints", "beats", "states", "contacts", "kinematic", "bartenieff", "motion"):
        assert envelope["nodes"][group]["items"], group
    for group in ("constraint_application", "beat_constraint", "temporal", "causal", "state_transition", "contact",
                  "kinematic_transition", "bartenieff_transition", "motion"):
        assert envelope["edges"][group]["items"], group
    scene = envelope["scene"]
    assert (scene["duration_s"], scene["duration_source"], scene["quadrant"]["quadrant"]) == (10, "user", "B")
    assert envelope["provenance"]["authored"][0]["step_id"] == "S04"

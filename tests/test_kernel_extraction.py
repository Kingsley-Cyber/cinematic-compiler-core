"""Kernel = controls both LBN-2.3-ADV and LBN-2.4-ADV-LMA state, quoted verbatim with spans."""

import pytest
import yaml
from conftest import ROOT

from kernel import schema_log
from kernel.canonical import ContractError
from kernel_extraction import control_inventory
from kernel_extraction.control_inventory import SOURCES, build, inventory, render

pytestmark = pytest.mark.unit
KERNEL = yaml.safe_load((ROOT / "kernel" / "invariants.yaml").read_text(encoding="utf-8"))
TEXTS = [(ROOT / name).read_text(encoding="utf-8") for name in SOURCES]


@pytest.mark.integration
def test_committed_kernel_is_the_regenerated_kernel_and_every_kernel_file_is_logged():
    assert (ROOT / "kernel" / "invariants.yaml").read_text(encoding="utf-8") == render(build())
    assert set(schema_log.KERNEL.verify()) == set(schema_log.KERNEL.files())


def test_every_item_quotes_its_sources_verbatim():
    for item in KERNEL["items"]:
        if item["origin"] == "lbn_intersection":
            for row, text in zip(item["sources"], TEXTS, strict=True):
                assert text[slice(*row["span"])] == item["text"]
        else:
            row = item["sources"][0]
            assert (ROOT / row["file"]).read_text(encoding="utf-8")[slice(*row["span"])] == item["text"]


def test_kernel_is_exactly_the_intersection():
    first, second = ({(f, t) for f, t, _ in inventory(text)[1]} for text in TEXTS)
    lbn = [i for i in KERNEL["items"] if i["origin"] == "lbn_intersection"]
    assert {(i["field"], i["text"]) for i in lbn} == first & second
    owner = [i for i in KERNEL["items"] if i["origin"] == "owner"]
    assert [i["text"] for i in owner] == [row["statement"] for row in yaml.safe_load(
        (ROOT / "kernel" / "owner_invariants.yaml").read_text(encoding="utf-8"))["items"]]
    texts = {i["text"] for i in KERNEL["items"]}
    assert not {"LMA on every beat", "no energy blasts", "no generic impact effects"} & texts
    assert not any(t.startswith("AERIAL BACKFLIP KICK") for t in texts)


def test_scope_file_must_cover_every_shared_item(tmp_path, monkeypatch):
    scope = yaml.safe_load(control_inventory.SCOPE_FILE.read_text(encoding="utf-8"))
    scope["items"] = scope["items"][1:]
    path = tmp_path / "kernel_scope.yaml"
    path.write_text(yaml.safe_dump(scope), encoding="utf-8")
    monkeypatch.setattr(control_inventory, "SCOPE_FILE", path)
    with pytest.raises(ContractError) as error:
        build()
    assert error.value.code == "KERNEL_SCOPE"

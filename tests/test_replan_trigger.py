"""Replan trigger: routing to the authored step, attempts recorded in provenance, two re-authors at most."""

import copy

import pytest
from scenes import COURTYARD_PLAN, COURTYARD_QUERY

from compiler import pipeline, replan_trigger
from compiler.authoring import StepFailed
from kernel.canonical import ContractError
from planner.beat_planner import prepare

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("failed, target", [("temporal", "temporal"), ("causal", "temporal"), ("state", "temporal"),
                                            ("contact", "temporal")])
def test_failures_route_to_the_nearest_authored_step(failed, target):
    assert replan_trigger.owning_step(failed) == target


def test_no_authored_step_upstream_is_refused():
    with pytest.raises(ContractError) as error:
        replan_trigger.owning_step("constraint")
    assert error.value.code == "REPLAN_TARGET"


def test_second_attempt_is_accepted_and_recorded():
    plan = copy.deepcopy(COURTYARD_PLAN)
    plan["attempt"] = 2
    provenance = pipeline.run(COURTYARD_QUERY, until="contact", plans={"temporal": plan})["provenance"]
    assert (provenance["replan_count"], provenance["replan_layers"]) == (1, ["S04"])
    assert provenance["authored"][0]["attempt"] == 2


def test_requests_stop_after_two_reauthoring_attempts():
    before = pipeline.run(COURTYARD_QUERY, until="constraint")
    failure = StepFailed("S06", [{"code": "REPLAY_REQUIRES", "message": "x"}])
    request = replan_trigger.request(failure, failed_node="state", attempt=2, prepare=prepare, envelope_before=before)
    assert (request["step_id"], request["attempt"], request["max_attempts"]) == ("S04", 3, 3)
    with pytest.raises(ContractError) as error:
        replan_trigger.request(failure, failed_node="state", attempt=3, prepare=prepare, envelope_before=before)
    assert error.value.code == "REPLAN_EXHAUSTED"

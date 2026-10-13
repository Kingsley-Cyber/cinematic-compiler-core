"""The owner's four reference frames (2026-10-13: clash, flying_kick, takedown, multiplier), as numbers: each figure's
head, chest, hips and feet in metres, read by eye from the still (x to the right of the frame, y up, the figure in
the picture plane). CLAUDE'S INTERPRETATION of the owner's images, not measured from them; the images themselves stay
out of this public repository (copyright). Each figure carries what the frame shows, which the mechanics must read
back (tests/test_pose_mechanics.py)."""

FIGURES = {
    # clash: Naruto lunges in from the left, the rear (left) leg stretched back, the trunk forward; one long bent line
    "clash/naruto": {"points": {"head": [1.40, 1.20, 0], "torso": [1.18, 0.95, 0], "pelvis": [1.10, 0.62, 0],
                                "left_foot": [0.35, 0.12, 0], "right_foot": [1.85, 0.12, 0]},
                     "shows": {"shape": "c", "base": "left_foot", "inverted": False, "tension": (0.08, 0.20)}},
    # clash: Sasuke takes it hunched, the head bowed into the clash, the back rounded over bent knees
    "clash/sasuke": {"points": {"head": [2.10, 1.05, 0], "torso": [2.45, 1.10, 0], "pelvis": [2.70, 0.80, 0],
                                "left_foot": [2.25, 0.12, 0], "right_foot": [2.60, 0.10, 0]},
                     "shows": {"shape": "c", "inverted": False, "tension": (0.25, 0.60)}},
    # flying_kick: Sasuke upside down, hands to the ground, one long diagonal from the head to the kicking foot
    "flying_kick/sasuke": {"points": {"head": [0.40, 0.45, 0], "torso": [0.62, 0.79, 0], "pelvis": [0.92, 1.12, 0],
                                      "left_foot": [1.00, 1.35, 0], "right_foot": [2.00, 1.85, 0]},
                           "shows": {"shape": "straight", "base": "right_foot", "inverted": True}},
    # flying_kick: Naruto in the air, the head snapped back by the kick, the chest thrown forward: an arched back
    "flying_kick/naruto": {"points": {"head": [2.00, 2.05, 0], "torso": [2.22, 1.65, 0], "pelvis": [2.15, 1.20, 0],
                                      "left_foot": [2.05, 0.50, 0], "right_foot": [2.25, 0.40, 0]},
                           "shows": {"shape": "c", "inverted": False, "tension": (0.08, 0.20)}},
    # takedown: the fighter on the ground rolled onto the shoulders, the legs thrown over the head
    "takedown/thrown": {"points": {"head": [0.55, 0.15, 0], "torso": [0.70, 0.45, 0], "pelvis": [0.75, 0.85, 0],
                                   "left_foot": [0.60, 1.55, 0], "right_foot": [0.95, 1.40, 0]},
                        "shows": {"shape": "c", "inverted": True}},
    # multiplier: the flying kick across the bottom panel, the body laid out flat in the air from head to foot
    "multiplier/flying_kick": {"points": {"head": [1.00, 1.30, 0], "torso": [1.35, 1.34, 0], "pelvis": [1.75, 1.35, 0],
                                          "left_foot": [2.40, 1.10, 0], "right_foot": [2.55, 1.30, 0]},
                               "shows": {"shape": "straight", "horizontal": True}},
}

class TOPICS:
    GENERAL = "general"
    ACTIONS_AND_GAME_EFFECTS = "actions-and-game-effects"
    COMBAT = "combat"
    ATTACK_TIMING_CHART = "attack-timing-chart"
    MISSIONS = "missions"
    MOVEMENT = "movement"
    RANGE_MEASUREMENT = "range-measurement"

    as_choices = (
        (GENERAL, 'General'),
        (ACTIONS_AND_GAME_EFFECTS, 'Actions and game effects'),
        (COMBAT, 'Combat'),
        (ATTACK_TIMING_CHART, 'Timing chart for performing an attack'),
        (MISSIONS, 'Missions'),
        (MOVEMENT, 'Movement'),
        (RANGE_MEASUREMENT, 'Range measurement'),
    )

    as_list = [
        GENERAL,
        ACTIONS_AND_GAME_EFFECTS,
        COMBAT,
        ATTACK_TIMING_CHART,
        MISSIONS,
        MOVEMENT,
        RANGE_MEASUREMENT
    ]

class DAMAGE_DECK_TYPES:
    CORE = 'core'
    CORE_TFA = 'core-tfa'

    as_choices = (
        (CORE, 'Core set'),
        (CORE_TFA, 'The Force Awakens core set'),
    )

    as_list = [
        CORE, CORE_TFA
    ]


class MANEUVERS_TYPES:
  TURN_LEFT = "[Turn Left]"
  BANK_LEFT = "[Bank Left]"
  STRAIGHT = "[Straight]"
  BANK_RIGHT = "[Bank Right]"
  TURN_RIGHT = "[Turn Right]"
  KOIOGRAN_TURN = "[Koiogran Turn]"
  SEGNORS_LOOP_LEFT = "[Segnor's Loop Left]"
  SEGNORS_LOOP_RIGHT = "[Segnor's Loop Right]"
  TALLON_ROLL_RIGHT = "[Tallon Roll Right]"
  TALLON_ROLL_LEFT = "[Tallon Roll Left]"
  REVERSE_STRAIGHT = "[Reverse Straight]"
  REVERSE_BANK_LEFT = "[Reverse Bank Left]"
  REVERSE_BANK_RIGHT = "[Reverse Bank Right]"

  STATIONARY = "[Stationary]"
  IG88D_SEGNORS_LOOP_LEFT = "[IG88D Segnor's Loop Left]"
  IG88D_SEGNORS_LOOP_RIGHT = "[IG88D Segnor's Loop Right]"

  NON_EXISTANT = None

  speed_zero = [
      NON_EXISTANT,
      NON_EXISTANT,
      STATIONARY,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT,
      NON_EXISTANT
  ]

  small_and_large = [
      TURN_LEFT,
      BANK_LEFT,
      STRAIGHT,
      BANK_RIGHT,
      TURN_RIGHT,
      KOIOGRAN_TURN,
      SEGNORS_LOOP_LEFT,
      SEGNORS_LOOP_RIGHT,
      TALLON_ROLL_RIGHT,
      TALLON_ROLL_LEFT,
      REVERSE_STRAIGHT,
      REVERSE_BANK_LEFT,
      REVERSE_BANK_RIGHT
  ]

  huge = [
      TURN_LEFT,
      BANK_LEFT,
      STRAIGHT,
      BANK_RIGHT,
      TURN_RIGHT,
  ]


class MANEUVERS_DIFFICULTY:
    EASY = 2
    DIFFICULT = 3
    NORMAL = 1
    UNAVAILABLE = 0

    as_classes = {
        EASY: 'Maneuver--easy',
        DIFFICULT: 'Maneuver--difficult',
        NORMAL: 'Maneuver--normal',
    }

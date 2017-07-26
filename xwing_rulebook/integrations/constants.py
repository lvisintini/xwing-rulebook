class DAMAGE_DECK_TYPES:
    CORE = 'core'
    CORE_TFA = 'core-tfa'
    REBEL_TRANSPORT = 'rebel-transport'

    as_choices = (
        (CORE, 'Core set'),
        (CORE_TFA, 'The Force Awakens core set'),
        (REBEL_TRANSPORT, 'Rebel Transport')
    )

    as_list = [
        CORE,
        CORE_TFA,
        REBEL_TRANSPORT
    ]


class FACTIONS:
    REBEL_ALLIANCE = "Rebel Alliance"
    RESISTANCE = "Resistance"
    GALACTIC_EMPIRE = "Galactic Empire"
    FIRST_ORDER = "First Order"
    SCUM_AND_VILLAINY = "Scum and Villainy"

    rebel_factions = [
        REBEL_ALLIANCE,
        RESISTANCE
    ]

    empire_factions = [
        GALACTIC_EMPIRE,
        FIRST_ORDER
    ]

    scum_factions = [
        SCUM_AND_VILLAINY,
    ]


class MANEUVERS_DIFFICULTY:
    EASY = 2
    DIFFICULT = 3
    NORMAL = 1
    UNAVAILABLE = 0


class MANEUVERS_TYPES:
  TURN_LEFT = "[Turn Left]"
  BANK_LEFT = "[Bank Left]"
  STRAIGHT = "[Straight]"
  BANK_RIGHT = "[Bank Right]"
  TURN_RIGHT = "[Turn Right]"
  KOIOGRAN_TURN = "[Koiogran Turn]"
  SEGNORS_LOOP_LEFT = "[Segnor's Loop Left]"
  SEGNORS_LOOP_RIGHT = "[Segnor's Loop Right]"
  TALLON_ROLL_LEFT = "[Tallon Roll Left]"
  TALLON_ROLL_RIGHT = "[Tallon Roll Right]"
  REVERSE_BANK_LEFT = "[Reverse Bank Left]"
  REVERSE_STRAIGHT = "[Reverse Straight]"
  REVERSE_BANK_RIGHT = "[Reverse Bank Right]"

  STATIONARY = "[Stationary]"

  NON_EXISTENT = None

  speed_zero = [
      NON_EXISTENT,
      NON_EXISTENT,
      STATIONARY,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT,
      NON_EXISTENT
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
      TALLON_ROLL_LEFT,
      TALLON_ROLL_RIGHT,
      REVERSE_BANK_LEFT,
      REVERSE_STRAIGHT,
      REVERSE_BANK_RIGHT
  ]

  huge = [
      NON_EXISTENT,
      BANK_LEFT,
      STRAIGHT,
      BANK_RIGHT,
      NON_EXISTENT,
  ]


class SHIP_SIZES:
    SMALL = 'small'
    LARGE = 'large'
    HUGE = 'huge'

    as_list = [
        SMALL,
        LARGE,
        HUGE
    ]
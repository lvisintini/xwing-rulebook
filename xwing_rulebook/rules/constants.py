class CLAUSE_TYPES:
    TEXT = 'text'
    UNORDERED_ITEM = 'item:ul'
    ORDERED_ITEM = 'item:ol'
    HEADER = 'header'

    as_choices = (
        (TEXT, 'Text'),
        (UNORDERED_ITEM, 'Unordered Item'),
        (ORDERED_ITEM, 'Ordered Item'),
        (HEADER, 'Header')
    )

    as_list = [
        TEXT,
        UNORDERED_ITEM,
        ORDERED_ITEM,
        HEADER,
    ]

    MARKDOWN_PREFIX_TYPE_MAPPING = {
        TEXT: '',
        UNORDERED_ITEM: '- ',
        ORDERED_ITEM: '1. ',
        HEADER: '{header_level}# ',
    }


class SOURCE_TYPES:
    MANUAL = 'M'
    REFERENCE_CARD = 'RC'
    RULES_REFERENCE = 'RR'
    RULES_BOOKLET = 'RB'
    FAQ = 'FAQ'
    OTHER = 'OTHER'

    PRECEDENCE = [
        FAQ,
        RULES_REFERENCE,
        RULES_BOOKLET,
        REFERENCE_CARD,
        MANUAL,
        OTHER,
    ]

    as_choices = (
        (MANUAL, 'Manual'),
        (RULES_BOOKLET, 'Rules Booklet'),
        (REFERENCE_CARD, 'Reference Card'),
        (RULES_REFERENCE, 'Rules Reference'),
        (FAQ, 'FAQ'),
    )
    as_list = [
        MANUAL,
        REFERENCE_CARD,
        RULES_BOOKLET,
        RULES_REFERENCE,
        FAQ,
        OTHER,
    ]


class RULE_TYPES:
    RULE = 'rule'
    RULE_CLARIFICATION = 'rule-clarification'
    CARD = 'card'

    as_choices = (
        (RULE, 'Rule'),
        (RULE_CLARIFICATION, 'Rule clarification'),
        (CARD, 'Card'),
    )

    as_list = [
        RULE,
        RULE_CLARIFICATION,
        CARD,
    ]


class CLAUSE_GROUPS:
    MAIN = 1
    IMAGES = 2
    CARD_ERRATA = 3
    CARD_CLARIFICATION = 4
    HUGE_SHIP_RELATED = 5

    as_choices = (
        (MAIN, 'Main'),
        (IMAGES, 'Images'),
        (CARD_ERRATA, 'Card Errata'),
        (CARD_CLARIFICATION, 'Card Clarification'),
        (HUGE_SHIP_RELATED, 'Huge Ship Related'),
    )

    as_list = [
        MAIN,
        IMAGES,
        CARD_ERRATA,
        CARD_CLARIFICATION,
        HUGE_SHIP_RELATED,
    ]


class CARD_TYPES:
    NOT_APPLICABLE = 0
    PILOT = 1
    UPGRADE = 2
    CONDITION = 3
    DAMAGE_ORG = 4
    DAMAGE_TFA = 5

    as_choices = (
        (NOT_APPLICABLE, 'N/A'),
        (PILOT, 'Pilot'),
        (UPGRADE, 'Upgrade'),
        (CONDITION, 'Condition'),
        (DAMAGE_ORG, 'Damage card (Original core set)'),
        (DAMAGE_TFA, 'Damage card (TFA core set)'),
    )

    as_list = [
        NOT_APPLICABLE,
        DAMAGE_ORG,
        DAMAGE_TFA,
        CONDITION,
        PILOT,
        UPGRADE,
    ]

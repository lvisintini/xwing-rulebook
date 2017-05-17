class CLAUSE_TYPES:
    TEXT = 'text'
    UNORDERED_ITEM = 'item:ul'
    ORDERED_ITEM = 'item:ol'

    as_choices = (
        (TEXT, 'Text'),
        (UNORDERED_ITEM, 'Unordered Item'),
        (ORDERED_ITEM, 'Ordered Item'),
    )

    as_list = [
        TEXT,
        UNORDERED_ITEM,
        ORDERED_ITEM,
    ]

    MARKDOWN_PREFIX_TYPE_MAPPING = {
        TEXT: '',
        UNORDERED_ITEM: '- ',
        ORDERED_ITEM: '1. ',
    }


class SOURCE_TYPES:
    MANUAL = 'M'
    REFERENCE_CARD = 'RC'
    RULES_REFERENCE = 'RR'
    FAQ = 'FAQ'
    OTHER = 'OTHER'

    PRECEDENCE = [
        FAQ,
        RULES_REFERENCE,
        REFERENCE_CARD,
        MANUAL,
        OTHER,
    ]

    as_choices = (
        (MANUAL, 'Manual'),
        (REFERENCE_CARD, 'Reference Card'),
        (RULES_REFERENCE, 'Rules Reference'),
        (FAQ, 'FAQ'),
    )
    as_list = [
        MANUAL,
        REFERENCE_CARD,
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

    as_choices = (
        (MAIN, 'Main'),
        (IMAGES, 'Images'),
        (CARD_ERRATA, 'Card Errata'),
        (CARD_CLARIFICATION, 'Card Clarification'),
    )

    as_list = [
        MAIN,
        IMAGES,
        CARD_ERRATA,
        CARD_CLARIFICATION,
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

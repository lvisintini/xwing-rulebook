from . import foreign_keys, maneuvers, rename, trivial


def normalize(data):
    script = [
        rename.FieldRenamer,

        maneuvers.HugeShipManeuverNormalizer,
        maneuvers.LargeShipManeuverNormalizer,
        maneuvers.SmallShipManeuverNormalizer,

        foreign_keys.SourceShipsForeignKeyNormalization,
        foreign_keys.SourceUpgradesForeignKeyNormalization,
        foreign_keys.SourceConditionsForeignKeyNormalization,
        foreign_keys.SourcePilotsForeignKeyNormalization,

        foreign_keys.UpgradeConditionsForeignKeyNormalization,
        foreign_keys.UpgradeShipForeignKeyNormalization,
        foreign_keys.UpgradeShipsForeignKeyNormalization,

        foreign_keys.PilotConditionsForeignKeyNormalization,
        foreign_keys.PilotShipForeignKeyNormalization,

        trivial.TextToMarkdown,
        trivial.NormalizeFilePaths
    ]

    for normalizer in script:
        data = normalizer(data).run()

    return data

from .base import ForeignKeyNormalizer


class SimpleForeignKeyNormalization(ForeignKeyNormalizer):
    def get_fk_model(self, fk, current_model):
        if isinstance(fk, dict) and self.pk_name in fk:
            model = next(
                (fk_model for fk_model in self.data[self.fk_source_key] if fk_model['id'] == fk[self.pk_name])
            )
        elif isinstance(fk, str) or isinstance(fk, bytes):
            model = next((fk_model for fk_model in self.data[self.fk_source_key] if fk_model['name'] == fk))
        else:
            raise ValueError('fk {!r} is not recognized please, check!!'.format(fk))

        if model is None:
            raise ValueError('Model for fk {!r} not found'.format(fk))

        return model

    def is_fk_normalized(self, fk, current_model):
        return isinstance(fk, dict) and self.pk_name in fk and 'name' in fk

    def construct_new_fk(self, fk, current_model):
        if self.is_fk_normalized(fk, current_model):
            return fk

        fk_model = self.get_fk_model(fk, current_model)

        return dict([(self.pk_name, fk_model['id']), ('name', fk_model['name'])])


class PilotConditionsForeignKeyNormalization(SimpleForeignKeyNormalization):
    source_key = 'pilots'
    fk_source_key = 'conditions'
    fk_field_path = ['conditions', ]
    pk_name = 'condition_id'

    def normalize(self):
        for model in self.data[self.source_key]:
            current_fk = self.get_fk_field(model)
            if current_fk is None:
                continue

            new_fk = []
            for fk in current_fk:
                new_fk.append(self.construct_new_fk(fk, model))

            self.set_fk_field(model, new_fk)


class PilotShipForeignKeyNormalization(SimpleForeignKeyNormalization):
    source_key = 'pilots'
    fk_source_key = 'ships'
    fk_field_path = ['ship', ]
    pk_name = 'ship_id'

    def normalize(self):
        for model in self.data[self.source_key]:
            current_fk = self.get_fk_field(model)
            if current_fk is None:
                continue

            self.set_fk_field(model, self.construct_new_fk(current_fk, model))


class SourceContentsForeignKeyNormalization(ForeignKeyNormalizer):

    def normalize(self):
        for model in self.data[self.source_key]:
            current_fk = self.get_fk_field(model)
            if current_fk is None:
                continue

            if isinstance(current_fk, list):
                new_fk = []
                for fk in current_fk:
                    new_fk.append(self.construct_new_fk(fk, model))
            elif isinstance(current_fk, dict):
                new_fk = []
                for fk in current_fk.items():
                    new_fk.append(self.construct_new_fk(fk, model))
            else:
                new_fk = self.construct_new_fk(current_fk, model)

            self.set_fk_field(model, new_fk)

    def is_fk_normalized(self, fk, current_model):
        return isinstance(fk, dict) and self.pk_name in fk and 'amount' in fk and 'name' in fk

    def get_fk_model(self, fk, current_model):
        if isinstance(fk, dict) and self.pk_name in fk:
            model = next(
                (fk_model for fk_model in self.data[self.fk_source_key] if fk_model['id'] == fk[self.pk_name])
            )
        elif isinstance(fk, tuple) and fk[0].isdigit():
            model = next(
                (fk_model for fk_model in self.data[self.fk_source_key] if fk_model['id'] == int(fk[0]))
            )
        else:
            raise ValueError('fk {!r} is not recognized please, check!!'.format(fk))

        if model is None:
            raise ValueError('Model for fk {!r} not found'.format(fk))

        return model

    def construct_new_fk(self, fk, current_model):
        if self.is_fk_normalized(fk, current_model):
            return fk

        fk_model = self.get_fk_model(fk, current_model)

        if 'amount' in fk:
            amount = fk['amount']
        elif isinstance(fk, tuple):
            amount = fk[1]
        else:
            raise ValueError('fk {!r} missing amount!!'.format(fk))

        return dict([
            (self.pk_name, fk_model['id']),
            ('amount', amount),
            ('name', fk_model['name'])
        ])


class SourceShipsForeignKeyNormalization(SourceContentsForeignKeyNormalization):
    source_key = 'sources'
    fk_source_key = 'ships'
    fk_field_path = ['contents', 'ships']
    pk_name = 'ship_id'

    def get_fk_model(self, fk, model):
        if isinstance(fk, dict) and 'ship_id' in fk:
            model = next((ship for ship in self.data[self.fk_source_key] if ship['id'] == fk['ship_id']))
        elif isinstance(fk, tuple) and fk[0].isdigit():
            model = next((ship for ship in self.data[self.fk_source_key] if ship['id'] == int(fk[0])))
        elif isinstance(fk, str) or isinstance(fk, bytes):
            model = next((ship for ship in self.data[self.fk_source_key] if ship['name'] == fk))
        else:
            raise ValueError('fk {!r} is not recognized please, check!!')

        if model is None:
            raise ValueError('Ship for pk {!r} not found'.format(fk))

        return model

    def construct_new_fk(self, fk, model):
        if self.is_fk_normalized(fk, model):
            return fk

        fk_model = self.get_fk_model(fk, model)

        if 'amount' in fk:
            amount = fk['amount']
        else:
            amount = fk[1]

        return dict([
            (self.pk_name, fk_model['id']),
            ('amount', amount),
            ('name', fk_model['name'])
        ])


class SourceUpgradesForeignKeyNormalization(SourceContentsForeignKeyNormalization):
    source_key = 'sources'
    fk_source_key = 'upgrades'
    fk_field_path = ['contents', 'upgrades']
    pk_name = 'upgrade_id'


class SourceConditionsForeignKeyNormalization(SourceContentsForeignKeyNormalization):
    source_key = 'sources'
    fk_source_key = 'conditions'
    fk_field_path = ['contents', 'conditions']
    pk_name = 'condition_id'


class SourcePilotsForeignKeyNormalization(SourceContentsForeignKeyNormalization):
    source_key = 'sources'
    fk_source_key = 'pilots'
    fk_field_path = ['contents', 'pilots']
    pk_name = 'pilot_id'


class UpgradeConditionsForeignKeyNormalization(SimpleForeignKeyNormalization):
    source_key = 'upgrades'
    fk_source_key = 'conditions'
    fk_field_path = ['conditions', ]
    pk_name = 'condition_id'

    def normalize(self):
        for model in self.data[self.source_key]:
            current_fk_field = self.get_fk_field(model)
            if current_fk_field is None:
                continue

            new_fk = []
            for fk in current_fk_field:
                new_fk.append(self.construct_new_fk(fk, model))

            self.set_fk_field(model, new_fk)


class UpgradeShipForeignKeyNormalization(SimpleForeignKeyNormalization):
    source_key = 'upgrades'
    fk_source_key = 'ships'
    fk_field_path = ['ship', ]
    pk_name = 'ship_id'

    def normalize(self):
        for model in self.data[self.source_key]:
            current_fk_field = self.get_fk_field(model)
            if current_fk_field is None:
                continue

            new_fk = []
            for fk in current_fk_field:
                new_fk.append(self.construct_new_fk(fk, model))

            self.set_fk_field(model, new_fk)


class UpgradeShipsForeignKeyNormalization(UpgradeShipForeignKeyNormalization):
    fk_field_path = ['ships', ]

class Normalizer:
    source_key = ''
    root = None
    data = []

    def __init__(self, data):
        self.data = data
        self.analise()

    def analise(self):
        pass

    def normalize(self):
        raise NotImplementedError

    def run(self):
        print(self.__class__.__name__ + '=' * 20)
        self.normalize()
        self.analise()
        return self.data


class ForeignKeyNormalizer(Normalizer):
    fk_source_key = None
    fk_field_path = None
    pk_name = None

    def analise(self):
        print('Models in fk data', len(self.data[self.fk_source_key]))
        print('Max id in fk data', max([fkd.get('id', 0) for fkd in self.data[self.fk_source_key]]))
        print('Models with no id in fk data', [
            fkd['name'] for fkd in self.data[self.fk_source_key] if 'id' not in fkd
        ])

    def get_fk_field(self, model):
        fk = model
        for path in self.fk_field_path:
            fk = fk.get(path)
            if fk is None:
                break
        return fk

    def set_fk_field(self, model, new_fk):
        fk = model
        for path in self.fk_field_path[:-1]:
            fk = fk[path]
        fk[self.fk_field_path[-1]] = new_fk

    def is_fk_normalized(self, fk, current_model):
        raise NotImplementedError

    def get_fk_model(self, fk, current_model):
        raise NotImplementedError

    def construct_new_fk(self, fk, current_model):
        raise NotImplementedError

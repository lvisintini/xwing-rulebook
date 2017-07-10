from .base import Normalizer

from utils.lib import normalize_static_file_path


class TextToMarkdown(Normalizer):
    source_keys = ['sources', 'upgrades', 'ships', 'pilots', 'conditions',
                   'damage-deck-core', 'damage-deck-core-tfa']

    def normalize(self):

        for key in self.data.keys():
            for model in self.data[key]:
                for f in ['text', 'effect']:
                    if f in model:
                        model[f] = model[f].replace('<strong>', '**')
                        model[f] = model[f].replace('</strong>', '**')
                        model[f] = model[f].replace('<b>', '**')
                        model[f] = model[f].replace('</b>', '**')
                        model[f] = model[f].replace('<br />', '\n')
                        model[f] = model[f].replace('<br/>', '\n')
                        model[f] = model[f].replace('<em>', '*')
                        model[f] = model[f].replace('</em>', '*')
                        model[f] = model[f].replace('<i>', '*')
                        model[f] = model[f].replace('</i>', '*')


class NormalizeFilePaths(Normalizer):
    source_keys = ['sources', 'upgrades', 'ships', 'pilots', 'conditions',
                   'damage-deck-core', 'damage-deck-core-tfa']

    def normalize(self):
        for key in self.data.keys():
            for model in self.data[key]:
                for f in ['image', 'thumb']:
                    if f in model:
                        model[f] = normalize_static_file_path(model[f])

import json
from collections import OrderedDict

from django.core.management.base import BaseCommand

from rules.models import Rule


class Command(BaseCommand):
    help = 'Command to print all loaded rules as json'

    def handle(self, *args, **options):
        rules = []
        for rule in Rule.objects.order_by('name').all():
            r = OrderedDict()

            r['id'] = rule.id
            r['name'] = rule.name
            r['expansion_rule'] = rule.expansion_rule
            r['markdown'] = rule.to_markdown(False)

            references = set()
            for c in rule.clauses.all():
                references.add((c.current_content.source.code, c.current_content.page))

            r['references'] = [
                OrderedDict([
                    ('code', x),
                    ('page', y)
                ])
                for x, y in sorted(list(references))
            ]

            r['related_rules'] = [
                OrderedDict([
                    ('id', related.id),
                    ('name', related.name),
                ])
                for related in rule.related_topics.all()
            ]

            rules.append(r)

        self.stdout.write(json.dumps(rules, indent=2, ensure_ascii=False))

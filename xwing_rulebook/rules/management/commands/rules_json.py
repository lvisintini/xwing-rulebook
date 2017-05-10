import json
from collections import OrderedDict

from django.core.management.base import BaseCommand

from rules.models import Rule
from markdowns.rule import Rule2Markdown


class Command(BaseCommand):
    help = 'Command to print all loaded rules as json'

    def handle(self, *args, **options):
        rules = []
        for rule in Rule.objects.order_by('name').all():
            r = OrderedDict()

            helper = Rule2Markdown(
                rule,
                anchored=False,
                linked=False,
            )

            r['id'] = rule.id
            r['name'] = rule.name
            r['type'] = rule.type
            r['huge_ship_rule'] = rule.huge_ship_rule
            r['expansion_rule'] = rule.expansion_rule
            r['markdown'] = helper.rule_markdown()

            references = set()
            for c in rule.clauses.all():
                references.add(
                    (
                        c.current_content.source.code,
                        c.current_content.page
                    )
                )

            r['references'] = [
                OrderedDict([
                    ('code', x),
                    ('page', y)
                ])
                for x, y in sorted(list(references), key=lambda x: (x[0], x[1] is None, x[1]))
            ]

            r['related_rules'] = [
                OrderedDict([
                    ('id', related.id),
                    ('name', related.name),
                ])
                for related in rule.related_rules.all()
            ]

            rules.append(r)

        self.stdout.write(json.dumps(rules, indent=2, ensure_ascii=False))

import json
from collections import OrderedDict

from django.core.management.base import BaseCommand

from rule.models import Rule


class Command(BaseCommand):
    help = 'Command to print all loaded rules as pdf'

    def add_arguments(self, parser):
        parser.add_argument(
            '--separate-paragraphs',
            action='store_true',
            dest='separate_paragraphs',
            default=False,
            help='Provide separate paragraphs instead of whole rules.',
        )

    def handle(self, *args, **options):
        rules = []
        for rule in Rule.objects.all():
            r = OrderedDict()

            r['id'] = rule.id
            r['name'] = rule.name
            r['expansion_rule'] = rule.expansion_rule

            if options['separate_paragraphs']:
                r['paragraphs'] = [
                    OrderedDict(
                        markdown=p.text,
                        order=p.order,
                        expansion_rule_related=p.format.get('expansion_rule', rule.expansion_rule),
                        format=OrderedDict(sorted(
                            [(k, v) for k, v in p.format.items() if k != "expansion_rule"],
                            key=lambda x: x[0]
                        )),
                        references=[
                            OrderedDict(
                                code=reference.source.code,
                                page=reference.page,
                            )
                            for reference in p.reference_set.all()
                        ]
                    )
                    for p in rule.paragraphs.order_by('order').all()
                ]
            else:
                r['markdown'] = rule.to_markdown(False)

            references = set()
            for p in rule.paragraphs.all():
                for reference in p.reference_set.all():
                    references.add((reference.source.code, reference.page))

            r['references'] = [
                OrderedDict(
                    code=x,
                    page=y
                )
                for x, y in sorted(list(references))
            ]

            r['related_rules'] = [
                OrderedDict(
                    id=related.id,
                    name=related.name,
                )
                for related in rule.related_topics.all()
            ]

            rules.append(r)

        self.stdout.write(json.dumps(rules, indent=2, ensure_ascii=False))

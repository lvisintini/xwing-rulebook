# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 22:52
from __future__ import unicode_literals

from django.db import migrations


def migrate_to_other_apps(apps, schema_editor):

    # SOURCE

    oSource = apps.get_model("rule", "Source")
    nSource = apps.get_model("rules", "Source")
    source_mapping = {}

    for o_source in oSource.objects.all():
        n_source = nSource(
            name=o_source.name,
            date=o_source.date,
            version=o_source.version,
            code=o_source.code,
            processed=o_source.processed,
            file=o_source.file,
        )
        n_source.save()
        source_mapping[o_source.id] = n_source.id

    # CONTENT

    oContent = apps.get_model("rule", "ClauseContent")
    nContent = apps.get_model("rules", "Content")
    content_mapping = {}

    for o_content in oContent.objects.all():
        n_content = nContent(
            title=o_content.title,
            content=o_content.content,
            source_id=source_mapping[o_content.source.id],
            page=o_content.page,
            keep_line_breaks=o_content.keep_line_breaks,
            file=o_content.file,
        )
        n_content.save()
        content_mapping[o_content.id] = n_content.id

    # RULE

    oRule = apps.get_model("rule", "Rule")
    nRule = apps.get_model("rules", "Rule")
    rule_mapping = {}

    for o_rule in oRule.objects.all():
        n_rule = nRule(
            name=o_rule.name,
            slug=o_rule.slug,
            expansion_rule=o_rule.expansion_rule,
        )
        n_rule.save()
        rule_mapping[o_rule.id] = n_rule.id

    for o_rule in oRule.objects.all():
        n_rule = nRule.objects.get(pk=rule_mapping[o_rule.id])
        for rt in o_rule.related_topics.all():
            if rule_mapping[rt.id] not in [n_rule.related_topics.values_list('id', flat=True)]:
                n_rule.related_topics.add(nRule.objects.get(pk=rule_mapping[rt.id]))

    # CLAUSE

    oClause = apps.get_model("rule", "Clause")
    nClause = apps.get_model("rules", "Clause")
    clause_mapping = {}

    for o_clause in oClause.objects.all():
        n_clause = nClause(
            rule_id=rule_mapping[o_clause.rule.id],
            order=o_clause.order,
            type=o_clause.type,
            expansion_related=o_clause.expansion_related,
            indentation=o_clause.indentation,
            ignore_title=o_clause.ignore_title,
            needs_revision=o_clause.needs_revision,
        )
        n_clause.save()
        clause_mapping[o_clause.id] = n_clause.id

    # CLAUSE CONTENT

    oClauseContent = apps.get_model("rule", "ClauseContentVersion")
    nClauseContent = apps.get_model("rules", "ClauseContent")
    clause_content_mapping = {}

    for o_clause_content in oClauseContent.objects.all():
        n_clause_content = nClauseContent(
            clause_id=clause_mapping[o_clause_content.clause.id],
            content_id=content_mapping[o_clause_content.content.id],
            active=o_clause_content.active,
        )
        n_clause_content.save()
        clause_content_mapping[o_clause_content.id] = n_clause_content.id

    # BOOK

    oBook = apps.get_model("rule", "RuleBook")
    nBook = apps.get_model("books", "Book")
    book_mapping = {}

    for o_book in oBook.objects.all():
        n_book = nBook(
            name=o_book.name,
            slug=o_book.slug,
            code=o_book.code,
            version=o_book.version,
            description=o_book.description,
        )
        n_book.save()
        book_mapping[o_book.id] = n_book.id

    # SECTION

    oSection = apps.get_model("rule", "BookSection")
    nSection = apps.get_model("books", "Section")
    section_mapping = {}

    for o_section in oSection.objects.all():
        n_section = nSection(
            book_id=book_mapping[o_section.rule_book.id],
            order=o_section.order,
            title=o_section.title,
            slug=o_section.slug,
            content=o_section.content
        )
        n_section.save()
        section_mapping[o_section.id] = n_section.id

    # SECTION RULE

    oSectionRule = apps.get_model("rule", "SectionRule")
    nSectionRule = apps.get_model("books", "SectionRule")
    section_rule_mapping = {}

    for o_section_rule in oSectionRule.objects.all():
        n_section_rule = nSectionRule(
            section_id=section_mapping[o_section_rule.book_section.id],
            rule_id=rule_mapping[o_section_rule.rule.id],
            order=o_section_rule.order,
        )
        n_section_rule.save()
        section_rule_mapping[o_section_rule.id] = n_section_rule.id


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0036_auto_20170109_0245'),
        ('rules', '0001_initial'),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_to_other_apps, do_nothing)
    ]

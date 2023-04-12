# Generated by Django 3.2.17 on 2023-02-11 12:13

import sortedm2m.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("literature", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="literature",
            name="authors",
            field=sortedm2m.fields.SortedManyToManyField(
                blank=True,
                help_text=None,
                related_name="literature",
                sort_value_field_name="number",
                through="literature.LiteratureAuthor",
                to="literature.Author",
                verbose_name="authors",
            ),
        ),
    ]

# Generated by Django 3.2.10 on 2021-12-24 11:23

import django.core.validators
from django.db import migrations
import re
import simpleblog.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('simpleblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='contents',
            field=wagtail.core.fields.StreamField([('richtext', simpleblog.blocks.RichtextBlock()), ('rawhtml', wagtail.core.blocks.TextBlock()), ('blockcode', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.CharBlock(required=True)), ('filename', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.TextBlock(required=False)), ('code', wagtail.core.blocks.TextBlock(required=True))])), ('postchooser', wagtail.core.blocks.PageChooserBlock(page_type=['simpleblog.Post'])), ('oembed', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')])), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('embed', wagtail.embeds.blocks.EmbedBlock(max_height=400, max_width=800))])), ('gistembed', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(required=True)), ('file', wagtail.core.blocks.CharBlock(help_text='If the gist has multiple files, specify the filename you want to show', required=False)), ('line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to show. The rest are removed. 1-3 or 1,2,3 or 2-', required=False)), ('highlight_line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to highlight. Uses the same syntax for line ranges as line', required=False)), ('hide_footer', wagtail.core.blocks.BooleanBlock(help_text='Removes the gist footer', required=False)), ('caption', wagtail.core.blocks.TextBlock(help_text='Places a header above the gist with your chosen caption string', required=False))])), ('table', simpleblog.blocks.CustomTableBlock(table_options={'autoColumnSize': False, 'colHeaders': False, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo'], 'editor': 'text', 'height': 108, 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': False, 'startCols': 3, 'startRows': 3, 'stretchH': 'all'}))], blank=True, help_text='Contents', null=True),
        ),
        migrations.AlterField(
            model_name='index',
            name='contents',
            field=wagtail.core.fields.StreamField([('richtext', simpleblog.blocks.RichtextBlock()), ('rawhtml', wagtail.core.blocks.TextBlock()), ('blockcode', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.CharBlock(required=True)), ('filename', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.TextBlock(required=False)), ('code', wagtail.core.blocks.TextBlock(required=True))])), ('postchooser', wagtail.core.blocks.PageChooserBlock(page_type=['simpleblog.Post'])), ('oembed', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')])), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('embed', wagtail.embeds.blocks.EmbedBlock(max_height=400, max_width=800))])), ('gistembed', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(required=True)), ('file', wagtail.core.blocks.CharBlock(help_text='If the gist has multiple files, specify the filename you want to show', required=False)), ('line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to show. The rest are removed. 1-3 or 1,2,3 or 2-', required=False)), ('highlight_line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to highlight. Uses the same syntax for line ranges as line', required=False)), ('hide_footer', wagtail.core.blocks.BooleanBlock(help_text='Removes the gist footer', required=False)), ('caption', wagtail.core.blocks.TextBlock(help_text='Places a header above the gist with your chosen caption string', required=False))])), ('table', simpleblog.blocks.CustomTableBlock(table_options={'autoColumnSize': False, 'colHeaders': False, 'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo'], 'editor': 'text', 'height': 108, 'minSpareRows': 0, 'renderer': 'text', 'rowHeaders': False, 'startCols': 3, 'startRows': 3, 'stretchH': 'all'}))], blank=True, help_text='Contents', null=True),
        ),
    ]

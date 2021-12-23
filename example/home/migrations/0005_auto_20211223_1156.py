# Generated by Django 3.2.10 on 2021-12-23 11:56

from django.db import migrations, models
import django.db.models.deletion
import simple_blog.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('simple_blog', '0003_index_contents'),
        ('home', '0004_homepage_contents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simple_blog.post')),
                ('contents', wagtail.core.fields.StreamField([('richtext', simple_blog.blocks.RichtextBlock()), ('choosen_pages', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('list', 'Page List'), ('card', 'Page Card')])), ('columns', wagtail.core.blocks.IntegerBlock(default=2, max_value=4, min_value=1)), ('show_thumbnail', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('show_summary', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('pages', wagtail.core.blocks.ListBlock(child_block=wagtail.core.blocks.PageChooserBlock(page_type=['simple_blog.Post'])))])), ('embed', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('embed', wagtail.embeds.blocks.EmbedBlock(max_height=400, max_width=800))])), ('code', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.CharBlock(required=True)), ('filename', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.TextBlock(required=False)), ('code', wagtail.core.blocks.TextBlock(required=True))])), ('gist', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(required=True)), ('file', wagtail.core.blocks.CharBlock(help_text='If the gist has multiple files, specify the filename you want to show', required=False)), ('line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to show. The rest are removed. 1-3 or 1,2,3 or 2-', required=False)), ('highlight_line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to highlight. Uses the same syntax for line ranges as line', required=False)), ('hide_footer', wagtail.core.blocks.BooleanBlock(help_text='Removes the gist footer', required=False)), ('caption', wagtail.core.blocks.TextBlock(help_text='Places a header above the gist with your chosen caption string', required=False))]))], blank=True, help_text='Contents', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('simple_blog.post',),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='contents',
            field=wagtail.core.fields.StreamField([('richtext', simple_blog.blocks.RichtextBlock()), ('choosen_pages', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('list', 'Page List'), ('card', 'Page Card')])), ('columns', wagtail.core.blocks.IntegerBlock(default=2, max_value=4, min_value=1)), ('show_thumbnail', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('show_summary', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('pages', wagtail.core.blocks.ListBlock(child_block=wagtail.core.blocks.PageChooserBlock(page_type=['simple_blog.Post'])))]))], blank=True, help_text='Contents', null=True),
        ),
    ]

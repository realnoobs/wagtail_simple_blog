# Generated by Django 3.2.10 on 2021-12-24 06:49

from django.db import migrations, models
import django.db.models.deletion
import simpleblog.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('simpleblog', '0001_initial'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpleblog.post')),
                ('contents', wagtail.core.fields.StreamField([('richtext', simpleblog.blocks.RichtextBlock()), ('choosen_pages', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('list', 'Page List'), ('card', 'Page Card')])), ('columns', wagtail.core.blocks.IntegerBlock(default=2, max_value=4, min_value=1)), ('show_thumbnail', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('show_summary', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('pages', wagtail.core.blocks.ListBlock(child_block=wagtail.core.blocks.PageChooserBlock(page_type=['simpleblog.Post'])))])), ('embed', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('embed', wagtail.embeds.blocks.EmbedBlock(max_height=400, max_width=800))])), ('code', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.CharBlock(required=True)), ('filename', wagtail.core.blocks.CharBlock(required=False)), ('caption', wagtail.core.blocks.TextBlock(required=False)), ('code', wagtail.core.blocks.TextBlock(required=True))])), ('gist', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(required=True)), ('file', wagtail.core.blocks.CharBlock(help_text='If the gist has multiple files, specify the filename you want to show', required=False)), ('line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to show. The rest are removed. 1-3 or 1,2,3 or 2-', required=False)), ('highlight_line', wagtail.core.blocks.CharBlock(help_text='Line numbers you want to highlight. Uses the same syntax for line ranges as line', required=False)), ('hide_footer', wagtail.core.blocks.BooleanBlock(help_text='Removes the gist footer', required=False)), ('caption', wagtail.core.blocks.TextBlock(help_text='Places a header above the gist with your chosen caption string', required=False))]))], blank=True, help_text='Contents', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('simpleblog.post',),
        ),
        migrations.AddField(
            model_name='home',
            name='allow_comments',
            field=models.BooleanField(default=True, help_text='Allow visitors to comments'),
        ),
        migrations.AddField(
            model_name='home',
            name='contents',
            field=wagtail.core.fields.StreamField([('richtext', simpleblog.blocks.RichtextBlock()), ('choosen_pages', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('list', 'Page List'), ('card', 'Page Card')])), ('columns', wagtail.core.blocks.IntegerBlock(default=2, max_value=4, min_value=1)), ('show_thumbnail', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('show_summary', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('pages', wagtail.core.blocks.ListBlock(child_block=wagtail.core.blocks.PageChooserBlock(page_type=['simpleblog.Post'])))]))], blank=True, help_text='Contents', null=True),
        ),
        migrations.AddField(
            model_name='home',
            name='custom_scripts',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='home',
            name='custom_styles',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='home',
            name='custom_template',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='home',
            name='show_comments',
            field=models.BooleanField(default=True, help_text='Show all comments'),
        ),
        migrations.AddField(
            model_name='home',
            name='summary',
            field=wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Summary'),
        ),
        migrations.AddField(
            model_name='home',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='home',
            name='view_count',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]

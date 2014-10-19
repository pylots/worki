# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('last_edit', models.DateTimeField(auto_now=True)),
                ('ttl', models.DateTimeField(null=True, blank=True)),
                ('version', models.IntegerField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name=b'children', blank=True, to='wiki_page.WikiPage', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ('slug',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WikiPageViewLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_time', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(related_name=b'page_views', to='wiki_page.WikiPage')),
                ('user', models.ForeignKey(related_name=b'page_views', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

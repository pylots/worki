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
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='wiki_page.WikiPage', null=True, on_delete=models.SET_NULL)),
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
                ('page', models.ForeignKey(related_name='page_views', to='wiki_page.WikiPage', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(related_name='page_views', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

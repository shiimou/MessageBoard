# Generated by Django 3.2.5 on 2022-04-18 10:49

import ckeditor_uploader.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='留言内容')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('comment_nums', models.IntegerField(default=0, verbose_name='评论数')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '留言管理',
                'verbose_name_plural': '留言管理',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', max_length=500, verbose_name='评论详情')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.articles', verbose_name='留言')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论用户')),
            ],
            options={
                'verbose_name': '用户评论',
                'verbose_name_plural': '用户评论',
            },
        ),
    ]

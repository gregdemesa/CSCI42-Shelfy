# Generated by Django 5.1.3 on 2025-03-19 13:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelfy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('comment_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media_comment_author', to=settings.AUTH_USER_MODEL)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shelfy.media')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]

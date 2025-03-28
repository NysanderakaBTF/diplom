# Generated by Django 5.1.5 on 2025-02-12 20:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('pinterest', 'Pinterest'), ('facebook', 'Facebook'), ('vk', 'VK')], max_length=50)),
                ('token', models.CharField(max_length=500)),
                ('token_secret', models.CharField(blank=True, max_length=500, null=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

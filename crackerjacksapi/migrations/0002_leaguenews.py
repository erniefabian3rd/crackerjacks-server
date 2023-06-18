# Generated by Django 4.2.2 on 2023-06-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crackerjacksapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('article', models.CharField(max_length=255)),
                ('published_date', models.CharField(max_length=100)),
                ('link_url', models.TextField(blank=True, null=True)),
            ],
        ),
    ]

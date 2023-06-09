# Generated by Django 4.2.2 on 2023-06-08 15:35

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
            name='CrackerjacksUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=255)),
                ('profile_image_url', models.TextField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Park',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=100)),
                ('image_url', models.TextField(blank=True, null=True)),
                ('capacity', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.TextField(blank=True, null=True)),
                ('caption', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_published', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image_url', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserVisitedPark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_visited', to='crackerjacksapi.park')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visited_parks', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_signed_up', to='crackerjacksapi.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips_signed_up', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=255)),
                ('image_url', models.TextField(blank=True, null=True)),
                ('park', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='crackerjacksapi.park')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to='crackerjacksapi.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='post_likes', through='crackerjacksapi.PostLike', to='crackerjacksapi.crackerjacksuser'),
        ),
        migrations.CreateModel(
            name='ParkReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=255)),
                ('park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='park_reviews', to='crackerjacksapi.park')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_of_parks', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.CreateModel(
            name='ParkRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='park_rating', to='crackerjacksapi.park')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_of_parks', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.AddField(
            model_name='park',
            name='rating',
            field=models.ManyToManyField(related_name='park_ratings', through='crackerjacksapi.ParkRating', to='crackerjacksapi.crackerjacksuser'),
        ),
        migrations.AddField(
            model_name='park',
            name='review',
            field=models.ManyToManyField(related_name='park_reviews', through='crackerjacksapi.ParkReview', to='crackerjacksapi.crackerjacksuser'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to='crackerjacksapi.crackerjacksuser')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_on', models.DateField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='crackerjacksapi.crackerjacksuser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='crackerjacksapi.crackerjacksuser')),
            ],
        ),
        migrations.AddField(
            model_name='crackerjacksuser',
            name='favorite_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_teams', to='crackerjacksapi.team'),
        ),
        migrations.AddField(
            model_name='crackerjacksuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='crackerjacksapi.crackerjacksuser')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='crackerjacksapi.post')),
            ],
        ),
    ]

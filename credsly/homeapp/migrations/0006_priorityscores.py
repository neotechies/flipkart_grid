# Generated by Django 3.2.7 on 2021-09-28 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_user_total_credit'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriorityScores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority_one_weight', models.IntegerField(default=100)),
                ('priority_two_weight', models.IntegerField(default=80)),
                ('priority_three_weight', models.IntegerField(default=50)),
            ],
        ),
    ]

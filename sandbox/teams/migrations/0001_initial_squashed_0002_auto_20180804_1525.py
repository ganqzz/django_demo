# Generated by Django 3.1.7 on 2021-03-31 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [('teams', '0001_initial'), ('teams', '0002_auto_20180804_1525')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('practice_location', models.CharField(max_length=255)),
                ('coach', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('position', models.CharField(
                    choices=[('GK', 'Goalkeeper'), ('CB', 'Center fullback'), ('SW', 'Sweeper'),
                             ('LFB', 'Left fullback'), ('RFB', 'Right fullback'),
                             ('WB', 'Wingback'), ('LM', 'Left midfield'), ('RM', 'Right midfield'),
                             ('DM', 'Defensive midfield'), ('CM', 'Center midfield'),
                             ('WM', 'Wide midfield'), ('CF', 'Center forward'),
                             ('AM', 'Attacking midfield'), ('S', 'Striker'),
                             ('SS', 'Second striker'), ('LW', 'Left winger'),
                             ('RW', 'Right winger')], max_length=3)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='players', to='teams.team')),
            ],
        ),
    ]
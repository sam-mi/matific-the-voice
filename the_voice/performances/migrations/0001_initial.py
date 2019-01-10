# Generated by Django 2.0.10 on 2019-01-09 21:37

from django.conf import settings
import django.contrib.postgres.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', model_utils.fields.StatusField(choices=[('active', 'Active'), ('closed', 'Closed'), ('inactive', 'Inactive')], default='active', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('timeslot', models.DateTimeField(blank=True, db_index=True, help_text='Performance Time Slot is the date and time that a performance is scheduled to take place, including the duration of the performance.', null=True)),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('score', models.IntegerField(blank=True, validators=[django.contrib.postgres.validators.RangeMinValueValidator(1), django.contrib.postgres.validators.RangeMaxValueValidator(100)])),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='performances.Performance')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', model_utils.fields.StatusField(choices=[('active', 'Active'), ('closed', 'Closed'), ('inactive', 'Inactive')], default='active', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(help_text='Team name', max_length=255)),
                ('slug', models.CharField(default=uuid.uuid4, max_length=255, unique=True)),
                ('candidates', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='team', to=settings.AUTH_USER_MODEL)),
                ('mentors', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to='performances.Song'),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together={('mentor', 'performance', 'score')},
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together={('performer', 'song')},
        ),
    ]

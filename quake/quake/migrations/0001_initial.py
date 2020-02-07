# Generated by Django 3.0.2 on 2020-02-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Eathquake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=50)),
                ('src', models.CharField(blank=True, max_length=50, null=True)),
                ('id_eathquake', models.CharField(blank=True, max_length=50, null=True)),
                ('version', models.CharField(blank=True, max_length=50, null=True)),
                ('eathquake_time', models.DateTimeField(blank=True, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True)),
                ('mag', models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True)),
                ('depth', models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True)),
                ('nst', models.CharField(blank=True, max_length=50, null=True)),
                ('region', models.CharField(blank=True, max_length=2500, null=True)),
                ('data_source', models.CharField(blank=True, max_length=500, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=2500, null=True)),
                ('lat_deg', models.CharField(blank=True, max_length=100, null=True)),
                ('lng_deg', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['eathquake_time'],
            },
        ),
    ]

# Generated by Django 3.0.2 on 2020-01-15 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quakemap', '0005_auto_20200115_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eathquake',
            name='create_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='data_source',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='depth',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='eathquake_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='id_eathquake',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='mag',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='nst',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='region',
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='src',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='eathquake',
            name='version',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

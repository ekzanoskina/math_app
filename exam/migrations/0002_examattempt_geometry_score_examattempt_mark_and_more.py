# Generated by Django 4.2.4 on 2024-05-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examattempt',
            name='geometry_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='examattempt',
            name='mark',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='examattempt',
            name='max_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examattempt',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
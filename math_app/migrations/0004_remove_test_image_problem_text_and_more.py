# Generated by Django 4.2.4 on 2023-10-05 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('math_app', '0003_remove_test_image_test_image_problem_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='image_problem_text',
        ),
        migrations.RemoveField(
            model_name='test',
            name='image_solution',
        ),
    ]

# Generated by Django 4.2.9 on 2024-01-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_alter_response_approve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]

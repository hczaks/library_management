# Generated by Django 3.2.20 on 2023-08-03 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20230803_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminborrowing',
            name='borrower',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app1.admin', verbose_name='借阅人'),
        ),
    ]

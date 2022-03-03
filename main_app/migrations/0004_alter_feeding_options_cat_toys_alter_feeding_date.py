# Generated by Django 4.0.2 on 2022-02-26 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_feeding'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feeding',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='cat',
            name='toys',
            field=models.ManyToManyField(to='main_app.Toy'),
        ),
        migrations.AlterField(
            model_name='feeding',
            name='date',
            field=models.DateField(verbose_name='feeding date'),
        ),
    ]
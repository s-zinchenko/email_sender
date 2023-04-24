# Generated by Django 4.2 on 2023-04-24 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtable',
            name='status',
            field=models.CharField(choices=[('uploaded', 'Uploaded'), ('recipients_created', 'Recipients Created'), ('mailing_in_progress', 'Mailing In Progress'), ('finished', 'Finished')], default='uploaded', verbose_name='Статус'),
        ),
        migrations.CreateModel(
            name='ExtraFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Имя файла')),
                ('file', models.FileField(upload_to='', verbose_name='Файл')),
                ('table', models.ManyToManyField(to='main.emailtable', verbose_name='Связанная таблица')),
            ],
            options={
                'verbose_name': 'Дополнительный файл',
                'verbose_name_plural': 'Дополнительные файлы',
            },
        ),
    ]

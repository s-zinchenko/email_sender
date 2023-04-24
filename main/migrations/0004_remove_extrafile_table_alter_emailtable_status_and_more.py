# Generated by Django 4.2 on 2023-04-24 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_extrafiles_extrafile_alter_emailtable_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrafile',
            name='table',
        ),
        migrations.AlterField(
            model_name='emailtable',
            name='status',
            field=models.CharField(choices=[('uploaded', 'Uploaded'), ('recipients_created', 'Recipients Created'), ('mailing_in_progress', 'Mailing In Progress'), ('finished', 'Finished')], default='uploaded', verbose_name='Статус'),
        ),
        migrations.CreateModel(
            name='ExtraFileEmailTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_table', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.emailtable', verbose_name='Таблица с получателями')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.extrafile', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Привязка файла к таблице с почтами',
                'verbose_name_plural': 'Привязки файлов к таблицам с почтами',
            },
        ),
    ]

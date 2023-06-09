# Generated by Django 4.2 on 2023-04-10 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки файла')),
                ('table_file', models.FileField(upload_to='', verbose_name='Шаблон файла')),
                ('successful_sendings', models.IntegerField(default=-1, verbose_name='Успешные отправки')),
                ('recipients_amount', models.IntegerField(blank=True, null=True, verbose_name='Количество получателей')),
                ('sendings', models.IntegerField(default=0, verbose_name='Успешные отправки')),
                ('status', models.CharField(choices=[('uploaded', 'Uploaded'), ('recipients_created', 'Recipients Created'), ('mailing_in_progress', 'Mailing In Progress'), ('finished', 'Finished')], default='uploaded', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Файл с электронными почтами',
                'verbose_name_plural': 'Файлы с электронными почтами',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.FileField(upload_to='', verbose_name='Шаблон файла')),
            ],
            options={
                'verbose_name': 'Шаблон письма',
            },
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта адресата')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.emailtable', verbose_name='Таблица с получателями')),
            ],
            options={
                'verbose_name': 'Получатель письма',
                'verbose_name_plural': 'Получатели писем',
            },
        ),
    ]

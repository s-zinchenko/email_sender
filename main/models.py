from django.db import models
from django.db.models import Choices
from solo.models import SingletonModel

from main.tasks import create_recipients


class EmailTemplate(SingletonModel):
    class Meta:
        verbose_name = "Шаблон письма"

    template = models.FileField(verbose_name="Шаблон файла")


class EmailTable(models.Model):
    class Meta:
        verbose_name = "Файл с электронными почтами"
        verbose_name_plural = "Файлы с электронными почтами"

    class ProcessStatus(Choices):
        UPLOADED = "uploaded"
        recipientS_CREATED = "recipients_created"
        MAILING_IN_PROGRESS = "mailing_in_progress"
        FINISHED = "finished"

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки файла")
    table_file = models.FileField(verbose_name="Шаблон файла")
    successful_sendings = models.IntegerField(verbose_name="Успешные отправки", default=-1)
    recipients_amount = models.IntegerField(verbose_name="Количество получателей", null=True, blank=True)
    sendings = models.IntegerField(verbose_name="Успешные отправки", default=0)
    status = models.CharField(choices=ProcessStatus.choices, default=ProcessStatus.UPLOADED, verbose_name="Статус")

    @property
    def successful_percent(self) -> float:
        return self.successful_sendings / self.recipients_amount

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == self.ProcessStatus.UPLOADED.value:
            create_recipients.apply_async((self.id,))


class Recipient(models.Model):
    class Meta:
        verbose_name = "Получатель письма"
        verbose_name_plural = "Получатели писем"

    email = models.EmailField(verbose_name="Электронная почта адресата")
    table = models.ForeignKey("main.EmailTable", verbose_name="Таблица с получателями", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.email

# сделать у таблицы счётчик успешно отправленных писем
# в таску передавать id таблицы
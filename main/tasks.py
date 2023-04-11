import logging
import os
from datetime import timedelta

import openpyxl as openpyxl
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from main.utils import send_template_mail


logger = logging.getLogger()


@shared_task
def create_recipients(table_id: int):
    from main.models import EmailTable, Recipient

    print(table_id)
    table = EmailTable.objects.get(id=table_id)
    table_file = table.table_file
    dataframe = openpyxl.load_workbook(table_file.path)
    dataframe1 = dataframe.active

    seller_email_column = dataframe1._cells[(1,1)]
    if seller_email_column.value != "sellerEmail":
        raise Exception

    recipients = []
    recipients_amount = 0
    with transaction.atomic():
        for row in range(0, dataframe1.max_row):
            for col in dataframe1.iter_cols(1, 1):
                if not col[row].value or col[row].value == "sellerEmail":
                    continue
                recipients.append(
                    Recipient(
                        email=col[row].value,
                        table_id=table_id,
                    )
                )
                recipients_amount += 1
                if len(recipients) == 1000:
                    Recipient.objects.bulk_create(recipients)
                    recipients = []
        Recipient.objects.bulk_create(recipients)
        # EmailTable.objects.filter(table_id=table_id).update(status=EmailTable.ProcessStatus.recipientS_CREATED)
        # initiate_msg_sending()
        EmailTable.objects.filter(id=table_id).update(
            status=EmailTable.ProcessStatus.recipientS_CREATED.value,
            recipients_amount=recipients_amount
        )

    initiate_msg_sending.apply_async((table_id,))


@shared_task
def initiate_msg_sending(table_id: int):
    from main.models import Recipient, EmailTable

    LIMIT = 1000
    OFFSET = 0
    recipients = Recipient.objects.filter(table_id=table_id)[OFFSET: LIMIT]
    EmailTable.objects.filter(id=table_id).update(status=EmailTable.ProcessStatus.MAILING_IN_PROGRESS.value, )
    while recipients:
        for recipient in recipients:
            send_msg.apply_async((recipient.email, table_id))
        OFFSET += LIMIT

        recipients = Recipient.objects.all()[OFFSET: LIMIT + OFFSET]


@shared_task
def send_msg(recipient: str, table_id: int):
    from main.models import EmailTemplate, EmailTable

    template = EmailTemplate.objects.get().template.path

    try:
        send_template_mail("новые предложения", template, {"test": "test"}, recipient)
    except Exception as e:
        logger.error(f"recipient: {recipient}, table_id: {table_id}, {e}")
    email_table = EmailTable.objects.filter(id=table_id).first()
    if email_table:
        if email_table.sendings + 1 == email_table.recipients_amount:
            email_table.status = EmailTable.ProcessStatus.FINISHED.value
        else:
            email_table.sendings += 1
        email_table.save()


@shared_task
def delete_old_tables():
    from main.models import EmailTable
    tables = EmailTable.objects.filter(uploaded_at__lte=timezone.now() - timedelta(days=30))
    for table in tables:
        if os.path.isfile(table.table_file.path):
            os.remove(table.table_file.path)
        table.delete()

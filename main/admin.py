from django.contrib import admin
from solo.admin import SingletonModelAdmin

from main.models import Recipient, EmailTemplate, EmailTable


@admin.register(EmailTemplate)
class EmailTemplateAdmin(SingletonModelAdmin):
    pass


@admin.register(EmailTable)
class EmailTableAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    pass

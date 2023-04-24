from django.contrib import admin
from solo.admin import SingletonModelAdmin

from main.models import Recipient, EmailTemplate, EmailTable, ExtraFile, ExtraFileEmailTable


@admin.register(EmailTemplate)
class EmailTemplateAdmin(SingletonModelAdmin):
    pass


class ExtraFileEmailTableAdminInline(admin.TabularInline):
    model = ExtraFileEmailTable


@admin.register(EmailTable)
class EmailTableAdmin(admin.ModelAdmin):
    inlines = [ExtraFileEmailTableAdminInline,]
    readonly_fields = (
        "uploaded_at",
        "recipients_amount",
        "sendings",
        "successful_sendings",
    )


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtraFile)
class ExtraFileAdmin(admin.ModelAdmin):
    pass

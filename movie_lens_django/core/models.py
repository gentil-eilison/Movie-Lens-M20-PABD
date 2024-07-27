from django.db import models
from django.utils.translation import gettext_lazy as _


class CSVImportMetaData(models.Model):
    upload_time_in_minutes = models.PositiveIntegerField(
        verbose_name=_("Upload Time in Minutes"),
        null=True,
    )
    inserted_data_count = models.PositiveBigIntegerField(
        verbose_name=_("Inserted Data Count"),
        null=True,
    )
    errors_count = models.PositiveBigIntegerField(
        verbose_name=_("Errors Count"),
        null=True,
    )
    csv_file = models.FileField(verbose_name=_("CSV File"))

    class Meta:
        verbose_name = _("CSV Import Meta Data")
        verbose_name_plural = _("CSV Imports Meta Data")

    def __str__(self):
        return f"{self.csv_file.name}"

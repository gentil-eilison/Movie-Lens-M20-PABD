from django.db import models
from django.utils.translation import gettext_lazy as _


class CSVImportMetaData(models.Model):
    upload_time_in_seconds = models.PositiveIntegerField(
        verbose_name=_("Upload Time in Minutes"),
        default=0,
    )
    inserted_data_count = models.PositiveBigIntegerField(
        verbose_name=_("Inserted Data Count"),
        default=0,
    )
    errors_count = models.PositiveBigIntegerField(
        verbose_name=_("Errors Count"),
        default=0,
    )
    csv_file = models.FileField(verbose_name=_("CSV File"))

    class Meta:
        verbose_name = _("CSV Import Meta Data")
        verbose_name_plural = _("CSV Imports Meta Data")

    def __str__(self):
        return f"{self.csv_file.name}"

    @property
    def formatted_upload_time(self):
        minutes, seconds = divmod(self.upload_time_in_seconds, 60)
        if minutes:
            return f"{minutes} min {seconds} s"
        return f"{seconds} s"

    @property
    def formatted_inserted_data_count(self):
        return f"{self.inserted_data_count:,}".replace(",", ".")

    @property
    def formatted_errors_count(self):
        return f"{self.errors_count:,}".replace(",", ".")

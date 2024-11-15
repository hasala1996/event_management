from django.db import models

from core.management.commands.base_model import (
    BaseModel,
)


class Category(BaseModel):
    """
    Represents the category of an event (conference, workshop, etc.).
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"

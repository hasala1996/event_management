import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from django.db import models

from safedelete.managers import SafeDeleteManager, DELETED_INVISIBLE


class BasicManager(SafeDeleteManager):
    _safedelete_visibility = DELETED_INVISIBLE


class BaseModel(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    created_by = models.UUIDField(
        null=True, editable=False, db_column="created_by")

    modified_at = models.DateTimeField(
        auto_now=True,
        null=True,
        db_column="modified_at"
    )
    modified_by = models.UUIDField(
        null=True, editable=False, db_column="modified_by")

    deleted_at = models.DateTimeField(
        null=True,
        db_column="deleted_at"
    )

    deleted_by = models.UUIDField(
        null=True, editable=False, db_column="deleted_by")
    _safedelete_policy = SOFT_DELETE_CASCADE
    objects = BasicManager()

    class Meta:
        abstract = True

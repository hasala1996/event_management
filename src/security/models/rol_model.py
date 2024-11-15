from django.db import models
from core.management.commands.base_model import BaseModel
from django.contrib.auth.models import Permission


class Rol(BaseModel):
    """
    Represents a role within the system, optionally associated with permissions.

    Attributes:
        name (CharField): The name of the role, limited to 50 characters.
        description (CharField): An optional textual description of the role,
        limited to 150 characters.
        active (BooleanField): Indicates whether the role is active. Defaults to True.
        permissions (ManyToManyField): A many-to-many relationship linking roles
        to permissions, allowing for flexible permission
        assignment.
    """

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, null=True, blank=True)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")

    class Meta:
        db_table = "rol"

    def __str__(self):
        """
        Returns a string representation of the role, primarily its name.

        Returns:
            str: The name of the role.
        """
        return self.name

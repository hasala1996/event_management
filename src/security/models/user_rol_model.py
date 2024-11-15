from django.db import models
from core.management.commands.base_model import BaseModel
from security.models import User, Rol


class UserRol(BaseModel):
    """
    Establishes a relationship between users and roles within the system.

    Attributes:
        user (ForeignKey): A foreign key to the User model. Represents the user associated with the role.
        rol (ForeignKey): A foreign key to the Rol model. Represents the role assigned to the user.
        active (BooleanField): Indicates whether the user's role is currently active or not. Defaults to True.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_rol"

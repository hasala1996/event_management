from django import forms
from django.core.exceptions import ValidationError
from .models import Rol, UserRol, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


class RolForm(forms.ModelForm):
    """
    A form for creating and updating Rol instances.

    This form ensures that each role has a unique name and a description
    of sufficient length. It includes validation to enforce these rules.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        custom_content_types = ContentType.objects.filter(
            model__in=["event", "reservation"]
        )
        self.fields["permissions"].queryset = Permission.objects.filter(
            content_type__in=custom_content_types
        )

    class Meta:
        model = Rol
        fields = ["name", "description", "active", "permissions"]

    def clean_name(self):
        """
        Validate the 'name' field to ensure it is unique (case insensitive),
        excluding the current instance if it already exists.

        Raises:
            ValidationError: If another role with the same name already exists.

        Returns:
            str: The cleaned name data.
        """
        name = self.cleaned_data.get("name")
        existing_roles = Rol.objects.filter(name__iexact=name)
        if self.instance.pk:
            existing_roles = existing_roles.exclude(pk=self.instance.pk)
        if existing_roles.exists():
            raise ValidationError(
                "The role name already exists. Please choose a different name."
            )
        return name

    def clean_description(self):
        """
        Validate the 'description' field to ensure it meets length requirements.

        Raises a ValidationError if the description has fewer than 10 characters.

        Returns:
            str: The cleaned description data.
        """
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise ValidationError(
                "The description must be at least 10 characters long."
            )
        return description


class UserRolForm(forms.ModelForm):
    """
    Custom form for UserRol model with validations to prevent duplicate role assignments for a user.
    """

    class Meta:
        model = UserRol
        fields = ["user", "rol", "active"]

    def clean(self):
        """
        General validation to ensure a user is not assigned the same role multiple times.

        Raises:
            ValidationError: If the user already has the selected role assigned.
        """
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        rol = cleaned_data.get("rol")

        if user and rol:
            existing_roles = UserRol.objects.filter(user=user, rol=rol)
        if self.instance.pk:
            existing_roles = existing_roles.exclude(pk=self.instance.pk)
        if existing_roles.exists():
            raise ValidationError("This user is already assigned the selected role.")

        return cleaned_data

    def clean_active(self):
        """
        Additional validation for the 'active' field if needed.

        Returns:
            bool: The active status of the role assignment.
        """
        active = self.cleaned_data.get("active")
        return active


class UserForm(forms.ModelForm):
    """
    Custom form for the User model with standard fields and validations.
    Ensures unique email addresses and validates required fields.
    """

    class Meta:
        model = User
        fields = ["email", "username", "status", "password", "is_active"]

    def clean_email(self):
        """
        Validate that the email address is unique.

        Raises:
            ValidationError: If the email is already used by another user.

        Returns:
            str: The cleaned email data.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                "A user with this email already exists. Please use a different email."
            )
        return email

    def clean_status(self):
        """
        Validate that the 'status' field is not empty.

        Raises:
            ValidationError: If the status is empty or invalid.

        Returns:
            str: The cleaned status data.
        """
        status = self.cleaned_data.get("status")
        if not status:
            raise ValidationError(
                "Status cannot be blank. Please provide a valid status."
            )
        return status

    def clean_password(self):
        """
        Validate and hash the password if it's a new user or if it's being updated.

        Returns:
            str: The hashed password.
        """
        password = self.cleaned_data.get("password")
        if password:
            return (
                User.objects.make_random_password()
                if not self.instance.pk
                else password
            )
        return password

    def save(self, commit=True):
        """
        Override the save method to ensure passwords are hashed.

        Parameters:
            commit (bool): If True, saves the instance to the database.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

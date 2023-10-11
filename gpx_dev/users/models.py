from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

from gpx_routes_backend.settings import AUTH_USER_MODEL


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    nickname_validator = UnicodeUsernameValidator()

    email = models.EmailField(unique=True, blank=False, null=False)
    nickname = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
        help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[nickname_validator],
    )
    birthday = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    objects = UserManager()

    def __str__(self):
        return self.email


class FollowManager(models.Manager):
    def active(self):
        return self.filter(status=Follow.Status.ACTIVE)

    def canceled(self):
        return self.filter(status=Follow.Status.CANCELED)


class Follow(models.Model):
    """Model to represent Following relationships"""

    class Status(models.IntegerChoices):
        CANCELED = 0, "Неактивна"
        ACTIVE = 1, "Активна"

    follower = models.ForeignKey(
        AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE
    )
    followee = models.ForeignKey(
        AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(choices=Status.choices, default=Status.ACTIVE)

    objects = FollowManager()

    class Meta:
        verbose_name = "Following Relation"
        verbose_name_plural = "Following Relationships"
        unique_together = (
            "follower",
            "followee",
        )

    def __str__(self):
        return f"User #{self.follower} follows #{self.followee}"

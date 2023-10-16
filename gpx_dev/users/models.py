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


class User(AbstractUser):
    nickname_validator = UnicodeUsernameValidator()

    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    nickname = models.CharField(max_length=255, verbose_name="Nickname", unique=True)
    birthday = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    objects = UserManager()

    def __str__(self):
        return self.email


class FollowManager(models.Manager):
    pass


class Follow(models.Model):
    """Model to represent Following relationships"""

    follower = models.ForeignKey(
        AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE
    )
    followee = models.ForeignKey(
        AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    objects = FollowManager()

    class Meta:
        verbose_name = "Following Relation"
        verbose_name_plural = "Following Relationships"
        constraints = [
            models.UniqueConstraint(
                fields=("follower", "followee"), name="unique_follow"
            )
        ]

    def __str__(self):
        return f"User #{self.follower} follows #{self.followee}"

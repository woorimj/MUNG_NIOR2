from django.db import models

# from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, user_type, **extra_fields):
        if not extra_fields.get("phone_number"):
            raise ValueError("The phonNumber field must be set")

        user = self.model(user_type=user_type, **extra_fields)
        user.set_password(extra_fields.get("phone_number"))

        # student/teacher id 각각 생성
        if user.user_type == "student":
            last_student = (
                User.objects.filter(user_type="student").order_by("-student_id").first()
            )
            user.student_id = (last_student.student_id + 1) if last_student else 1
        elif user.user_type == "teacher":
            last_teacher = (
                User.objects.filter(user_type="teacher").order_by("-teacher_id").first()
            )
            user.teacher_id = (last_teacher.teacher_id + 1) if last_teacher else 1

        user.save(using=self._db)
        return user

    def create_superuser(self, user_type, **extra_fields):
        user = self.create_user(user_type, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    USER_TYPES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    student_id = models.PositiveIntegerField(default=0, editable=False)
    teacher_id = models.PositiveIntegerField(default=0, editable=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["user_type", "phone_number"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

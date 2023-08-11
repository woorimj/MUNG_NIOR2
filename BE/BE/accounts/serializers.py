from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class StudentSignUpSerializer(serializers.ModelSerializer):
    student_id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["student_id", "username", "phone_number"]
        extra_kwargs = {
            "username": {"required": True},
            "phone_number": {"required": True},
            # "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data["user_type"] = "student"
        user = User.objects.create_user(**validated_data)
        return user


class TeacherSignUpSerializer(serializers.ModelSerializer):
    teacher_id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["teacher_id", "username", "email", "phone_number"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "phone_number": {"required": True},
            # "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data["user_type"] = "teacher"
        user = User.objects.create_user(**validated_data)
        return user


# 공통로그인
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=15)

    def validate(self, data):
        username = data["username"]
        phone_number = data["phone_number"]

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=phone_number,
        )

        if user is None:
            raise serializers.ValidationError("로그인 정보가 올바르지 않습니다.")

        return data

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from .models import UserProfile
from ProductManagement.models import Cart, Wishlist
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)
    phone_number = serializers.CharField(max_length=15, write_only=True)
    address = serializers.CharField(write_only=True)
    password1 = serializers.CharField(
        write_only=True, min_length=8, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number',
                  'address', 'email', 'password1', 'password2']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        profile_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'phone_number': validated_data.pop('phone_number'),
            'address': validated_data.pop('address'),
        }
        user = User.objects.create_user(
            email=validated_data['email'], password=validated_data['password1']
        )
        user_profile = UserProfile.objects.create(user=user, **profile_data)
        Cart.objects.create(user=user_profile)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(
        source='user.created_at', read_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name',
                  'phone_number', 'address', 'created_at']
        read_only_fields = ['created_at']


class UpdateProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'address', 'current_password']

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('current_password')):
            raise serializers.ValidationError(
                {"current_password": "Invalid credentials."}
            )
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        if email and email != instance.user.email:
            if User.objects.filter(email=email).exclude(id=instance.user.id).exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use."}
                )
            instance.user.email = email
            instance.user.save()

        for field in ['phone_number', 'address']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, min_length=8, validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError(
                {"current_password": "Invalid credentials."}
            )
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError(
                {"new_password": "Passwords do not match."}
            )
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist."
            )
        return value


class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True, min_length=8, validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        uidb64 = data.get("uidb64")
        token = data.get("token")
        new_password = data.get("new_password")
        confirm_new_password = data.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                {"new_password": "Passwords do not match."}
            )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError(
                {"user": "Invalid user ID."}
            )

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {"token": "Invalid or expired token."}
            )

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user

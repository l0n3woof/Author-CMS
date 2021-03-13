from rest_framework import serializers
import django.contrib.auth.password_validation as pass_validator
from django.core import exceptions

from .models import *
from .validators import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone = serializers.IntegerField(validators=[validate_phone_field])
    pincode = serializers.IntegerField(validators=[validate_pincode_field])

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        errors = dict() 
        try:
            pass_validator.validate_password(password=data['password'])
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return data

class ContentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    body = serializers.CharField(max_length=300)
    summary = serializers.CharField(max_length=60)
    document = serializers.FileField() 

    class Meta:
        model = Content
        fields = ('title', 'body', 'summary', 'document', 'author')

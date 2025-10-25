from rest_framework import serializers
from task.models import TaskModel
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id','user','title','description','completed','created_at','updated_at']
        read_only_fields = ['id','user','created_at','updated_at']

class AccountSerializers(serializers.ModelSerializer):
    password=serializers.CharField(min_length=8, write_only=True,error_messages={
        "min_length":"password must be atleast 8 character long!"
    })
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','confirm_password']
    
    def validate(self, data):
        if data['password']!=data['confirm_password']:
            raise ValidationError({'confirm_password':"password does not match!"})
        return data
    
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            )
        return user
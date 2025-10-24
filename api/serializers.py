from rest_framework import serializers
from task.models import TaskModel
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskModel
        fields='__all__'

class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            )
        return user




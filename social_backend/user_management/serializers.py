from rest_framework import serializers
from .models import FriendRequest,User



class UserSerializer(serializers.ModelSerializer):
    # phone_number = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = '__all__'
class UserDetailSerializer(serializers.ModelSerializer):
    # phone_number = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ("id","email","name")
    # def validate(self, data):
    #     data = super().validate(data)
    #     email = data.get("email")
    #     try:
    #         User.objects.get(email = email)
    #         raise serializers.ValidationError({"email":"user with this email already exist"})
    #     except User.DoesNotExist:
    #         pass  
    #     return data

# serializers.py


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserDetailSerializer()
    receiver = UserDetailSerializer()
    class Meta:
        model = FriendRequest
        fields = ('__all__')

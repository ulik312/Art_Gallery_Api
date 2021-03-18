from rest_framework import serializers

from account.models import MyUser


class FanSerializer(serializers.ModelSerializer):


    class Meta:
        model = MyUser
        fields = ('username', 'email')

        def get_username(self,obj):
            return obj.get_username()
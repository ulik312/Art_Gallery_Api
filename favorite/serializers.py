from rest_framework import serializers

from favorite.models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['post'] = instance.post.title
        return representation
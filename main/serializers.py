from rest_framework import serializers

from .models import *
from likes import services as likes_services

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'author', 'created_at', 'text', 'is_fan')

    def get_is_fan(self, obj):
        user = self.context.get('request').user
        print(user)
        return likes_services.is_fan(obj, user)



    def to_representation(self, instance):
        action = self.context.get('action')
        fields = super().get_fields()
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data

        return representation


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)

        else:
            url = ''
        return url



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post_id')
        ratings = validated_data.get('rating')
        rating = Rating.objects.get_or_create(author=user, post_id=post)[0]
        rating.rating = ratings
        rating.save()
        return rating

    def to_representation(self, instance):
        action = self.context.get('action')
        representation = super().to_representation(instance)
        representation['user'] = instance.author.email
        if action == 'retrieve':
            recomendation = Post.objects.filter(title__icontains=instance.title)
            recomendation_ = []
            for rec in recomendation:
                recomendation_.append(rec.title)
            representation['recomendation'] = f"{recomendation_}"
        return representation
        return representation


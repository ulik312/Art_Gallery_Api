from comment.models import Comments
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Comments
        fields = ('post', 'body', 'created', 'author')

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        # validated_data['author_id'] = user_id
        comment = Comments.objects.create(**validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation

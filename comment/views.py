from django.shortcuts import render
from rest_framework import viewsets

from comment.models import Comments
from comment.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

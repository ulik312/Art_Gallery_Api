from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favorite.models import Favourite
from favorite.serializers import FavouriteSerializer


class FavoriteMIxin:


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favourite(self, request, pk=None):
        post = self.get_object()
        obj, created = Favourite.objects.get_or_create(user=request.user, post=post, )
        if not created:
            obj.favourite = not obj.favourite
            obj.save()
        favourites = 'added to favorites' if obj.favourite else 'removed to favorites'

        return Response('Successfully {} !'.format(favourites), status=status.HTTP_200_OK)




    @action(detail=False, methods=['get'])
    def favourites(self, request):
        queryset = Favourite.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = FavouriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

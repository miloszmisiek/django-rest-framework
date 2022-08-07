# from django.http import Http404
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django.db.models import Count
from rest_framework import generics, filters #, permissions
from django_filters.rest_framework import DjangoFilterBackend #third-party library django-filter
from .models import Profile
from .serialaziers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """

    serializer_class = ProfileSerializer
    # annotate method allows to add specific fields to the queryset
    # distinct = true allows to limit the query to unique set, no duplicates
    # 'owner__xyz' reletes to the db releted to common table i.e. profile-user-follower(used with releted names!) or profile-user-post
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        # profiles that are following the profile given its id
        'owner__following__followed__profile',
        # get all profiles that are followed by a profile, given its id
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    # def get(self, request):
    #     profiles = Profile.objects.all()
    #     serializer = ProfileSerializer(
    #         profiles, many=True, context={'request': request}
    #     )
    #     return Response(serializer.data)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')

    # def get_object(self, pk):
    #     try:
    #         profile = Profile.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, profile)
    #         return profile
    #     except Profile.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     profile = self.get_object(pk)
    #     serializer = ProfileSerializer(
    #         profile, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     profile = self.get_object(pk)
    #     serializer = ProfileSerializer(
    #         profile, data=request.data, context={'request': request}
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
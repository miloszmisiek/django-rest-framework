from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend #third-party library django-filter
from .models import Post
from .serializers import PostsSerializer
from drf_api.permissions import IsOwnerOrReadOnly



class PostList(generics.ListCreateAPIView):
    serializer_class = PostsSerializer # renders nice looking form in the UI
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ] # it will hide the post method if user in not logged in
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        # user post feed by their profile id (including posts from users the user is following)
        # post owner is John -> refer to his instance in User model -> check who is following John in Follower model -> refer to following user by User instance -> point out to profile owner of following user
        'owner__followed__owner__profile',
        # passing user id filter his liked posts
        'likes__owner__profile', 
        # user posts that he created based on passed profile id
        'owner__profile'
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]

    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostsSerializer(
    #         posts, many=True, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = PostsSerializer(
    #         data=request.data, context={'request': request}
    #     )
    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(
    #             serializer.data, status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostsSerializer # renders nice looking form in the UI
    permission_classes = [IsOwnerOrReadOnly] #only post owner can edit or delete post
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    # def get_object(self, pk):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, post) # check if reqeuested user has permission to edit or delete the post
    #         return post
    #     except Post.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     post = self.get_object(pk) # to get post you must call your won permission method to handle the DoesNotExist
    #     serializer = PostsSerializer(
    #         post, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostsSerializer(
    #         post, data=request.data, context={'request': request}
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )
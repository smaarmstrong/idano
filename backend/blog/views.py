from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost
from .serializer import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Ensure only authenticated users can access these views

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # Debugging line
        serializer.is_valid(raise_exception=True)
        blog_post = serializer.save(
            author=request.user
        )  # Set the author to the current user
        return Response(
            {"message": "Blog post created successfully.", "id": blog_post.id},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"message": "Blog post retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            print(serializer.errors)  # Debugging line
        serializer.is_valid(raise_exception=True)
        blog_post = serializer.save()
        return Response(
            {"message": "Blog post updated successfully.", "id": blog_post.id},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Blog post deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

from django.http import Http404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter
from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError as MessageError
from rest_framework import status
from .models import Post, Tags, Comment
from .serializers import ListPostSerializer, ListTagsSerializer, CreatePostSerializer, ListCommentSerializer, CreateCommentSerializer
from fakeapirest.pagination_custom import CustomPagination
from fakeapirest.message_response import (
    message_response_no_content,
    message_response_list,
    message_response_bad_request,
    message_response_created,
    message_response_detail,
    message_response_delete,
    message_response_update
)

class ListTagsView(ListAPIView):

    serializer_class = ListTagsSerializer
    queryset = Tags.objects.all()

    def get(self, request, format=None):

        tags = self.get_queryset()

        if not tags.exists():

            return Response(message_response_no_content("tags"), status.HTTP_204_NO_CONTENT)
        
        serializer = self.get_serializer(tags, many=True)

        return Response(message_response_list(serializer.data, tags.count(), "tags"), status.HTTP_200_OK)
    
class ArrayTagsView(ListTagsView):

    def get(self, request, format=None):

        tags = Tags.objects.values_list("slug")
        tags_list = []

        for tag in tags:

            tags_list.append(tag[0])

        return Response(tags_list)

class ListCreatePostView(ListCreateAPIView):

    queryset = Post.objects.all()
    pagination_class = CustomPagination
    limit_queryset = True
    filter_backends = (OrderingFilter,)
    ordering_fields = ("id_post", "title")
    ordering = ("title",)

    def get_queryset(self):

        queryset = self.queryset
        limit = self.request.query_params.get('limit')
        skip = self.request.query_params.get('skip')
        sort_by = self.request.query_params.get('sortBy')
        order = self.request.query_params.get('order')

        if sort_by and order:

            if order == 'desc':
                sort_by = '-' + sort_by
            try:
                queryset = self.queryset.order_by(sort_by)
            except FieldError:
                raise MessageError({"status_code": 404, "message": "La columna que ingresaste no existe"}, status.HTTP_404_NOT_FOUND)

        try:

            skip = 0 if skip is None else int(skip)

            if limit is not None:
                queryset = queryset[:skip + int(limit)]

            if skip is not None:
                queryset = queryset[int(skip):]

        except ValueError:
            raise MessageError({"status_code": 400, "message": "El limite o el skip tiene que ser de tipo numerico"},
                                status.HTTP_400_BAD_REQUEST)
        
        return queryset

    def get(self, request, format=None):

        posts = self.get_queryset()
        
        if not posts.exists():

            return Response(message_response_no_content("posts"), status.HTTP_204_NO_CONTENT)
        
        page_list = self.paginate_queryset(posts)
        serializer = ListPostSerializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):

        serializer = CreatePostSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(message_response_bad_request("post", serializer.errors, "POST"), status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(message_response_created("post", serializer.data), status.HTTP_201_CREATED)

class SearchPostView(ListAPIView):

    serializer_class = ListPostSerializer
    pagination_class = CustomPagination

    def get(self, request, format=None):

        title_post = self.request.query_params.get("title")
        posts = Post.objects.filter(Q(title__icontains=title_post))
        page_list = self.paginate_queryset(posts)
        serializer = self.get_serializer(page_list, many=True)
        
        return self.get_paginated_response(serializer.data)


class FilterTagPostView(ListAPIView):

    serializer_class = ListPostSerializer
    pagination_class = CustomPagination

    def get(self, request, tag_slug: str, format=None):

        tag = Tags.objects.filter(slug=tag_slug).first()

        if tag is None:
            return Response({"status_code": 404, "message": "El tag ingresado no existe"}, status.HTTP_404_NOT_FOUND)

        queryset = Post.objects.filter(Q(tag=tag.id_tag))

        page_list = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)
    
class FilterUserPostView(ListAPIView):

    serializer_class = ListPostSerializer
    pagination_class = CustomPagination

    def get(self, request, user: int, format=None):

        queryset = Post.objects.filter(author=user)

        page_list = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)
    
class ListCommentsPostView(ListAPIView):

    serializer_class = ListCommentSerializer
    pagination_class = CustomPagination

    def get(self, request, id_post: int, format=None):

        post = Post.objects.filter(id_post=id_post).first()

        if post is None:
            return Response({"status_code": 404, "message": "Post no encontrado"}, status.HTTP_404_NOT_FOUND)

        queryset = Comment.objects.filter(post=post.id_post)

        if len(queryset) == 0:
            return Response({"status_code": 204, "message": "Este post no tiene comentarios"}, status.HTTP_204_NO_CONTENT)

        page_list = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)
    
class DetailPostView(RetrieveUpdateDestroyAPIView):

    def get_object(self, id: int):

        try:
            post = Post.objects.get(id_post=id)
        except Post.DoesNotExist:
            raise Http404

        return post
    
    def get(self, request, id: int, format=None):

        post = self.get_object(id)
        serializer = ListPostSerializer(post)

        return Response(message_response_detail(serializer.data), status.HTTP_200_OK)
    
    def put(self, request, id: int, format=None):

        post = self.get_object(id)
        serializer = CreatePostSerializer(post, data=request.data)

        if not serializer.is_valid():
            
            return Response(message_response_bad_request("post", serializer.errors, "PUT"), status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(message_response_update("post", serializer.data), status.HTTP_205_RESET_CONTENT)
    
    def delete(self, request, id: int, format=None):

        post = self.get_object(id)
        post.delete()

        return Response(message_response_delete("post"), status.HTTP_204_NO_CONTENT)


class ListCreateCommentsView(ListCreateAPIView):

    pagination_class = CustomPagination
    queryset = Comment.objects.all()
    limit_queryset = True
    filter_backends = (OrderingFilter,)
    ordering_fields = ("id_comment", "likes")
    ordering = ("id_comment",)

    def get_queryset(self):

        queryset = self.queryset
        limit = self.request.query_params.get('limit')
        skip = self.request.query_params.get('skip')
        sort_by = self.request.query_params.get('sortBy')
        order = self.request.query_params.get('order')

        if sort_by and order:

            if order == 'desc':
                sort_by = '-' + sort_by
            try:
                queryset = self.queryset.order_by(sort_by)
            except FieldError:
                raise MessageError({"status_code": 400, "message": "La columna que ingresaste no existe"}, status.HTTP_404_NOT_FOUND)

        try:

            skip = 0 if skip is None else int(skip)

            if limit is not None:
                queryset = queryset[:skip + int(limit)]

            if skip is not None:
                queryset = queryset[int(skip):]

        except ValueError:
            raise MessageError({"status_code": 400, "message": "El limite o el skip tiene que ser de tipo numerico"},
                                status.HTTP_400_BAD_REQUEST)
        
        return queryset

    def get(self, request, format=None):

        comments = self.get_queryset()

        if not comments.exists():
            return Response(message_response_no_content("comments"), status.HTTP_204_NO_CONTENT)
        
        page_list = self.paginate_queryset(comments)
        serializer = ListCommentSerializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):

        serializer = CreateCommentSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(message_response_bad_request("comment", serializer.errors, "POST"), status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(message_response_created("comment", serializer.data), status.HTTP_201_CREATED)
    
class FilterCommentPostView(ListAPIView):

    serializer_class = ListCommentSerializer
    pagination_class = CustomPagination

    def get(self, request, id_post: int, format=None):

        post = Post.objects.filter(id_post=id_post).first()

        if post is None:
            return Response({"status_code": 404, "message": "Post no encontrado"}, status.HTTP_404_NOT_FOUND)
        
        queryset = Comment.objects.filter(post=post.id_post)

        if len(queryset) == 0:
            return Response({"status_code": 204, "message": "Este post no tiene comentarios"}, status.HTTP_204_NO_CONTENT)
        
        page_list = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_list, many=True)

        return self.get_paginated_response(serializer.data)
    
class DetailCommentView(RetrieveUpdateDestroyAPIView):

    def get_object(self, id: int):

        comment = Comment.objects.filter(id_comment=id).first()

        return comment
    
    def get(self, request, id: int, format=None):

        comment = self.get_object(id)

        if comment is None:

            return Response({"status_code": 404, "message": "Comentario no encontrado"}, status.HTTP_404_NOT_FOUND)

        serializer = ListCommentSerializer(comment)

        return Response(message_response_detail(serializer.data), status.HTTP_200_OK)
    
    def update(self, request, id: int, format=None):

        comment = self.get_object(id)
        serializer = CreateCommentSerializer(comment, data=request.data)

        if not serializer.is_valid():
            return Response(message_response_bad_request("comment", serializer.errors, "PUT"), status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(message_response_update("comment", serializer.data), status.HTTP_205_RESET_CONTENT)
    
    def delete(self, request, id: int, format=None):

        comment = self.get_object(id)
        comment.delete()

        return Response(message_response_delete("comment"), status.HTTP_204_NO_CONTENT)

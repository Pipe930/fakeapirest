from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from .models import Comment, Post, Tags
from django.contrib.auth import get_user_model
User = get_user_model()

class ListTagsSerializer(ModelSerializer):

    class Meta:

        model = Tags
        fields = (

            "id_tag",
            "name",
            "slug",
            "description"
        )

class ListPostSerializer(ModelSerializer):

    reactions = SerializerMethodField(method_name="get_reactions")
    author = StringRelatedField()
    tag = StringRelatedField()

    class Meta:

        model = Post
        fields = (
            "id_post",
            "title",
            "reactions",
            "body",
            "views",
            "author",
            "tag"
        )

    def get_reactions(self, post: Post):

        return {

            "likes": post.likes,
            "dislikes": post.dislikes
        }

class CreatePostSerializer(ModelSerializer):

    class Meta:

        model = Post
        fields = (
            "title",
            "likes",
            "dislikes",
            "body",
            "views",
            "author",
            "tag"
        )

class UserCommentSerializer(ModelSerializer):

    fullname = SerializerMethodField(method_name="get_fullname")

    class Meta:

        model = User
        fields = (
            "id",
            "username",
            "fullname"
        )

    def get_fullname(self, user):

        return user.first_name + " " + user.last_name
    
class ListCommentSerializer(ModelSerializer):

    user = UserCommentSerializer(many=False)

    class Meta:

        model = Comment
        fields = (
            "id_comment",
            "body",
            "likes",
            "post",
            "user"
        )

class CreateCommentSerializer(ModelSerializer):

    class Meta:

        model = Comment
        fields = (
            "body",
            "likes",
            "post",
            "user"
        )

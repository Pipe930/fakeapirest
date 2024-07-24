from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from .models import Comment, Post, Tags

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
    
class ListCommentSerializer(ModelSerializer):

    user = StringRelatedField()

    class Meta:

        model = Comment
        fields = (
            "id_comment",
            "body",
            "likes",
            "post",
            "user"
        )

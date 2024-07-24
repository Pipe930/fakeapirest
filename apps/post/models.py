from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Tags(models.Model):

    id_tag = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True)
    slug = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:

        db_table = "tag"
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name
    

class Post(models.Model):

    id_post = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:

        db_table = "post"
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title
    
class Comment(models.Model):

    id_comment = models.BigAutoField(primary_key=True)
    body = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        db_table = "comment"
        verbose_name = "comment"
        verbose_name_plural = "comments"

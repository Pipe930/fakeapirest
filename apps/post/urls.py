from django.urls import path
from .views import (
    ListCreatePostView, 
    ListTagsView, 
    ArrayTagsView, 
    FilterTagPostView, 
    FilterUserPostView, 
    SearchPostView, 
    DetailPostView,
    ListCommentsPostView,
    ListCreateCommentsView,
    DetailCommentView,
    FilterCommentPostView
)

urls_posts = [
    path("", ListCreatePostView.as_view(), name="listcreatepost"),
    path("search", SearchPostView.as_view(), name="searchpost"),
    path("tags", ListTagsView.as_view(), name="listtags"),
    path("tags-list", ArrayTagsView.as_view(), name="arraytags"),
    path("tag/<str:tag_slug>", FilterTagPostView.as_view(), name="filtertagpost"),
    path("user/<int:user>", FilterUserPostView.as_view(), name="filteruserpost"),
    path("post/<int:id>", DetailPostView.as_view(), name="detailupdatedeletepost"),
    path("comments/post/<int:id_post>", ListCommentsPostView.as_view(), name="listcommentspost")
]

urls_comments = [

    path("", ListCreateCommentsView.as_view(), name="listcomments"),
    path("comment/<int:id>", DetailCommentView.as_view(), name="detailupdatedeletecomment"),
    path("post/<int:id_post>", FilterCommentPostView.as_view(), name="filtercommentpost")
]

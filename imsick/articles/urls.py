from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path("", views.PostListAPIView.as_view(), name="post_list"),
    path("<int:post_pk>/", views.PostDetailAPIView.as_view(),name="post_detail"),
    path("<int:post_pk>/comment/", views.CommentListAPIView.as_view(),name="comment_list_create"),
    path("<int:post_pk>/comment/<int:comment_pk>/", views.CommentListAPIView.as_view(),name="comment_reply"),
    path("comment/<int:comment_pk>/", views.CommentDetailAPIView.as_view(),name="comment_edit_delete_like"),
    path("search/", views.search, name="search"),
    path("list/", views.list, name="list"),
    path("main/", views.main, name="main"),
    path("datathrow/", views.datathrow, name="datathrow"),
    path("post/", views.post, name="post"),
]
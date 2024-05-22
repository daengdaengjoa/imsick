from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Article, Like, Comment
from .serializers import ArticleSerializer, LikeSerializer


class HospitalAPIView(APIView):
    # 로그인 상태
    permission_classes = [IsAuthenticated]

    # 게시물 전체 조회
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시물 생성
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP.201_CREATED)
        return Response(serializer.errors, status=status.HTTP.400_BAD_REQUEST)
    

class HospitalDetailAPIView(APIView):
    #로그인 상태
    permission_classes = [IsAuthenticated]

    #게시물 상세조회
    def get(self,request,pk):
        article = get_object_or_404(Article, article_id=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    #게시물 수정
    def put(self,request, pk):
        article = get_object_or_404(Article, article_id=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP.400_BAD_REQUEST)

    #게시물 삭제
    def delete(self, request, pk):
        article = get_object_or_404(Article, article_id=pk)
        article.delete()
        return Response(status=status.HTTP_204_NOT_CONTENT)
    
    #댓글 생성
    def post(self, request, article_id):
        article = self.get_article(article_id)
        content = request.data.get("content")

        if not content:
            return Response({"error": "content is required"}, status=stauts.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(
            content=content,
            article=article,
            author=request.account,
        )
        return Response({
            "id": comment.id,
            "article": comment.article.id,
            "author": comment.author.id,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)


class LikeAPIView(APIView):
    #로그인 상태
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        

        if request.account in article.like.all():
            article.likes.remove(request.account)
            return Response("Cancled Like.", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.account)
            return Response("Thanks Like.", status=status.HTTP_200_OK)
        # account = request.account

        # if Like.objects.filter(account=account, article=article).exists():        
        #     return Response({"message": "You have already liked this host."}, status=status.HTTP_400_BAD_REQUEST)
        # Like.objects.create(account=account, article=article)
        # return Response({"message": "This post liked."}, status=status.HTTP_201_CREATED)
    
    # def delete(self, request, article_id):
    #     article = get_object_or_404(Article, id=article_id)
    #     account=request.account
        
    #     like = Like.objects.filter(account=account, article=article).first()

class CommentAPIView(APIView):
    #로그인 상태
    permission_classes = [IsAuthenticated]
    
    def get_comment(self, comment_id):
        return get_object_or_404(Comment, id=comment_id)
    def post(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")

        if content is None:
            return Response({"error": "content is required"}, status-status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(
            content=content,
            parent_comment=comment,
            author=request.account
        )
        return Response({
            "id": comment.id,
            "parent_comment": comment.parent_comment.id
            "author": comment.author.id,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)

    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")

        if request.account != comment.author:
            return Response({"error": "permission denied"}, stauts=status.HTTP_403_FORBIDDEN)
        
        if content is None:
            return Response({"error": "content is required"}, stauts=status.HTTP_400_BAD_REQUEST)
        
        comment.content=content
        comment.save()

        return Response({"message": "comment update successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        comment = self.get_comment(comment_id)

        if request.account != comment.author:
            return Response({"error": "permission denied"}, stauts=status.HTTP_403_FORBIDDEN)
        
        comment.delete()

        return Response({"message": "comment delete successfully"}, status=status.HTTP_204_NO_CONTENT)
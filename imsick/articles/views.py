from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer


class HospitalAPIView(APIView):
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
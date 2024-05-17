from rest_framework import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer

from django.shortcuts import render


# Create your views here.

class HospitalAPIView(APIView):
    #게시물 전체 조회
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #게시물 생성
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP.201_CREATED)
        return Response(serializer.errors, status=status.HTTP.400_BAD_REQUEST)
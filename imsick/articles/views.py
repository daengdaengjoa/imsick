from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from openai import OpenAI



class HospitalAPIView(APIView):
    # 게시물 전체 조회
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시물 생성
    def post(self, request):

        # 제목 추출
        title = request.data.get('title')
        
        # 내용 생성
        content = generate_content_from_title(title)

        # 데이터에 제목과 내용 추가
        request.data['content'] = content
        
        # Serializer 생성
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def generate_content_from_title(title):
    # OpenAI API를 사용하여 영화 추천 내용 생성
    client = OpenAI(api_key="")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": "역할: 의사, 역할: 의사, 작업: 아픈 증상을 기반으로 진단 내용과 병명을 제공합니다. 어떤 진료과를 가야하는지 추천합니다.",
            },
            {"role": "user", "content": title},
        ],
    )
    # 대화에서 시스템의 응답을 추출하여 반환
    print(response.choices[0].message.content)
    system_response = response.choices[0].message.content
    return system_response

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
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #게시물 삭제
    def delete(self, request, pk):
        article = get_object_or_404(Article, article_id=pk)
        article.delete()
        return Response(status=status.HTTP_204_NOT_CONTENT)

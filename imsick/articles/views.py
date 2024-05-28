from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from openai import OpenAI
from django.db.models import Q


def set_category(instance):
    if instance.is_staff:
        return "admin"
    else:
        return "review"


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        author = request.user
        
        # 질문 추출
        content = request.data.get('content')
        
        # 내용 생성
        content_ai = generate_content(content)

        # 데이터에 내용 추가
        request.data['content_ai'] = content_ai

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=author, category=set_category(author))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        
        
class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, post_pk):
        return get_object_or_404(Post, id=post_pk)

    def get(self, request, post_pk):
        post = self.get_object(post_pk)
        post.view_count += 1  #조회수
        post.save()        
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    
    def post(self, request, post_pk):
        post = self.get_object(post_pk)
        user = request.user
        if user in post.like_users.all():
            post.like_users.remove(user)
            post.like_counts -= 1
            post.save()
            return Response("좋아요", status=status.HTTP_200_OK)
        else:
            post.like_users.add(user)
            post.like_counts += 1
            post.save()
            return Response("좋아요 완료 다시누르면 좋아요x", status=status.HTTP_201_CREATED)
    
    def put(self, request, post_pk):
        post = self.get_object(post_pk)
        if post.author == request.user:
            serializer = PostDetailSerializer(
                post, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, post_pk):
        post = self.get_object(post_pk)
        if post.author == request.user:
            post.delete()
            data = {"pk": f"{post_pk} is deleted."}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        



class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, post_pk, comment_pk=None):
        author = request.user
        print(author)
        post = get_object_or_404(Post, pk=post_pk)
        if comment_pk:
            comment = get_object_or_404(Comment, pk=comment_pk)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=author, post_id=post, is_reply=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=author, post_id=post, is_reply=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            

        
class CommentDetailAPIView(APIView):
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, id=comment_pk)

    def post(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        user = request.user
        if user in comment.like_comments.all():
            comment.like_comments.remove(user)
            comment.like_counts -= 1
            comment.save()
            return Response("좋아요", status=status.HTTP_200_OK)
        else:
            comment.like_comments.add(user)
            comment.like_counts += 1
            comment.save()
            return Response("좋아요x", status=status.HTTP_201_CREATED)
        
    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.author == request.user:
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.author == request.user:
            comment.delete()
            data = {"pk": f"{comment_pk} is deleted."}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        


@api_view(['GET'])
def search(request):
    print("Search function is called.")  # 함수가 호출되는지 확인
    query = request.GET.get('q')
    if query:
        print("Query:", query)  # 검색어가 올바르게 전달되는지 확인
        results = Post.objects.filter(
            title__icontains=query
        ) | Post.objects.filter(
            content__icontains=query
        ) | Post.objects.filter(
            author__nickname__icontains=query
        )
        serializer = PostSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        print("No query parameter provided.")  # 검색어가 제공되지 않은 경우
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
    
    
def generate_content(content):
    # OpenAI API를 사용하여 영화 추천 내용 생성
    client = OpenAI(api_key="")
    
    prompt = f"""
    당신은 의사입니다. 사용자가 자신의 증상을 설명하면 가능한 진단명과 추천 병원과, 그리고 소견을 제시합니다.

    **사용자:**
    - 주요 증상 (예: 두통, 복통, 발진 등)
    - 증상의 위치 (예: 머리, 복부, 피부 등)
    - 증상의 강도 (예: 경미함, 중간, 심함)
    - 증상이 시작된 시기와 지속 기간
    - 증상을 악화시키거나 완화시키는 요인
    - 기타 관련 증상 (예: 발열, 구토, 피로 등)

    **응답:**
    - 가능한 진단명:
    - 추천 병원과:
    - 소견:

    **예시 입력:**
    - 두통이 3일째 계속되고 있으며, 강도가 점점 심해지고 있습니다. 특히 아침에 일어날 때 더 심합니다. 또한, 목 뒤쪽이 뻣뻣하고, 빛에 민감해졌습니다.

    **예시 출력:**
    - 가능한 진단명: 편두통, 긴장성 두통, 뇌수막염 등
    - 추천 병원과: 신경과 또는 내과
    - 소견: 두통이 지속되고 강도가 증가하는 경우, 특히 목의 뻣뻣함과 빛에 민감한 증상이 동반되는 경우, 이는 심각한 상태일 수 있으므로 빠른 시일 내에 신경과를 방문하는 것이 좋습니다. 필요시 CT나 MRI와 같은 추가 검사가 필요할 수 있습니다.

    **사용자의 입력:**
    {content}

    **응답:**
    """    
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    # 대화에서 시스템의 응답을 추출하여 반환
    print(response.choices[0].message.content)
    system_response = response.choices[0].message.content
    return system_response
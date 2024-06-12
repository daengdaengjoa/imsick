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
import deepl


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        author = request.user

        if author.point < 50:
            return Response({"detail": "포인트가 부족합니다. 게시물을 작성하려면 최소 50포인트가 필요합니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 질문 추출
        content = request.data.get('content')
        
        # 내용 생성
        content_ai = generate_content(content)

        # 데이터에 내용 추가
        request.data['content_ai'] = content_ai
        

        serializer = PostSerializer(data=request.data)
        
        
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save(author=author, category=set_category(author))
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        if serializer.is_valid(raise_exception=True):
            # 게시 여부 설정
            is_published = request.data.get('is_published', False)
            serializer.save(author=author, is_published=is_published)
            author.point -= 50
            # 게시된 경우 점수 추가
            if is_published:
                author.point += 10
                author.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
        
        
class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get_object(self, post_pk):
    #     return get_object_or_404(Post, id=post_pk)
    def get_object(self, post_pk):
        return get_object_or_404(Post, id=post_pk, is_published=True)


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
        post = get_object_or_404(Post, pk=post_pk)
        if comment_pk:
            comment = get_object_or_404(Comment, pk=comment_pk)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=author, post_id=post, is_reply=True, comment_id=comment)
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
    # OpenAI API를 사용하여 내용 생성
    client = OpenAI(api_key="sk-proj-7h7qhkgFqexlYxpwBnGBT3BlbkFJT7NGRBKtBjPIKB4fCuuQ")
    
    auth_key = "37093b85-16f8-4819-982f-455ef40922d3:fx"
    translator = deepl.Translator(auth_key)
    content_tr = translator.translate_text(content, target_lang="EN-US")

    print(content_tr.text)
    
    # 위급 상황 경고 시스템
    emergency_conditions = ["chest pain", "shortness of breath", "severe bleeding"]
    emergency_alert = any(cond in content for cond in emergency_conditions)
    
    prompt = f"""
    You are a doctor. The user describes their symptoms, and you provide possible diagnoses with percentages, recommend hospitals with percentages, and give your opinion.

    **User:**
    - Main symptoms (e.g., headache, abdominal pain, rash)
    - Location of symptoms (e.g., head, abdomen, skin)
    - Severity of symptoms (e.g., mild, moderate, severe)
    - Start and duration of symptoms
    - Factors that worsen or alleviate symptoms
    - Other related symptoms (e.g., fever, vomiting, fatigue)

    **Response:**
    - diagnoses:
    - Recommended hospitals:
    - Opinion:
    - Emergency alert: {"Yes" if emergency_alert else "No"}

    **Example Input:**
    - I have had a headache for 3 days, and the intensity is increasing. It is worse in the morning when I wake up. My neck is stiff, and I have become sensitive to light.

    **Example Output:**
    - diagnoses:
        - Migraine: 60%
        - Tension headache: 30%
        - Meningitis: 10%
    
    - Recommended hospitals: 
        - Neurology: 70%
        - Internal Medicine: 30%
    
    - Opinion: Persistent and worsening headache, especially with neck stiffness and light sensitivity, could be a serious condition. Visiting a neurologist as soon as possible is recommended. Additional tests such as CT or MRI may be needed.
    - Emergency alert: Yes
    
    **User Input:**
    {content_tr.text}

    **Response:**
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    
    print(response.choices[0].message.content)
    
    content_ai = translator.translate_text(response.choices[0].message.content, target_lang="KO")
    print(content_ai)

    system_response = content_ai.text
    return system_response


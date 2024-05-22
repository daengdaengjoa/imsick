# # accounts/views.py
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializers import CustomUserSerializer

# class UserCreateView(APIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "회원가입이 성공적으로 완료되었습니다."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

class UserCreateView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # 사용자를 비활성화 상태로 설정하여 이메일 인증을 기다립니다.
            user.is_active = False
            user.save()
            
            # 이메일 인증 메일 전송
            send_verification_email(request, user)
            
            return Response({"message": "회원가입이 성공적으로 완료되었습니다. 이메일을 확인하여 계정을 활성화하세요."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"http://{get_current_site(request).domain}/verify-email/{uid}/{token}/"
    subject = '이메일 인증 확인'
    message = render_to_string('registration/email_verification.html', {
        'user': user,
        'verification_url': verification_url,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.send()

# accounts/views.py
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponse

class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verification_success')  # 인증 성공 페이지로 리다이렉트
        else:
            return redirect('verification_failed')  # 인증 실패 페이지로 리다이렉트

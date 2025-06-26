# accounts/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from threads.models import Thread
from threads.serializers import ThreadSerializer
from books.serializers import BookSerializer
from books.models import Category
from dj_rest_auth.views import UserDetailsView
from accounts.serializers import UserSimpleSerializer

User = get_user_model()


# 특정 사용자의 프로필 정보를 조회하는 API
@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request, user_login_id):
    user = get_object_or_404(User, username=user_login_id)

    # 사용자가 작성한 스레드 목록
    threads = Thread.objects.filter(user=user)
    thread_serializer = ThreadSerializer(threads, many=True)

    # 사용자가 좋아요를 누른 도서 목록
    liked_books = user.liked_books.all()
    liked_books_serializer = BookSerializer(liked_books, many=True, context={'request': request})

    # 사용자 기본 정보 시리얼라이징
    user_serializer = UserSimpleSerializer(user, context={'request': request})

    return Response({
        'user': user_serializer.data,
        'threads': thread_serializer.data,
        'liked_books': liked_books_serializer.data,
    })


# 로그인한 사용자가 본인의 정보를 수정하는 API
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, user_login_id):
    if request.user.username != user_login_id:
        return Response({'error': '본인만 수정할 수 있습니다.'}, status=403)
    
    serializer = UserSimpleSerializer(
        request.user,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# 로그인한 사용자가 자신의 계정을 삭제하는 API
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete(request, user_login_id):
    if request.user.username != user_login_id:
        return Response({'error': '본인만 탈퇴할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

    request.user.delete()
    return Response({'message': '회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)


# 로그인한 사용자가 다른 사용자를 팔로우/언팔로우하는 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_login_id):
    target_user = get_object_or_404(User, username=user_login_id)

    me = request.user
    if me == target_user:
        return Response({'error': '자기 자신은 팔로우할 수 없습니다.'}, status=400)

    # 팔로우 상태에 따라 추가 또는 제거
    if target_user in me.followings.all():
        me.followings.remove(target_user)
        followed = False
    else:
        me.followings.add(target_user)
        followed = True

    return Response({
        'followed': followed,
        'followers_count': target_user.followers.count(),
        'followings_count': target_user.followings.count(),
        'is_following': followed
    })


# 사용자 기본 정보를 반환하는 View 클래스 (커스텀 시리얼라이저 사용)
class CustomUserDetailsView(UserDetailsView):
    serializer_class = UserSimpleSerializer


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileImageSerializer

# 프로필 이미지 업로드용 API 클래스
class ProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileImageSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

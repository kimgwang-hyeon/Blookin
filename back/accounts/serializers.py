# accounts/serializers.py

from django.contrib.auth import get_user_model
from books.models import Category
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser

User = get_user_model()

# 프로필 이미지 전용 serializer
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_image']


# 회원가입 시 사용되는 serializer
class CustomRegisterSerializer(RegisterSerializer):
    # 성별 필드 (선택 입력, M/F 선택지 제공)
    gender = serializers.ChoiceField(
        choices=[('M', '남성'), ('F', '여성')],
        required=False,
        allow_blank=True
    )
    # 이름 관련 필드 (선택 입력)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    # 이메일 필드 (선택 입력)
    email = serializers.EmailField(required=False, allow_blank=True)
    # 나이 (선택 입력)
    age = serializers.IntegerField(required=False, allow_null=True)
    # 주간 평균 독서 시간 (선택 입력)
    weekly_reading_time = serializers.IntegerField(required=False, allow_null=True)
    # 연간 독서량 (선택 입력)
    yearly_reading_volume = serializers.IntegerField(required=False, allow_null=True)
    # 프로필 이미지 (선택 입력)
    profile_image = serializers.ImageField(required=False)
    # 관심 장르 (카테고리 id 리스트 형태, M:N 관계용)
    interested_genres = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    # 유효성 검증을 마친 데이터를 딕셔너리로 정리하여 반환
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['gender'] = self.validated_data.get('gender', '')
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['email'] = self.validated_data.get('email', '')
        data['age'] = self.validated_data.get('age', 0)
        data['weekly_reading_time'] = self.validated_data.get('weekly_reading_time', 0)
        data['yearly_reading_volume'] = self.validated_data.get('yearly_reading_volume', 0)
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['interested_genres'] = self.validated_data.get('interested_genres', [])
        return data

    # 사용자 객체 저장 로직 정의
    def save(self, request):
        user = super().save(request)

        # 커스텀 필드 수동 할당
        user.gender = self.validated_data.get('gender', '')
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.email = self.validated_data.get('email', '')
        user.age = self.validated_data.get('age', 0)
        user.weekly_reading_time = self.validated_data.get('weekly_reading_time', 0)
        user.yearly_reading_volume = self.validated_data.get('yearly_reading_volume', 0)
        user.profile_image = self.validated_data.get('profile_image', None)
        user.save()

        # 관심 장르(ManyToManyField)는 save 후 별도 처리 필요
        genre_ids = self.validated_data.get('interested_genres', [])
        if genre_ids:
            user.interested_genres.set(genre_ids)

        return user


# 사용자 정보 조회용 serializer
class UserSimpleSerializer(serializers.ModelSerializer):
    # 성 + 이름을 조합한 필드
    full_name = serializers.SerializerMethodField()
    # 관심 장르 이름만 추출하여 리스트로 반환
    interested_genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    # 팔로워 수, 팔로잉 수
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    # 현재 로그인한 사용자가 해당 사용자를 팔로우 중인지 여부
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'gender',
            'age',
            'weekly_reading_time',
            'yearly_reading_volume',
            'profile_image',
            'interested_genres',
            'followers_count',
            'followings_count',
            'is_following',
        ]

    # 성과 이름이 있으면 결합, 없으면 username 사용
    def get_full_name(self, obj):
        if obj.first_name or obj.last_name:
            return f"{obj.last_name}{obj.first_name}".strip()
        return obj.username

    # 팔로워 수 반환
    def get_followers_count(self, obj):
        return obj.followers.count()

    # 팔로잉 수 반환
    def get_followings_count(self, obj):
        return obj.followings.count()

    # 로그인한 사용자가 해당 사용자를 팔로우 중인지 여부 반환
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.followings.all()
        return False

    # 사용자 이름 중복 검증
    def validate_username(self, value):
        request = self.context.get('request')
        if request:
            user = request.user
            if User.objects.exclude(pk=user.pk).filter(username=value).exists():
                raise serializers.ValidationError("이미 존재하는 사용자 이름입니다.")
        return value

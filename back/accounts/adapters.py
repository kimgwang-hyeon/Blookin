# accounts/adapters.py

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    django-allauth의 기본 회원가입 로직에 프로필 이미지 등 커스텀 필드 저장 기능을 추가한 어댑터 클래스
    """

    def save_user(self, request, user, form, commit=True):
        """
        기본 필드 외의 커스텀 필드들을 저장하기 위해 save_user 메서드를 오버라이드함
        super()를 통해 username, email, first_name, last_name 등의 기본 필드를 먼저 저장하고
        그 이후 커스텀 필드(profile_image, gender 등)를 추가로 할당
        """
        user = super().save_user(request, user, form, False)  # 기본 필드만 저장
        data = form.cleaned_data

        # profile_image 필드가 있는 경우 사용자 객체에 할당
        profile_image = data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image

        # gender 필드가 있는 경우 할당
        if hasattr(user, 'gender'):
            user.gender = data.get('gender', '')

        # age 필드가 있는 경우 할당
        if hasattr(user, 'age'):
            user.age = data.get('age', None)

        # weekly_reading_time 필드가 있는 경우 할당
        if hasattr(user, 'weekly_reading_time'):
            user.weekly_reading_time = data.get('weekly_reading_time', None)

        # yearly_reading_volume 필드가 있는 경우 할당
        if hasattr(user, 'yearly_reading_volume'):
            user.yearly_reading_volume = data.get('yearly_reading_volume', None)

        # 커스텀 필드 저장 후 user 객체 저장
        user.save()

        # 관심 장르(interested_genres)는 ManyToMany 필드이므로 save 후 별도로 set 처리
        interested_genres = data.get('interested_genres')
        if interested_genres and hasattr(user, 'interested_genres'):
            user.interested_genres.set(interested_genres)

        return user

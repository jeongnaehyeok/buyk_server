# BuyK_server

2년전 크로컴퍼니 팀에서 진행하였던 BuyK 프로젝트를 다시 만들어보았습니다. 기존에 있던 코드를 최대한 이해하고 공부하면서 구현했습니다. 구현하기 힘들었던 기능 중 몇가지는 제외하거나 대체하여 개발하였습니다.

## 사용한 것

- Django
- Django-REST-framework
- SQLite
- Postman
- Sourcetree

## 제거한 기능

- 좋아요 기능
- 회원정보 변경 및 소셜로그인
- 자동완성 기능
- 인기 검색순위 기능
- 바이크 모델에 따른 타입 브렌드와 모델 선언

## 수정 및 추가한 기능

- django-rest-auth를 이용한 회원가입, 토큰제공
- jwt으로 인증받기
- 접근권한 추가
- 매물 삭제기능

## 공부하게 된것

- User 관련
  - [Jwt 인증](https://jpadilla.github.io/django-rest-framework-jwt/)
  - [django-rest-auth을 이용한 회원가입](https://django-rest-auth.readthedocs.io/en/latest/installation.html)
  - [로그인 관련 권한](https://django-allauth.readthedocs.io/en/latest/configuration.html)
  - [User Model](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/)
- Model 관련
  - [ForeignKey 설정](https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_one/)
  - [유효값 설정](https://docs.djangoproject.com/en/3.0/ref/validators/)
  - [Django ORM]([https://medium.com/@chrisjune_13837/django-%EB%8B%B9%EC%8B%A0%EC%9D%B4-%EB%AA%B0%EB%9E%90%EB%8D%98-orm-%EA%B8%B0%EC%B4%88%EC%99%80-%EC%8B%AC%ED%99%94-592a6017b5f5](https://medium.com/@chrisjune_13837/django-당신이-몰랐던-orm-기초와-심화-592a6017b5f5))

## 실행

```python
# 패키지 설치
$ pip install -r requirements.txt
# 마이그래이션
$ python manage.py makemigrations
$ python manage.py migrate
# 실행
python manage.py runserver 127.0.0.1:8000
```

## 추가 하고 싶은 기능

- django-allauth를 이용한 소셜로그인
- Like기능
- User 모델 변경

## 후기

2년전 기술스택 부족으로 인해 만들지 못했던 BuyK 웹 클라이언트 개발을 위해 API 서버를 만들게 되었습니다. 기존에 있던 코드를 계속 읽어보면서 최대한 이해하고 구현해보려고 노력해봤습니다. 기존에는 단위별로 코드를 읽고 이해했다면 서비스를 위한 짜여진 코드를 이해하는 것은 거의 처음이었습니다. 전체코드의 80%를 이해하는데 하루정도 소요가 된거 같습니다. 기존에 개발을 하면서 어떻게 구현될까 궁금하던 코드들을 직접보니 신기하고 더 열심히 공부 해야겠다고 느꼈습니다. 

구현에 앞서서 기존 코드에서 자체적으로 구현하였던 User에 관한 문제(회원가입을 하고 토큰을 지급해주는 문제)를 어떻게 해결을 할까 고민이 많았습니다. 그래서 레퍼런스를 찾던 도중에 `django-rest-auth`를 이용한 회원가입과 토큰 제공에 대한 문제를 해결하게 되었습니다. 

구현을 하면서 가장 중점적으로 추가했던 부분은 회원 정보에 따라 API 동작이었습니다. 기존에 있던 코드에는 비인증 사용자가 API에 접근하여 이미지를 만드는 것이 가능했습니다. 이러한 문제를 해결하고자 `User Model`과 `request`의 문서를 참고하여서 해결을 했습니다.

```python
# bikes/views.py
...
class BikeImageCreate(generics.CreateAPIView):
  ...
  def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise exceptions.PermissionDenied('로그인이 필요합니다.')
        if not bool(self.request.user.bike_set.all().filter(id=self.request.data['bike'])):
            raise exceptions.PermissionDenied('해당 매물을 수정 할 권한이 없습니다.')
        try:
            return serializer.save()
        except IntegrityError:
            raise exceptions.ValidationError("잘못된 형식입니다.")
...
```


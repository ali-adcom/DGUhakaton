from django.contrib.auth import login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin

from common.serializers import EmailSerializer
from users.models import User
from users.serializers import UserSerializer, UserSignUpSerializer
from users.services import get_otp_for_email, check_otp


class UserViewSet(
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'], url_path='auth/send-otp', serializer_class=EmailSerializer)
    def send_otp(self, request, *args, **kwargs):
        """
            Отправка otp на почту
            Body:
                - email: почта, на которую нужно отправить otp
            Response:
                - 200: otp успешно отправлен
                - 500: ошибка при отправке otp
        """
        email = request.data.get('email')

        serializer = EmailSerializer(data={'email': email})
        serializer.is_valid(raise_exception=True)

        if not email:
            return Response(data='Email не указан', status=status.HTTP_400_BAD_REQUEST)

        otp = get_otp_for_email(email)

        return Response(f'otp успешно отправлен {otp}')

    @action(detail=False, methods=['POST'], url_path='auth/sign-up', serializer_class=UserSignUpSerializer)
    def sign_up(self, request, *args, **kwargs):
        """
            Регистрация пользователя.
            Сперва проходит проверка на корректность otp, если он верен, регистрация проходит дальше.
            Если пользователь с таким email уже есть, возвращает его, иначе нет
            Body:
                - email: почта, на которую нужно отправить otp
            Response:
                - 200: Пользователь успешно зарегистрирован
                - 400: Данные для создания пользователя
                - 403: Не корректный otp
        """
        sign_up_serializer = UserSignUpSerializer(data=request.data)
        sign_up_serializer.is_valid(raise_exception=True)

        email = sign_up_serializer.data.get('email')
        otp = sign_up_serializer.data.get('otp')

        is_otp_valid = check_otp(email, otp)
        if not is_otp_valid:
            return Response('otp не корректен', status=status.HTTP_403_FORBIDDEN)

        user_serializer = UserSerializer(data=sign_up_serializer.data)
        user_serializer.is_valid()

        try:
            user = User.objects.get_or_create(email=email, defaults=user_serializer.data)[0]
            user_serializer = UserSerializer(user)

            login(request, user)

            return Response(user_serializer.data)
        except Exception as e:
            return Response(
                'Возникла ошибка при создании/получении пользователя', status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

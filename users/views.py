from django.contrib.auth import login, logout
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, CreateModelMixin

from common.serializers import EmailSerializer
from users.models import User, FamilyInviteCode, Family
from users.serializers import UserSerializer, UserSignUpSerializer, FamilySerializer, FamilyCreateSerializer, \
    FamilyMemberCreateSerializer
from users.services import get_otp_for_email, check_otp, generate_family_invite_code, send_otp_mail


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
        send_otp_mail(request, otp, email)
        return Response(f'otp успешно отправлен {otp}')

    @action(detail=False, methods=['POST'], url_path='auth/login', serializer_class=UserSignUpSerializer)
    def login_user(self, request, *args, **kwargs):
        """
            Аутентификация пользователя.
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

    @action(detail=False, methods=['POST'], url_path='auth/logout')
    def login_user(self, request, *args, **kwargs):
        logout(request)
        return Response('Успешно')


class FamilyViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return FamilyCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.family:
            return Response({'family': 'Вы уже состоите в семье'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        family = self.get_object()
        members = family.members.all()

        family_serializer = FamilySerializer(family)
        members_serializer = UserSerializer(members, many=True)

        return Response({'family': family_serializer.data, 'members': members_serializer.data})

    @action(detail=False, methods=['POST'], url_path='join-to-family')
    def join_user_to_family(self, request, *args, **kwargs):
        """
            family_invite_code: str
        """
        user = request.user

        if user.is_authenticated and user.family:
            return Response({'family': 'Вы уже состоите в семье'}, status=status.HTTP_400_BAD_REQUEST)

        family_invite_code = request.data.get('family_invite_code')
        if not family_invite_code:
            return Response('family_invite_code не передан', status=status.HTTP_400_BAD_REQUEST)

        family_invite_code_instance = FamilyInviteCode.objects.filter(code=family_invite_code).first()
        if not family_invite_code_instance:
            return Response({'family_invite_code': 'Приглашение с таким кодом не найдено'})

        user.family = family_invite_code_instance.family
        user.save()

        if not user.is_authenticated:
            login(request, family_invite_code_instance.user)

        family_invite_code_instance.delete()

        return Response('Пользователь успешно добавлен в семью')

    @action(detail=True, methods=['POST'], url_path='invite-member', serializer_class=FamilyMemberCreateSerializer)
    def invite_family_member(self, request, pk=None):
        """
            Создание InviteFamilyCode
            Body:
              - 'first_name', 'last_name', 'email', 'role', 'gender', 'age'
            Response:
              - 200: family_invite_code успешно создан
              - 400: некорректные данные пользователя
              - 404: семья не найдена
        """
        user_email = request.data.get('email')
        if not user_email:
            return Response('email не был передан')

        user = User.objects.filter(email=user_email).first()
        if user:
            user_serializer = FamilyMemberCreateSerializer(user)
        else:
            user_serializer = FamilyMemberCreateSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)

        family = self.get_object()

        with transaction.atomic():
            user = user_serializer.save()
            code = generate_family_invite_code(family_id=family.id, user_id=user.id)

            family_invite_code = FamilyInviteCode.objects.create(user=user, family=family, code=code)

        return Response({'family_invite_code': family_invite_code.code})

# crear APIView del modelo
from rest_framework import status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdmin, IsCollaborator
from apps.users.models import User, AcademicProgram, Estudiante, UsuarioBienestar, Gender, DocumentType
from apps.users.api.serializers import UserSerializer, EstudianteSerializer, UsuarioBienestarSerializer, AcademicProgramSerializer, EditUsuarioBienestarSerializer, GenderSerializer, DocumentTypeSerializer, EmailVerificationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, ListUsuarioBienestarSerializer, StudentAcoumulatedHoursSerializer


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.utils.http import urlsafe_base64_encode
# from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

from django.shortcuts import get_object_or_404

# ----------------
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import Util
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics
from django.urls import reverse
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import AllowAny


# def send_activation_email(user, request):
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
#     activation_url = f'{request.scheme}://{request.get_host()}{activation_link}'

#     subject = 'Activa tu cuenta'
#     message = (
#         f'Hola {user.username},\n\n'
#         'Gracias por registrarte en nuestro sitio. Por favor, activa tu cuenta haciendo clic en el siguiente enlace:\n\n'
#         f'{activation_url}\n\n'
#         'Si no solicitaste este registro, ignora este correo.\n\n'
#         'Saludos,\n'
#         'El equipo de soporte'
#     )

#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# @api_view(['GET'])
# def activate_account(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return Response({'message': 'Cuenta activada correctamente'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'Token de activación inválido'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def activate_account(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         return Response({'message': 'El enlace de activación es inválido o el usuario no existe.'}, status=status.HTTP_400_BAD_REQUEST)

#     if user is not None and default_token_generator.check_token(user, token):
#         if not user.is_active:
#             user.is_active = True
#             user.save()
#             return Response({'message': 'Cuenta activada correctamente'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'La cuenta ya está activada.'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'message': 'Token de activación inválido.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_api_view(request):

    if request.method == 'GET':
        # Queryset
        users = User.objects.all()
        # Serializer
        users_serializer = UserSerializer(users, many=True)

        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    # elif request.method == 'POST':
    #     role = request.data.get('role')
    #     if role == 'Estudiante':
    #         print(request.data)
    #         user_serializer = EstudianteSerializer(data=request.data)
    #     elif role == 'Usuario_Bienestar':
    #         user_serializer = UsuarioBienestarSerializer(data=request.data)
    #     else:
    #         user_serializer = UserSerializer(data=request.data)

    #     if user_serializer.is_valid():
    #         print("el usuario el valido")
    #         user = user_serializer.save()

    #         user.is_active = False  # Desactiva la cuenta hasta la activación
    #         user.save()

    #         # Enviar correo de activación
    #         send_activation_email(user, request)
    #         return Response({'message': 'Usuario creado correctamente, Revisa tu correo para activar la cuenta.'}, status=status.HTTP_201_CREATED)
    #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated, IsAdmin])
@permission_classes([AllowAny])
def create_student_api_view(request):
    if request.method == 'GET':
        # Queryset
        users = Estudiante.objects.all()
        # Serializer
        users_serializer = EstudianteSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        estudiante_serializer = EstudianteSerializer(data=request.data)

        if estudiante_serializer.is_valid():
            estudiante = estudiante_serializer.save()
            estudiante.is_active = False  # Desactiva la cuenta hasta que sea activada
            estudiante.save()

            user = User.objects.get(id=estudiante.id)

            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Hola '+user.username+' usa el siguiente link para verificar tu correo \n'+absurl
            data = {'email_body': email_body, 'email_subject': 'Activa tu cuenta', 'to_email': user.email, 'name': user.name}
            Util.send_email(data)

            # Enviar correo de activación
            # send_activation_email(estudiante, request)

            return Response({
                'message': 'Estudiante creado correctamente. Revisa tu correo para activar la cuenta.'
            }, status=status.HTTP_201_CREATED)

        return Response(estudiante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detailStudent_api_view(request, pk=None):
    # Queryset
    user = User.objects.filter(id=pk).first()
    print(user)

    if user:

        if request.method == 'GET':
            # Serializer
            user_serializer = StudentAcoumulatedHoursSerializer(user)
            print(user_serializer.data)
            # return Response(user_serializer.data, status=status.HTTP_200_OK)
            accumulated_hours = Estudiante.objects.get(id=pk).accumulated_hours
            print(accumulated_hours)
            return Response({'accumulated_hours': accumulated_hours}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated, IsAdmin, IsCollaborator])
def create_collaborator_api_view(request):
    permissions = (IsAuthenticated, IsAdmin, IsCollaborator)
    if request.method == 'GET':
        # Queryset
        users = UsuarioBienestar.objects.all()
        # Serializer
        users_serializer = ListUsuarioBienestarSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        print(request.data)
        bienestar_serializer = UsuarioBienestarSerializer(data=request.data)

        if bienestar_serializer.is_valid():
            bienestar = bienestar_serializer.save()
            bienestar.is_verified = True
            bienestar.is_active = True
            bienestar.save()

            # Si no requiere activación por correo
            return Response({
                'message': 'Usuario Bienestar creado correctamente.'
            }, status=status.HTTP_201_CREATED)

        return Response(bienestar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    # Queryset
    user = User.objects.filter(id=pk).first()

    if user:

        if request.method == 'GET':
            # Serializer
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            if user.role == 'Estudiante':
                user_serializer = EstudianteSerializer(user, data=request.data)
            elif user.role == 'Usuario_Bienestar':
                print('Usuario Bienestar')
                print(request.data)
                user_serializer = EditUsuarioBienestarSerializer(instance=user, data=request.data)
            else:
                user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def academic_programs_api_view(request):
    if request.method == 'POST':
        academic_program_serializer = AcademicProgramSerializer(data=request.data)
        if academic_program_serializer.is_valid():
            academic_program_serializer.save()
            return Response(academic_program_serializer.data, status=status.HTTP_201_CREATED)
        return Response(academic_program_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        academic_programs = AcademicProgram.objects.all()
        academic_programs_serializer = AcademicProgramSerializer(academic_programs, many=True)
        return Response(academic_programs_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def genders_api_view(request):

    if request.method == 'POST':
        genders_serializer = GenderSerializer(data=request.data)
        if genders_serializer.is_valid():
            genders_serializer.save()
            return Response(genders_serializer.data, status=status.HTTP_201_CREATED)
        return Response(genders_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        genders = Gender.objects.all()
        genders_serializer = GenderSerializer(genders, many=True)
        return Response(genders_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def document_types_api_view(request):

    if request.method == 'POST':
        document_type_serializer = DocumentTypeSerializer(data=request.data)
        if document_type_serializer.is_valid():
            document_type_serializer.save()
            return Response(document_type_serializer.data, status=status.HTTP_201_CREATED)
        return Response(document_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        document_types = DocumentType.objects.all()
        document_types_serializer = DocumentTypeSerializer(document_types, many=True)
        return Response(document_types_serializer.data, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data = data)
        # serializer.is_valid(raise_exception=True)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            frontend_url = settings.FRONTEND_URL 
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            # absurl = 'http://'+current_site+relativeLink
            # absurl = f'{frontend_url}{relativeLink}'
            absurl = 'http://localhost:5173/auth/password-reset/'+uidb64+'/'+token
            email_body = 'Hola usa el siguiente link para restablecer tu contraseña \n'+absurl
            data = {'email_body': email_body, 'email_subject': 'Restablecer contraseña', 'to_email': user.email, 'name': user.name}
            Util.send_email(data)
        return Response({'success': 'hemos enviado un enlace para restablecer tu contraseña'}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token inválido, por favor solicita un nuevo enlace'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'success': True,
                'message': 'Credenciales válidas',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)
            return Response({'success': True, 'message': 'Credenciales válidas', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token inválido, por favor solicita un nuevo enlace'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as identifier:
            return Response({'error': 'Este usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Contraseña restableciuda correctamente'}, status=status.HTTP_200_OK)
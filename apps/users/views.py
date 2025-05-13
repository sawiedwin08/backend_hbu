from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.authentication_mixins import Authentication
# from apps.users.api.serializers import UserTokenSerializer

# ------------------
from rest_framework import generics
from .serielizers import LoginSerializer, LogoutSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

# class UserToken(Authentication, APIView):

#     def get(self, request, *args, **kwargs):
#         print('Hola desde get UserToken')
#         try:
#             user_token, _ = Token.objects.get_or_create(user = self.user)
#             user = UserTokenSerializer(self.user)
#             return Response({'token': user_token.key, 'user': user.data}, status = status.HTTP_200_OK)
#         except:
#             return Response({'error': 'Credenciales enviadas incorrectas'}, status = status.HTTP_400_BAD_REQUEST)

# class Login(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         login_serializer = self.serializer_class(data = request.data, context = {'request':request})
#         if login_serializer.is_valid():
#             user = login_serializer.validated_data['user']
#             if user.is_active:
#                 token, created = Token.objects.get_or_create(user = user)
#                 user_serializer = UserTokenSerializer(user)
#                 print(user.role)
#                 if created:
#                     return Response({
#                         'token': token.key,
#                         'user': user_serializer.data,
#                         'role': user.role,
#                         'message': 'inicio de sesion exitoso'
#                     }, status = status.HTTP_201_CREATED)
#                 else:
#                     all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
#                     if all_sessions.exists():
#                         for session in all_sessions:
#                             session_data = session.get_decoded()
#                             if user.id == int(session_data.get('_auth_user_id')):
#                                 session.delete()
#                     token.delete()
#                     token = Token.objects.create(user = user)
#                     return Response({
#                         'token': token.key,
#                         'user': user_serializer.data,
#                         'role': user.role,
#                         'message': 'inicio de sesion exitoso'
#                     }, status = status.HTTP_201_CREATED)
#                 # token.delete()
#                 # return Response({
#                 #     'error': 'Ys se ha iniciado sesion con este usuario'
#                 # }, status = status.HTTP_409_CONFLICT)
#             else:
#                 return Response({'error': 'Este usuario no puede iniciar sesion'}, status = status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({'error': 'Usuario o contraseña incorrectos'}, status = status.HTTP_400_BAD_REQUEST)
#         return Response({'mensaje': 'Hola desde response'}, status = status.HTTP_200_OK)

# class Logout(APIView):

#     def get(self, request, *args, **kwargs):
#         try:
#             token = request.GET.get('token')
#             token = Token.objects.filter(key = token).first()
#             if token:
#                 user = token.user
#                 all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
#                 if all_sessions.exists():
#                     for session in all_sessions:
#                         session_data = session.get_decoded()
#                         if user.id == int(session_data.get('_auth_user_id')):
#                             session.delete()
#                 token.delete()
#                 session_message = 'Sesiones de usuario eliminadas.'
#                 token_message = 'Token eliminado.'
#                 return Response({'token_message': token_message, 'session_messge': session_message}, status = status.HTTP_200_OK)
#             return Response({'error': 'No se ha encontrado un usuario con estas credenciales.'}, status = status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({'error': 'No se ha encontrado un token en la peticion.'}, status = status.HTTP_409_CONFLICT)
        
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        print(serializer.data)
        
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(status.HTTP_200_OK)

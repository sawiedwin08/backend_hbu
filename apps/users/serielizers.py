from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.users.models import User

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        usuario = User.objects.filter(username=username).first()
        full_name = f"{usuario.name} {usuario.last_name}"

        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Credenciales incorrectas, intenta nuevamente')
        if not user.is_active:
            raise AuthenticationFailed('Cuenta desactivada, contacta al administrador')
        if not user.is_verified:
            raise AuthenticationFailed('La cuenta no esta verificada')
        return {
            # 'email': user.email,
            'username': full_name,
            'user': usuario,
            'role': user.role,
            'tokens': user.tokens()
        }
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token inválido',
        }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

from rest_framework import serializers
from apps.users.models import User, Estudiante, UsuarioBienestar, AcademicProgram, Gender, DocumentType
from apps.activities.api.serializers.general_serializers import DimensionSerializer

from django.contrib.auth.tokens import  PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

# class UserTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'last_name', 'type_document', 'identification', 'gender', 'password', 'role', 'image', 'is_active', 'is_staff']

    def validate_name(self, value):
        if value == "":
            raise serializers.ValidationError("Error, el nombre no puede estar vacio")
        if len(value) < 3:
            raise serializers.ValidationError("Error, el nombre debe tener al menos 3 caracteres")
        # necesito validar que el nombre no tenga numeros pero si puede tener espacios
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Error, el nombre debe ser alfabetico")
        return value
    
    def validate_last_name(self, value):
        if value == "":
            raise serializers.ValidationError("Error, el apellido no puede estar vacio")
        if len(value) < 3:
            raise serializers.ValidationError("Error, el apellido debe tener al menos 3 caracteres")
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Error, el apellido debe ser alfabetico")
        return value
    
    def validate_type_document(self, value):
        if value == "":
            raise serializers.ValidationError("Error, debe seleccionar un tipo de documento")
        if not DocumentType.objects.filter(name=value).exists():
            raise serializers.ValidationError("Error, el tipo de documento no existe")
        return value
    
    def validate_identification(self, value):
        if value == "":
            raise serializers.ValidationError("Error, la identificacion no puede estar vacia")
        if User.objects.filter(identification=value).exists():
            raise serializers.ValidationError("Error, la identificacion ya existe")
        if value.isdigit() == False:
            raise serializers.ValidationError("Error, la identificacion debe ser numerica")
        if len(value) < 6:
            raise serializers.ValidationError("Error, la identificacion debe tener al menos 6 caracteres")
        if len(value) > 10:
            raise serializers.ValidationError("Error, la identificacion debe tener maximo 10 caracteres")
        return value
    
    def validate_gender(self, value):
        if value == "":
            raise serializers.ValidationError("Error, debe seleccionar un genero")
        return value
    
    def validate_password(self, value):
        if value == "":
            raise serializers.ValidationError("Error, la contraseña no puede estar vacia")
        if len(value) < 8:
            raise serializers.ValidationError("Error, la contraseña debe tener al menos 8 caracteres")
        if len(value) > 16:
            raise serializers.ValidationError("Error, la contraseña debe tener maximo 16 caracteres")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Error, la contraseña debe tener al menos un numero")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Error, la contraseña debe tener al menos una letra")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Error, la contraseña debe tener al menos una letra mayuscula")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Error, la contraseña debe tener al menos una letra minuscula")
        if not any(char in ['$', '#', '@', '&', '%', '!', '.', '+', '-', '*', '/'] for char in value):
            raise serializers.ValidationError("Error, la contraseña debe tener al menos un caracter especial")
        return value    

    def validate_email(self, value):
        print('validacion de correo')
        print(value)
    # Validacion personalizada
        if value == "":
            raise serializers.ValidationError("Error, el email no puede estar vacio")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Error, el correo ya existe")
        if not value.endswith('@campusucc.edu.co') and not value.endswith('@ucc.edu.co'):
            raise serializers.ValidationError("Error, el correo debe ser institucional @campuss.edu.coc")
        # if self.validate_name(self.context['name']) in value:
        #     raise serializers.ValidationError("Error, el nombre no puede estar en el email")
        return value
    
    # def validate_username(self, value):
    #     if value == "":
    #         raise serializers.ValidationError("Error, el usuario no puede estar vacio")
    #     if User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError("Error, el usuario ya existe")
    
    def validate_role(self, value):
        if value == "":
            raise serializers.ValidationError("Error, el rol no puede estar vacio")
        if value not in ['Administrador', 'Estudiante', 'Usuario_Bienestar']:
            raise serializers.ValidationError("Error, el rol no es valido")
        return value

    def create(self, validated_data):
        print(validated_data)
        role = validated_data.get('role')
        email = validated_data.get('email')
        username = email.split('@')[0]
        print(username)
        validated_data['username'] = username
        if role == 'Estudiante':
            validated_data['username'] = username
            user = Estudiante(**validated_data)
        elif role == 'Usuario_Bienestar':
            validated_data['username'] = username
            user = UsuarioBienestar(**validated_data)
        else:
            user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        return super().update(instance, validated_data)
class AcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicProgram
        fields = ['id', 'name', 'code']
class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'code', 'name']
class StudentAcoumulatedHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['accumulated_hours']
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'code', 'name']
class EstudianteSerializer(UserSerializer):
    email = serializers.EmailField()
    # semester = serializers.IntegerField()
    # academic_program = AcademicProgramSerializer()
    # type_document = DocumentTypeSerializer()
    # gender = GenderSerializer()

    class Meta(UserSerializer.Meta):
        model = Estudiante
        fields = UserSerializer.Meta.fields + ['semester', 'academic_program', 'accumulated_hours']

    def validate_semester(self, value):
        if value == "":
            raise serializers.ValidationError("Error, el semestre no puede estar vacio")
        if value < 1 or value > 10:
            raise serializers.ValidationError("Error, el semestre debe estar entre 1 y 10")
        return value

    def validate_academic_program(self, value):
        if value.code == "":
            raise serializers.ValidationError("Error, el programa academico no puede estar vacio")
        if not AcademicProgram.objects.filter(code=value.code).exists():
            raise serializers.ValidationError("Error, el programa academico no existe")
        return value

class UsuarioBienestarSerializer(UserSerializer):
    email = serializers.EmailField()
    # type_document = serializers.CharField()
    class Meta(UserSerializer.Meta):
        model = UsuarioBienestar
        fields = UserSerializer.Meta.fields + ['dimension']

class ListUsuarioBienestarSerializer(serializers.ModelSerializer):
    dimension = DimensionSerializer()
    class Meta:
        model = UsuarioBienestar
        fields = ['id', 'username', 'email', 'name', 'last_name', 'gender', 'type_document', 'identification', 'dimension', 'is_active', 'last_login']

class EditUsuarioBienestarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioBienestar
        fields = ['id', 'username', 'email', 'name', 'last_name', 'identification', 'gender', 'type_document', 'dimension', 'is_active']

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=16, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El link de restablecimiento es invalido', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('El link de restablecimiento es invalido', 401)        
        return super().validate(attrs)
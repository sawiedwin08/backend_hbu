from django.urls import path
from apps.users.api.api import user_api_view, user_detail_api_view, create_student_api_view, create_collaborator_api_view, academic_programs_api_view, genders_api_view, document_types_api_view, VerifyEmail, PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView, user_detailStudent_api_view

urlpatterns = [
    path('user/', user_api_view, name='user_api'),
    path('create-student/', create_student_api_view, name='create_student'),
    path('user-student/<int:pk>/', user_detailStudent_api_view, name='user_detailStudent_api_view'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('create-collaborator/', create_collaborator_api_view, name='create_collaborator'),
    path('user/<int:pk>/', user_detail_api_view, name='user_detail_api_view'),

    # path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('academic-programs/', academic_programs_api_view, name='academic_programs'),
    path('genders/', genders_api_view, name='genders'),
    path('document-types/', document_types_api_view, name='document_types')
]
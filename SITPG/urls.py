from django.contrib.staticfiles.templatetags.staticfiles import static as staticfiles
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from SITPG import views
from django.conf import settings
from django.conf.urls.static import static
from controlcenter.views import controlcenter
from django.contrib.auth import views as auth_views

# url patters for apps
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', controlcenter.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),    
    path(
        'admin/password_reset/', 
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
     ),
    path(
        'admin/password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
     ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    url(
        r'^$', views.home_redirect, 
        name="home_redirect"
    ),

    url(
        regex=r'^email-users/$', 
        view=views.SendUserEmails.as_view(), 
        name='email'
    ), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this is for handling document queries 
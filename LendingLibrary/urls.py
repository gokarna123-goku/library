
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

    path('login/', auth_views.LoginView.as_view(
    template_name='registration/login.html',  
    extra_context={ 
        'next': '/', 
    },
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

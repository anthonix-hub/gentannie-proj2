from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
# from gentannieApp.views import signup
from gentannieReferal.views import signup_view
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gent_marketering.urls')),
    path('', include('gentannieApp.urls')),
    path('', include('gentannieReferal.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('signup', signup_view, name='signup_view'),
    # path('signup/',signup.as_view(),name='signup'),
    path('tinymce', include('tinymce.urls'))

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

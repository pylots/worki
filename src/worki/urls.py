from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from wiki_page.views import ListPages

urlpatterns = [
    path('', ListPages.as_view()),
    path('wiki/', include('wiki_page.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

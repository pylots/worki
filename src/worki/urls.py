from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.conf import settings
from django.conf.urls.static import static
from wiki_page.views import ListPages

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'worki.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^$', ListPages.as_view()),
    url( r'^wiki/', include( 'wiki_page.urls' )),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$','django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login' ),
    url(r'^accounts/logout/$','django.contrib.auth.views.logout', { 'next_page': '/' }, name='logout' ),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

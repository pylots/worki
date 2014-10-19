from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^search/$','wiki_page.views.search', name='search'),
                       url(r'^by_tag/(?P<tag>[^/]+)/$', 'wiki_page.views.pages_by_tag', name='pages_by_tag'),
                       url(r'^by_user/(?P<user>[^/]+)/$', 'wiki_page.views.pages_by_user', name='pages_by_user'),
                       url(r'^(?P<slug>[-\w]+)/$', 'wiki_page.views.show_page', name='show_wiki_page'),
                       url(r'^(?P<slug>[-\w]+)/edit/$', 'wiki_page.views.edit', name='edit_wiki_page'),
                       )

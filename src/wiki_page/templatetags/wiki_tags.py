from datetime import datetime, timedelta
from django.template import Library
from django.contrib.auth.models import User
from wiki_page.models import WikiPage
import time, pytz

register = Library()

maxsize = 150 
minsize = 50

@register.filter
def short_date(d):
	return d.strftime('%y%m%d %H%M')

@register.filter
def synopsis( text ):
	return text[:50]

@register.simple_tag
def is_selected(url, pattern):
	import re
	if re.search('wiki/' + pattern, url):
		return 'active'
	return ''

@register.inclusion_tag('tags/page_breadcrumb.html')
def page_breadcrumb(wiki_page):
	return {'wiki_page': wiki_page}

@register.inclusion_tag('tags/wiki_nav.html')
def wiki_nav(url):
	# has no parents
	return {'roots': WikiPage.objects.filter(parent__isnull=True), 'url' : url }


def get_page_view_cloud(qs):
	max1=max([int(item.page_views.count()) for item in qs])
	for i in range(qs.count()):
		if max1 > 0:
			size =int(round(int(qs[i].page_views.count())*maxsize/max1))
			qs[i].show = True
			if size<minsize:
				size=minsize
				qs[i].show = False
			cloudsize =str(size) +"%"
			qs[i].cloudsize=cloudsize
		else:
			qs[i].cloudsize = "100%"
	return qs

@register.inclusion_tag('tags/get_cloud_by_page_views.html')
def get_cloud_by_page_views():
	qs = WikiPage.objects.all()
	pages = get_page_view_cloud(qs)
	# return {'pages': sorted(pages, key=lambda page: page.cloudsize, reverse=False)[:10]}
	return {'pages': pages }

@register.inclusion_tag('tags/get_cloud_by_tags.html')
def get_cloud_by_tags( ):
	tags = WikiPage.tags.all()
	return {'tags': tags }

@register.inclusion_tag('tags/get_cloud_by_user_views.html')
def get_cloud_by_user_views():
	td = datetime.now( pytz.utc) - timedelta( days=90 )
	qs = User.objects.filter( last_login__gte=td )
	users = get_page_view_cloud(qs)
	return {'users': sorted(users, key=lambda page: page.cloudsize, reverse=False)[:10]}
	# return {'users': users }

@register.inclusion_tag('tags/get_expired_views.html')
def get_expired_views():
	n = datetime.now( pytz.utc )
	expired = WikiPage.objects.filter( ttl__lte=n )
	return {'pages': [page for page in expired][:10]}

@register.inclusion_tag('tags/latest_edits.html')
def latest_edits():
	pages = WikiPage.objects.order_by('-last_edit')[:15]
	return {'pages': pages}


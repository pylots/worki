import pytz
from datetime import datetime, timedelta
# Create your views here.
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from wiki_page.models import WikiPage
from wiki_page.forms import WikiPageForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q
from django.views.generic.list import ListView


class ListPages( ListView ):
    model = WikiPage
    template_name = 'wiki_page/index.html'

def show_page(request, slug):
    authorized = False
    if not isinstance( request.user, AnonymousUser ):
        authorized = True
    try:
        wiki_page = WikiPage.objects.get(slug=slug)
        if authorized :
            wiki_page.page_views.create(user=request.user)
        expired = False
        if wiki_page.ttl and wiki_page.ttl < datetime.now( pytz.utc ):
            expired = True
        return render_to_response( 'wiki_page/show.html', 
            { 'wiki_page': wiki_page, 'url' : request.path, 'expired':expired, 'authorized' : authorized }, 
                context_instance=RequestContext( request ))
    except WikiPage.DoesNotExist:
        return HttpResponseRedirect(reverse('edit_wiki_page', args=[slug]))

def proces_form( request, wiki_page, slug, form ):
    if form.is_valid():
        cur_ttl = None
        if wiki_page :
            cur_ttl = wiki_page.ttl
        ttl = int(form.cleaned_data["ttl"])
        tags = form.cleaned_data[ "tags" ]
        wiki_page = form.save(commit=False)
        wiki_page.slug = slug
        wiki_page.author = request.user
        wiki_page.save( )
        wiki_page.tags.add(*tags)
        if ttl == 9999 :
            wiki_page.ttl = cur_ttl
        elif ttl > 0 :
            wiki_page.ttl = datetime.now( pytz.utc ) + timedelta(days=ttl)
        else: # forever
            wiki_page.ttl = None
        if wiki_page.version == None :
            wiki_page.version = 0
        wiki_page.version += 1
        return wiki_page
    return None

@login_required
def edit(request, slug):
    post = request.POST
    try:
        wiki_page = WikiPage.objects.get( slug=slug )
        if post :
            # try to save an updated page
            form = WikiPageForm( post, instance=wiki_page )
            if proces_form( request, wiki_page, slug, form ):
                wiki_page.save()
                return HttpResponseRedirect(reverse('show_wiki_page', args=[slug]))
        else:
            # show something with wiki_page as instance
            form = WikiPageForm( instance=wiki_page )
    except WikiPage.DoesNotExist:
        if post :
            # try to save a new wiki_page
            form = WikiPageForm( post )
            wiki_page = proces_form( request, None, slug, form )
            if wiki_page != None :
                if 'parent' in request.GET.keys():
                    wiki_page.parent = WikiPage.objects.get(slug=request.GET['parent'])
                wiki_page.save()
                return HttpResponseRedirect(reverse('show_wiki_page', args=[slug]))
        else: 
            form = WikiPageForm()
    return render_to_response('wiki_page/edit.html', {'form': form, 'url' : request.path }, context_instance=RequestContext(request))
    
def pages_by_tag(request, tag):
    print 'looking for tag', tag
    if tag == 'all' :
        tags = WikiPage.tags.all( )
        print 'tags=', tags
        page_list = WikiPage.objects.filter(tags__name__in=[tag for tag in tags]).distinct( )
    else:
        page_list = WikiPage.objects.filter(tags__name__in=[tag])
    return render_to_response('wiki_page/index.html', {'object_list': page_list, 'head': tag, 'url' : request.path }, context_instance=RequestContext(request))

def search(request):
    if 'q' in request.GET.keys():
        q = request.GET['q']
        object_list = WikiPage.objects.filter(Q(body__icontains=q)|Q(slug__icontains=q)|Q(author__username=q))
    else:
        return HttpResponseRedirect('/')
    return render_to_response('wiki_page/index.html', {'object_list': object_list, 'head': 'Search', 'url' : request.path})
    
def pages_by_user( request, user ):
    user_list = WikiPage.objects.filter( author__username=user )
    return render_to_response( 'wiki_page/index.html', { 'object_list' : user_list, 'head' : user, 'url' : request.path })

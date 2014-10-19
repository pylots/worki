from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re, sys
from taggit.managers import TaggableManager
import pytz

class WikiPage(models.Model):
    """ a simple wikipage """
    
    slug = models.SlugField(unique=True)
    body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    last_edit = models.DateTimeField(auto_now=True)
    ttl = models.DateTimeField(null=True, blank=True)
    version = models.IntegerField( null=True, blank=True )
    tags = TaggableManager( )
    
    def get_tags( self ):
        return tags.names( )

    def camel_parsed_text(self):
        pattern = re.compile('(\[[-\w]+\])')
        
        def _create_or_show( m ):
            cc = m.group( )
            # remove [ ] around tag
            if cc[ 0 ] == '[' and cc[ -1 ] == ']':
                cc = cc[1:-1]
            try:
                page = WikiPage.objects.get(slug=cc)
                if page.ttl and page.ttl < datetime.now( pytz.utc ):
                    return "<a class='ttl' title='page expired!' href='%s'>%s</a>" % (reverse('show_wiki_page', kwargs={'slug': cc}), cc)
                else:
                    return "<a href='%s'>%s</a>" % (reverse('show_wiki_page', kwargs={'slug': cc}), cc)
                    
            except WikiPage.DoesNotExist:
                return "<a class='create' title='create by clicking' href='%s?parent=%s'>%s</a>" % (reverse('edit_wiki_page', kwargs={'slug': cc}), self.slug, cc)
            except:
                return "%s" % sys.exc_info()[1]

        return pattern.sub( _create_or_show, self.body)
    
    def recurse_for_parents(self, p_lst=None):
        if not p_lst:
            p_lst = [self]        
        if self.parent:
            # prevent dead_locks
            if self.parent in p_lst:
                return p_lst
            p_lst.append(self.parent)
            p_lst = self.parent.recurse_for_parents(p_lst)
        return p_lst
    
    def __unicode__(self):
        return self.slug
    
    class Meta:
        ordering = ('slug',)
    
class WikiPageViewLog(models.Model):
    """ a logger to gather info of who clicked wich page when """
    page = models.ForeignKey(WikiPage, related_name='page_views')
    user = models.ForeignKey(User, related_name='page_views')
    log_time = models.DateTimeField(auto_now_add=True)
    

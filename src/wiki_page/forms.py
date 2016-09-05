from wiki_page.models import WikiPage
from django import forms
from taggit.forms import TagWidget, TagField

CHOICES = (
        (9999, 'update'),
	(1100, '3 years'), 
	(367, '1 year' ), 
	(95, '3 months'),
	(33, '1 month'),
	(0, 'forever')
	)

class WikiPageForm(forms.ModelForm):
    ttl = forms.ChoiceField( label="Valid for", choices=CHOICES)
    tags = TagField( required=False )
    class Meta:
        exclude = ('slug','author','parent', 'ttl', 'version')
        model = WikiPage
        widgets = {
            'tags' : TagWidget(),
            }

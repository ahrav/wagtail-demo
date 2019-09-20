from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks


class BlogListingPage(Page):
    """Page that lists all blog objects"""

    template = 'blog/blog_listing_page.html'

    custom_title = models.CharField(max_length=100,
                                    blank=False,
                                    null=False,
                                    help_text='Overwrite default title')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Add custom details to context"""

        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        return context


class BlogDetailPage(Page):
    """Each detailed blog page"""

    custom_title = models.CharField(max_length=100,
                                    blank=False,
                                    null=False,
                                    help_text='Overwrite default title')
    blog_image = models.ForeignKey(
        'wagtailimages.image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    content = StreamField([
        ('title_and_text', blocks.TitleAndTextBlock()),
        ('full_richtext', blocks.RichTextBlock()),
        ('cards', blocks.CardBlock()),
        ('cta', blocks.CTABlock()),
    ],
                          null=True,
                          blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
    ]
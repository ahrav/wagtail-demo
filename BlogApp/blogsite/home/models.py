from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, ObjectList,
                                         PageChooserPanel, StreamFieldPanel,
                                         TabbedInterface)
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks


class HomePageCarouselImages(Orderable):
    """Between 1-5 images for home page carousel"""

    page = ParentalKey('home.HomePage', related_name='carousel_images')
    carousel_image = models.ForeignKey('wagtailimages.Image',
                                       null=True,
                                       blank=False,
                                       on_delete=models.SET_NULL,
                                       related_name='+')

    panels = [
        ImageChooserPanel('carousel_image'),
    ]

    api_fields = [
        APIField('carousel_image'),
    ]


class HomePage(RoutablePageMixin, Page):
    """ Home Page """

    templates = "templates/home/home_page.html"
    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]
    # max_count = 1
    parent_page_type = ['wagtailcore.Page']

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'])
    banner_image = models.ForeignKey('wagtailimages.Image',
                                     null=True,
                                     blank=False,
                                     on_delete=models.SET_NULL,
                                     related_name='+')
    banner_cta = models.ForeignKey('wagtailcore.Page',
                                   null=True,
                                   blank=False,
                                   on_delete=models.SET_NULL,
                                   related_name='+')

    content = StreamField(
        [
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    api_fields = [
        APIField('banner_title'),
        APIField('banner_subtitle'),
        APIField('banner_image'),
        APIField('banner_cta'),
        APIField('carousel_images'),
        APIField('content'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('carousel_images', max_num=5, min_num=1,
                        label='Image'),
        ],
                        heading='Carousel Images'),
        StreamFieldPanel('content'),
    ]

    banner_panels = [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ],
                        heading='Banner Options'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(banner_panels, heading='Banner Settings'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'),
    ])

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    @route(r'^subscribe/$')
    def subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['special'] = 'hello world'
        return render(request, 'home/subscribe.html', context)


HomePage._meta.get_field('title').verbose_name = 'Verbbbyy'
HomePage._meta.get_field('title').help_text = 'Custom help text'
HomePage._meta.get_field('title').default = 'Default Value'
HomePage._meta.get_field('slug').default = 'default-value'

from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel, PageChooserPanel,
                                         StreamFieldPanel, InlinePanel,
                                         MultiFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks
from subscribers.forms import SubscriberForm


class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for home page carousel"""

    page = ParentalKey('home.HomePage', related_name='carousel_images')
    carousel_image = models.ForeignKey('wagtailimages.Image',
                                       null=True,
                                       blank=False,
                                       on_delete=models.SET_NULL,
                                       related_name='+')

    panels = [
        ImageChooserPanel('carousel_image'),
    ]


class HomePage(RoutablePageMixin, Page):
    """Home page model"""

    template = 'home/home_page.html'
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'])
    banner_image = models.ForeignKey('wagtailimages.Image',
                                     null=True,
                                     blank=False,
                                     on_delete=models.SET_NULL,
                                     related_name='+')
    banner_cta = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    content = StreamField([
        ('cta', blocks.CTABlock()),
    ],
                          null=True,
                          blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ],
                        heading='Banner Options'),
        MultiFieldPanel([
            InlinePanel('carousel_images', max_num=5, min_num=1,
                        label='Image'),
        ],
                        heading='Carousel Images'),
        StreamFieldPanel('content'),
    ]

    class Meta:

        verbose_name = 'Bloggy Home Page'
        verbose_name_plural = 'Bloggy Home Pages'

    @route(r'^subscribe/$')
    def subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        form = SubscriberForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = SubscriberForm()
        context = {
            'form': form,
        }
        return render(request, 'home/subscribe.html', context)

from django import forms
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, StreamFieldPanel)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from streams import blocks


class BlogAuthorsOrderable(Orderable):
    """Allow to select one or more blog authors from snippet"""

    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel('author'),
    ]


class BlogAuthor(models.Model):
    """Blog author for snippets"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                ImageChooserPanel('image'),
            ],
            heading='Name and Image',
        ),
        MultiFieldPanel(
            [FieldPanel('website')],
            heading='Links',
        )
    ]

    def __str__(self):
        """String repr of this class"""

        return self.name

    class Meta:  #noqa
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for a snippet"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='Slug to identify posts by this category',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:  #noqa
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        """String repr for BlogCategory"""

        return self.name


register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog detail pages"""

    template = 'blog/blog_listing_page.html'

    custom_title = models.CharField(max_length=100,
                                    blank=False,
                                    null=False,
                                    help_text='Overwrite the default title')

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        category = request.GET.get('category', '')
        print(category)
        if category:
            context['posts'] = BlogDetailPage.objects.live().public().filter(
                categories__slug=category)
            return context
        context['posts'] = BlogDetailPage.objects.live().public()
        context['categories'] = BlogCategory.objects.all()
        return context

    @route(r'^latest/$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:2]
        return render(request, 'blog/latest_posts.html', context)

    def get_sitemap_urls(self, request):
        # return [] no sitemap for this page
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            'location':
            self.full_url + self.reverse_subpage('latest_posts'),
            'lastmod': (self.last_published_at
                        or self.latest_revision_created_at),
            'priority':
            0.9
        })
        return sitemap


class BlogDetailPage(Page):
    """Blog detail page"""

    custom_title = models.CharField(max_length=100,
                                    blank=False,
                                    null=False,
                                    help_text='Overwrite the default title')
    blog_image = models.ForeignKey('wagtailimages.Image',
                                   blank=False,
                                   null=True,
                                   related_name='+',
                                   on_delete=models.SET_NULL)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichtextBlock()),
            ('simple_richtext', blocks.SimpleRichtextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label='Author', min_num=1, max_num=4)
        ],
                        heading='Author(s)'),
        MultiFieldPanel(
            [FieldPanel('categories', widget=forms.CheckboxSelectMultiple)],
            heading='Categories'),
        StreamFieldPanel('content'),
    ]

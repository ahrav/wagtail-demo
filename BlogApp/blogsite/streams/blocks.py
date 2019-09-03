""" Streamfields are here """

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock




class TitleAndTextBlock(blocks.StructBlock):
    """ Title and text."""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:  #noqa
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title and Text'


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)"""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True)),
            ('title', blocks.CharBlock(required=True, max_length=40)),
            ('text', blocks.TextBlock(required=True, max_length=200)),
            ('button_page', blocks.PageChooserBlock(required=False)),
            ('button_url', blocks.URLBlock(required=False, help_text='If the button page above is selected, that will be used first')),
        ]))

    class Meta:  #noqa
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Staff Cards'


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all features"""
    class Meta:  #noqa
        template = 'streams/richtext_block.html'
        icon = 'doc-full'
        label = 'Full Richtext'


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext without all features"""
    def __init__(self,
                 required=True,
                 help_text=None,
                 editor='default',
                 features=None,
                 validators=(),
                 **kwargs):
        super().__init__(**kwargs)
        self.field_options = {
            'required': required,
            'help_text': help_text,
            'validators': validators,
        }
        self.editor = editor
        self.features = [
            'bold',
            'italic',
            'link',
        ]

    class Meta:  #noqa
        template = 'streams/richtext_block.html'
        icon = 'edit'
        label = 'Simple Richtext'


class CTABlock(blocks.StructBlock):
    """Simple call to action"""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    class Meta: #noqa
        template = 'streams/cta_block.html'
        icon = 'placeholder'
        label = 'Call to Action'


class LinkStructValue(blocks.StructValue):
    """Additional logic for urls."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        return None


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""

    button_page = blocks.PageChooserBlock(required=False, help_text='If selected this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added this url will be used secondarily')

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta: #noqa
        template = 'streams/button_block.html'
        icon = 'placeholder'
        label = 'Single Button'
        value_class = LinkStructValue

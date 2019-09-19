"""Streamfields are here"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text only"""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:  #noqa
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & Text'


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)"""

    title = blocks.CharBlock(required=True, help_text='Add your title')

    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True)),
            ('name', blocks.CharBlock(required=True, max_length=40)),
            ('title', blocks.TextBlock(required=True, max_length=200)),
            ('button_page', blocks.PageChooserBlock(required=False)),
            ('button_url', blocks.URLBlock(required=False, help_text='If button page above selected, that will be used first')),
        ]))

    class Meta:  #noqa
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Staff Cards'


class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all features"""
    class Meta:  #noqa
        template = 'streams/richtext_block.html'
        icon = 'doc-full'
        label = 'Full Richtext'

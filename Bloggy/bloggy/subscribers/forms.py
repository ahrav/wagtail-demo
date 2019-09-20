from django.forms import ModelForm
from subscribers.models import Subscriber


class SubscriberForm(ModelForm):
    """Model for to register subscribers to the site"""
    class Meta:
        model = Subscriber
        fields = ['email', 'full_name']

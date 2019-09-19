from django.db import models


class Subscriber(models.Model):
    """A subscriber model"""

    email = models.CharField(blank=False,
                             null=False,
                             help_text='Email',
                             max_length=150)
    full_name = models.CharField(max_length=100,
                                 blank=False,
                                 null=False,
                                 help_text='Full Name')

    def __str__(self):
        return self.full_name

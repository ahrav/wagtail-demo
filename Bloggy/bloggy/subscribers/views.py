# from django.shortcuts import render
# from django.views.generic.edit import CreateView

# from subscribers.forms import SubscriberForm
# from subscribers.models import Subscriber

# def subscriber_create_view(request):
#     form = SubscriberForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#     context = {
#         'form': form,
#     }
#     return render(request, 'home/subscribe.html', context)

# class SubscriberCreate(CreateView):
#     """View to handle lettings users become a subscriber"""

#     model = Subscriber
#     fields = ['email', 'full_name']
#     template_name = 'home/subscribe.html'

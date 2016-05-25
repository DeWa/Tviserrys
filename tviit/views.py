from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render
from .models import Tviit, TviitForm
from user_profile.models import UserProfile
import uuid


class IndexView(View):

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tviit/index.html')
        profile = UserProfile.objects.get(user=request.user)
        context = {
            'profile': profile,
        }
        return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def create_tviit(request):
    if request.method == 'POST':
        form = TviitForm(request.POST, request.FILES)

        if form.is_valid():
            f = form.save(commit=False)
            f.uuid = uuid.uuid4().int
            f.sender = request.user

            # If there's image
            if 'image' in request.FILES:
                f.image = request.FILES['image']

            f.save()
            return HttpResponse(status=201) # Created


    else:
        return HttpResponse(status=400) # Bad Content


def reply_tviit(request):
    if request.method == 'POST':
        form = TviitForm(request.POST, request.FILES)

        if form.is_valid():
            if request.POST.get('reply'):
                reply = Tviit.objects.get(uuid=request.POST.get('reply'))
                if not reply:
                    return HttpResponse(status=404)  # Not found
            else:
                return HttpResponse(status=400)  # Bad Content


            f = form.save(commit=False)
            f.uuid = uuid.uuid4().int
            f.sender = request.user
            f.reply = reply


            # If there's image
            if 'image' in request.FILES:
                f.image = request.FILES['image']

            f.save()
            return HttpResponse(status=201) # Created


    else:
        return HttpResponse(status=400) # Bad Content

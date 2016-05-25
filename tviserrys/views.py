from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render
from tviit.models import Tviit, TviitForm
from django.contrib.auth.models import User
from user_profile.models import UserProfile


class IndexView(View):


    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tviit/index.html')
        profile = UserProfile.objects.get(user=request.user)

        tviits = get_latest_tviits(profile)
        print(tviits)
        context = {
            'profile': profile,
            'tviit_form': TviitForm,
            'tviits': tviits,
        }
        return HttpResponse(template.render(context, request))


# Get all the tviits, which aren't replies
def get_latest_tviits(profile):
    follows = User.objects.filter(pk__in=profile.follows.all())
    tviits = Tviit.objects.filter(sender__in=follows)
    return tviits
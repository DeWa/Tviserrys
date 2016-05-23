from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render
from tviit.models import Tviit, TviitForm


class IndexView(View):


    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tviit/index.html')
        context = {
            'tviit_form': TviitForm,
        }
        return HttpResponse(template.render(context, request))

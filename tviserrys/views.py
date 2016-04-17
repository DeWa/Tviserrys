from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render


class IndexView(View):
    template_name = 'tviit/index.html'

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        if request.user.is_facilitator:
            context = RequestContext(request, {
            })

            return render(request, self.template_name, context)

        else:
            raise PermissionDenied


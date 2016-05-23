from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response, render
from models import UserProfile, EditProfileForm
from django.conf import settings

class EditView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        template = loader.get_template('profile/edit.html')
        user = request.user
        profile = UserProfile.objects.get(user=user)
        form = EditProfileForm(instance=profile)

        context = {
            'user': user,
            'profile': profile,
            'form': form,
        }

        return HttpResponse(template.render(context, request))

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request, *args, **kwargs):
        template = loader.get_template('profile/edit.html')
        user = request.user
        profile = UserProfile.objects.get(user=user)
        form = EditProfileForm(request.POST, request.FILES, instance=profile)


        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect('/profile')
        else:

            context = {
                'user': user,
                'profile': profile,
                'form': EditProfileForm(request.POST, instance=profile),
            }

            return HttpResponse(template.render(context, request))

class ViewView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        template = loader.get_template('profile/view.html')
        if 'user_name' in kwargs:
            user = get_object_or_404(User, username=kwargs['user_name'])
        else:
            user = request.user

        profile = UserProfile.objects.get(user=user)

        context = {
            'user': user,
            'profile': profile,
            'apikey': settings.GOOGLE_API_KEY
        }

        return HttpResponse(template.render(context, request))

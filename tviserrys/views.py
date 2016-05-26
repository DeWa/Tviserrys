from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render
from django import forms
from tviit.models import Tviit, TviitForm
from user_profile.models import CreateProfileForm
from django.contrib.auth.models import User, Group
from user_profile.models import UserProfile


class IndexView(View):

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, *args, **kwargs):
        template = loader.get_template('tviit/index.html')
        profile = UserProfile.objects.get(user=request.user)
        users = get_random_users()

        tviits = get_latest_tviits(profile)
        context = {
            'profile': profile,
            'tviit_form': TviitForm,
            'random_users': users,
            'tviits': tviits,
        }
        return HttpResponse(template.render(context, request))

class RegisterView(View):
        def get(self, request, *args, **kwargs):
            # If user is already logged in, redirect to front page
            if request.user.is_authenticated():
                return HttpResponseRedirect("/")

            template = loader.get_template('registration/register.html')
            form = CreateProfileForm()
            context = {
                'form': form,
            }
            return HttpResponse(template.render(context, request))

        def post(self, request, *args, **kwargs):
            # If user is already logged in, redirect to front page
            if request.user.is_authenticated():
                return HttpResponseRedirect("/")

            form = CreateProfileForm(request.POST, request.FILES)
            template = loader.get_template('registration/register.html')
            if form.is_valid():
                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                password=password)
                f = form.save(commit=False)
                f.user = user
                f.save()
                g = Group.objects.get(name='users')
                g.user_set.add(user)

                return HttpResponseRedirect("/")
            else:
                context = {
                    'form': form,
                }
                return HttpResponse(template.render(context, request))


# Get all the tviits, which aren't replies
def get_latest_tviits(profile):
    follows = User.objects.filter(pk__in=profile.follows.all())
    tviits = Tviit.objects.filter(sender__in=follows)
    return tviits

# Get 5 random users
def get_random_users():
    users = User.objects.filter(groups__name__in=['users']).order_by('?')[:5]
    return users
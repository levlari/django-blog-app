from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # New in Django 1.9
from django.views.decorators.csrf import csrf_protect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied

from .models import Article
from .forms import RegisterForm #, ArticleForm


# NOTE: The LoginRequiredMixin assumes LOGIN_URL is set. Otherwise
# define the `login_url` attribute.


class BlogHome(LoginRequiredMixin, ListView):
    """
    Home page for the blog. Displays 6 posts per page.
    """
    model = Article
    template_name = 'blog/home.html'
    paginate_by = 6


class ReadPost(LoginRequiredMixin, DetailView):
    """
    Displays a single blog post.
    """
    model = Article
    template_name = 'blog/read_post.html'


class WritePost(LoginRequiredMixin, CreateView):
    """
    Creates a new blog post.
    """
    # Required even when form_class is a ModelForm.
    model = Article
    # Comment out `fields` attribute when `form_class` is defined.
    # Define it in `Meta` class of form_class instead.
    # Defining both `fields` and `form_class` is illegal since Django 1.9.
    fields = ['title', 'content', 'image']
    template_name = 'blog/write_post.html'

    # Saves the model object when validated form data is POSTed.
    # Overriding this method to add additional fields.
    # We can also do this in the `save()` of form_class by overriding it.
    # But since CreateView includes ModelFormMixin, we should handle it here.
    # That way we don't have to create a ModelForm explicitly.
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        # Uploaded files are accessible from request.FILES['file'].
        form.instance.image = form.cleaned_data.get('image', None)
        form.instance.word_count = len(form.cleaned_data['content'].split())
        # Ceiling division. Assuming avg reading speed.
        form.instance.read_time_in_mins = (form.instance.word_count + 130 - 1) // 130
        return super(WritePost, self).form_valid(form)

    # To add extra features not present in default generated ModelForm
    # form_class = ArticleForm
    #
    # def get_form_kwargs(self):
    #     kwargs = super(WritePost, self).get_form_kwargs()
    #     kwargs.update({'author': self.request.user})
    #     return kwargs


class DeletePost(LoginRequiredMixin, DeleteView):
    """
    Deletes a post if user is the author.
    Otherwise shows HTTP 403 PermissionDenied.
    """
    model = Article
    template_name = 'blog/delete_post.html'
    # Not using `reverse()` as the URLconfs are not loaded when the file is imported.
    success_url = reverse_lazy('blog:home')

    # delete related image (override delete method).

    # `delete()` method can also be overridden to achieve the same result.
    def get_object(self, queryset=None):
        obj = super(DeletePost, self).get_object()
        if not obj.author == self.request.user:
            raise PermissionDenied  # HTTP 403 (django built-in)
        else:
            return obj


@csrf_protect
def register(request):
    """
    Registers the user to database but sets `is_active` attribute to False.
    Sends email to user with the activation link.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user is inactive untill email verification
            user.is_active = False
            user.save()

            # Send email with a one-time only uid and token.
            subject = "Blog account register confirmation."
            context = {
                'user': user,
                'protocol': 'http',
                'domain': 'upkkbd9aabef.pankaj05.koding.io',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            message = loader.render_to_string('blog/register_confirm_email.html', context)
            user.email_user(subject, message, from_email=settings.EMAIL_HOST_USER)
            return HttpResponseRedirect(reverse('blog:register_confirm'))
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def register_confirm(request):
    """
    Displays email sent message.
    """
    return render(request, 'blog/register_confirm.html')


# Doesn't need csrf_protect since no one can guess the URL.
def register_check(request, uidb64=None, token=None):
    """
    Check the hash in a registration confirmation link.
    Redirects to `register_done` page.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None # checked by URLconf
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('blog:register_done'))
    else:
        return HttpResponse("Cannot verify your account. Please contact site admin.")


def register_done(request):
    """
    Shows registration complete message.
    """
    return render(request, 'blog/register_done.html')

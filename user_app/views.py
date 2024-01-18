from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView
from .forms import SignUpForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
# Create your views here.


def send_verify_mail_to_user(confirm_link, user):
    email_subject = "Confirm Your Email"
    email_body = render_to_string(
        'verify_email.html', {'confirm_link': confirm_link})
    email = EmailMultiAlternatives(email_subject, '', to=[user.email])
    email.attach_alternative(email_body, 'text/html')
    email.send()


base_link = 'http://127.0.0.1:8000'


# class BookCreateView(CreateView):
#     def get(self, request, *args, **kwargs):
#         context = {'form': BookCreateForm()}
#         return render(request, 'books/book-create.html', context)

#     def post(self, request, *args, **kwargs):
#         form = BookCreateForm(request.POST)
#         if form.is_valid():
#             book = form.save()
#             book.save()
#             return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
#         return render(request, 'books/book-create.html', {'form': form})


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.is_active = False
            user_form.save()
            uid = urlsafe_base64_encode(force_bytes(user_form.pk))
            confirm_link = f"{base_link}/users/activate/{uid}/"
            send_verify_mail_to_user(confirm_link, user_form)
            messages.success(request, 'Please Verify Your Mail For Login.')
            return redirect('login')
    return render(request, 'signup.html', {'form': form})


class UserLogin(LoginView):
    template_name = 'login.html'
    model = User

    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("home")

    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def user_logout(request):
    logout(request)
    return redirect('login')


def activate(request, uid64):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        print(user)
        return redirect('login')
    else:
        return redirect('signup')


# class UserProfile(DetailView):
#     model = User
#     pk_url_kwarg = 'id'
#     template_name = 'profile.html'

#     def post(self, request, *args, **kwargs):
#         update_form = UserUpdateForm(data=self.request.POST)
#         if update_form.is_valid():
#             update_form.save()
#         return self.get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.object
#         orders = Order.objects.filter(user=user)
#         update_form = UserUpdateForm()
#         added_cars = Car.objects.filter(owner=user)
#         context['update_form'] = update_form
#         context['orders'] = orders
#         context['added_cars'] = added_cars
#         context['user_info'] = user
#         return context

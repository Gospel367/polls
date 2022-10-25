from http.client import HTTPResponse
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.http import BadHeaderError, Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from polls_app.forms import NewsletterForm, SignUpForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,  force_str
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from polls_app.token import account_activation_token
from django.contrib.auth.models import User
from polls_app.models import Newsletter, Profile
from django.core.mail import send_mail


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'register.html'
    redirect_authenticated_user = True
    
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            
            user =form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.set_password(form.cleaned_data["password2"])
            user.is_active =False
            user.is_staff=False

            user.save()
            
            current_site = get_current_site(request)
            subject ='Congrats! Activate Your Account'
            message =render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please ' + user.username + ' Confirm your email to complete registration'))
            return redirect('signup')
        return render(request, self.template_name, {'form':form})



class Activation(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user =User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user =None
            
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active =True
            user.is_staff=True
            use =User.objects.get(username=user)
            use.saver.email_confirmed=True
            user.save()
            messages.success(request, ('Your account has been confirmed. Please Login Now'))
            return redirect('index')
        else:
            messages.warning(request, ('Validation of account fatally failed'))
            return redirect('index')
        
        
class LoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    
class LogoutView(LogoutView):
    pass



def index(request):
    latest_question_list = User.objects.all()
    context = { 'latest_question_list': latest_question_list, }
    return render(request, 'index.html', context)

'''class PubCreate(LoginRequiredMixin,  FormView):
    model = Newsletter
    form_class = NewsletterForm
    template_name ='newsletter.html'
    redirect_authenticated_user =True
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['emails'] = User.objects.all()
        return context
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        subject = self.request.POST.get('title', '')
        html_message = self.request.POST.get('description', '')
        from_email = 'adminlogoman@gmail.com'
        if subject and html_message and from_email:
            try:
                send_mail(subject, html_message, from_email, ['floxy@gmail.com', 'admin@yahoo.com'])
                    
            except BadHeaderError:
                return HttpResponse('Bad header error')
        else:
            return HttpResponse('INVALID ONE MY GUY')
        return super(PubCreate, self).form_valid(form)'''


class PubCreate(LoginRequiredMixin,  FormView):
    model = Newsletter
    form_class = NewsletterForm
    template_name ='newsletter.html'
    redirect_authenticated_user =True
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['emails'] = User.objects.all()
        return context
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        don = form.instance.title
        author = form.instance.author
        post = form.instance.description[:100]
        current_site = get_current_site(self.request)
        from_email = 'admin@gmail.com'
        receivers = []
        for userman in User.objects.all():
            receivers.append(userman.email)
        subject ='Our Latest Post: ' + don + '.'
        message =render_to_string( 'newsletter_email.html', {
                     'post': post,
                    'domain': current_site.domain,
                    'don': don,
                    'author': author

                })
        send_mail(subject, message, from_email, receivers)
        messages.success(self.request, ('Please ' + self.request.user.username + 'Verify your newsletter is sent by checking your inbox'))
        return super(PubCreate, self).form_valid(form)



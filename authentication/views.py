from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_gen

# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username = data['userName']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain Alphanumeric charecters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry Username is in use, choose another name'}, status=409)

        return JsonResponse({'username_valid':True})

        

class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry Email in use, choose another one'}, status=409)

        return JsonResponse({'email_valid':True})

        

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['userName']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if(len(password) < 8):
                    messages.error(request,'Password too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                email_subject = 'Activate your account'
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                #path to view
                # -- getting domain we're on
                domain = get_current_site(request).domain
                # -- relative URL verification
                link= reverse('activate',kwargs={'uidb64':uidb64, 'token':token_gen.make_token(user)})
                # -- encode uid
                # -- token
                activate_url='http://'+domain+link
                email_body ='Hi '+ username+" Please use this link to verify your account \n"+ activate_url
                # emailSend = EmailMessage(
                #             email_subject,
                #             email_body,
                #             'noreply@trulyexpenses.com',
                #             [email],
                #         )
                emailSend = EmailMessage(
                email_subject,
                email_body,
                'noreply@trulyexpenses.com',
                [email],
                [],
                reply_to=[],
                headers={},
                )
                emailSend.send(fail_silently=False)
                messages.success(request,'Account created Successfully!')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self,request, uidb64, token):
        return redirect('login')


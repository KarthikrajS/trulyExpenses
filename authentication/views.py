from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        userName = data['userName']
        
        if not str(userName).isalnum():
            return JsonResponse({'username_error':'username should only contain Alphanumeric charecters'}, status=400)

        if User.objects.filter(username=userName).exists():
            return JsonResponse({'username_error':'Sorry Username is in use, choose another name'}, status=409)

        return JsonResponse({'username_valid':True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
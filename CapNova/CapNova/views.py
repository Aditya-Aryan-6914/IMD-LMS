from django.http import HttpResponse
from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        category = request.POST.get("category")
        email = request.POST.get("email")
        return render(request, 'auth/success.html', {
            'full_name': full_name,
            'category': category,
            'email': email
        })
    return render(request, 'auth/register.html')

def login(request):
    return render(request,'auth/login.html')

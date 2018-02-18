from django.shortcuts import render, redirect
from django.contrib import auth
from django.conf import settings

def index(request):
    return render(request, "index.html")

def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = settings.FIREBASE_AUTH.sign_in_with_email_and_password(email, password)
        except Exception as error:
            return render(request, "sign_in.html", {"alert": 'invalid ID or password'})
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        return redirect("/index/")
    return render(request, "sign_in.html")

def logout(request):
    auth.logout(request)
    return render(request, 'sign_in.html', {"alert", "successfully signed out"})

def upload_bills(request):
    bills = []
    data = settings.FIREBASE_DB.child("requests").get().val()
    for num, entry in enumerate(data.items()):
        bills.append({'num': num, 'id': entry[0], 'timestamp': entry[1]['timestamp']})
    return render(request, 'upload_bills.html', {'bills': bills})

def chart(request):
    return render(request, 'chart.html')

def profile(request):
    return render(request, 'profile.html')


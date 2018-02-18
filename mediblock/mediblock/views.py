import datetime
import pygal
import pandas as pd
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

def medical_bills(request):
    bills = []
    data = settings.FIREBASE_DB.child("requests").get().val()
    if data:
        num = len(data)
        for id, entry in reversed(data.items()):
            bills.append({'num': num, 'id': id, 'timestamp': entry['timestamp']})
            num-=1
    else:
        bills = None
    return render(request, 'medical_bills.html', {'bills': bills})

def medical_bill_info(request, medical_bill_id):
    fb_request = settings.FIREBASE_DB.child("requests").child(medical_bill_id).get().val()
    fb_request_timestamp = fb_request['timestamp'] if fb_request else None

    fb_request_imgs = settings.FIREBASE_DB.child("requests_imgs").child(medical_bill_id).get().val()
    fb_request_img_base64 = fb_request_imgs['image'] if fb_request_imgs else None

    blockchain = settings.FIREBASE_DB.child("blockchain").child(medical_bill_id).get().val()
    blockchain_data = blockchain['data'] if blockchain else None
    blockchain_timestamp = blockchain['timestamp'] if blockchain else None

    blockchain_img = settings.FIREBASE_DB.child("blockchain_imgs").child(medical_bill_id).get().val()
    blockchain_img_base64 = blockchain_img['image'] if blockchain_img else None

    return render(request, 'medical_bill_info.html', {
        'medical_bill_id': medical_bill_id,
        'request_timestamp': fb_request_timestamp,
        'request_img_base64': fb_request_img_base64,
        'blockchain_data': blockchain_data,
        'blockchain_timestamp': blockchain_timestamp,
        'blockchain_img_base64': blockchain_img_base64,
    })

def chart(request):
    csv_data = pd.read_csv('mediblock_data.csv')
    csv_data.convert_objects(convert_numeric=True).dtypes
    csv_data_points = pd.Series(csv_data.iloc[:,2])
    py_chart = pygal.Bar()
    py_chart.x_labels = map(str, range(2013, 2013))
    py_chart.add('Debridement & Destruction', list(csv_data_points[:50].astype('float')))
    py_chart.add('Occupational  Therapy', list(csv_data_points[50:100].astype('float') * 2))
    py_chart.add('Echocardiography', list(csv_data_points[100:150].astype('float') * 0.6))
    data = py_chart.render_data_uri()

    return render(request, 'chart.html', {'data': data})

def profile(request):
    return render(request, 'profile.html')


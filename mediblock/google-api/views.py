# coding: utf-8
import datetime
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from . import vision_api

def analyze(request, medical_bill_id):
    timestamp = datetime.datetime.now().isoformat()
    fb_request_imgs = settings.FIREBASE_DB.child("requests_imgs").child(medical_bill_id).get().val()
    if fb_request_imgs:
        base64_img_str = fb_request_imgs['image']
    else:
        return HttpResponse('Internal Server Error', status=502)
    image_str, data = vision_api.render_doc_text(base64_img_str)
    settings.FIREBASE_DB.child("blockchain").child(medical_bill_id).set({
        'id':medical_bill_id,
        'data': data,
        'timestamp': timestamp
    })
    settings.FIREBASE_DB.child("blockchain_imgs").child(medical_bill_id).set({
        'id': medical_bill_id,
        'image': str(image_str),
        'timestamp': timestamp
    })

    return redirect('/medical_bills/' + medical_bill_id)
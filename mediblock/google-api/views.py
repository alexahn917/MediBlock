# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse

def transform(request):
    return HttpResponse('OK', status=200)
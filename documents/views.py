from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

# TODO views for documents


def index(request):
    return render(request, 'documents/index.html', None)

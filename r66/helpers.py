from django.template import Context
from django.template import loader
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.core import serializers
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.core import serializers

from r66.models import *

# def _save_session_messages(request, messages, errors):
#     request.session['messages']=messages
#     request.session['errors']=errors
# 
#     request.session.modified = True

def _pop_session_messages(request):
    messages = []
    errors = []
    try:
        messages = request.session['messages']
        request.session['messages']=[]
    except KeyError:
        pass
    try:
        errors = request.session['errors']
        request.session['errors']=[]
    except KeyError:
        pass

    request.session.modified = True

    return messages,errors



def _create_context(request):
    context_dict={}

    messages,errors = _pop_session_messages(request)
    context_dict['messages']=messages
    context_dict['error_messages']=errors
    # context_dict['nav_global']=settings.MENU_BAR

    return context_dict



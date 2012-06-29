from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.core import serializers
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.core import serializers

from django import forms
from django.contrib.auth.decorators import login_required

from r66 import helpers

def index(request):

    context_dict = {}
    context_dict = RequestContext(request)
    context_dict = RequestContext(request, {
            'title': 'Title',
            'content_description': 'Description for this content',
            })
    return render_to_response('r66/index.html', context_dict)


def home(request, page_id):
    context_dict = helpers._create_context(request)
    context_dict["page_id"] = page_id
    context = RequestContext(request, context_dict)

    if page_id == "interfaces":
      context_dict["title"] = "Interfaces"
      context_dict["content_description"] = "Description for interfaces page"

      return render_to_response('r66/interfaces.html', context)

    if page_id == "search":
      context_dict["content_description"] = "This list shows network \
 interfaces detected \
 by the R66 system. Here, you can add or delete any interface to the \
 network manager service"
      context_dict["title"] = "Search network interfaces"

      return render_to_response('r66/search.html', context)

    context_dict["title"] = "Anyother"
    context_dict["content_description"] = "Description for anyother page"

    return render_to_response('r66/anyother.html', context)




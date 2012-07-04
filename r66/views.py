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
import r66.forms
import r66.models

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
      context_dict["content_description"] = "Network interfaces managed by R66"

      return render_to_response('r66/interfaces.html', context)

    if page_id == "bridges":
      context_dict["title"] = "Bridges"
      context_dict["content_description"] = "Network bridges managed by R66"

      return render_to_response('r66/bridges.html', context)

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


def bridges(request, profile_id=None):
    page_id = "bridge_profiles"

    context_dict = helpers._create_context(request)
    context_dict["page_id"] = page_id
    context_dict["selected_profile"] = profile_id
    context = RequestContext(request, context_dict)

    context_dict["title"] = "Bridges"
    context_dict["content_description"] = "Network bridges and network " + \
"bridges profiles managed by R66"

    return render_to_response('r66/bridge_profile.html', context)


def interfaces(request, profile_id=None):
    page_id = "interface_profiles"

    context_dict = helpers._create_context(request)
    context_dict["page_id"] = page_id
    context_dict["selected_profile"] = profile_id
    context = RequestContext(request, context_dict)

    context_dict["title"] = "Interfaces"
    context_dict["content_description"] = "Network interfaces and network " + \
"interfaces profiles managed by R66"

    p = None
    try:
      p = r66.models.NetIfaceProfile.objects.get(pk=profile_id)
    except Exception:
      p = None

    if p:
      context_dict["net_settings_form"] = \
            r66.forms.NetSettingsForm(instance = \
              p.net_settings, prefix="net"
            )
      context_dict["net_settings_extended_form"] = \
            r66.forms.NetSettingsExtendedForm(instance = \
              p.net_settings, prefix="netextended"
            )
      context_dict["wifi_settings_form"] = \
            r66.forms.WirelessSettingsForm (instance = \
              p.wifi_settings, prefix="wifi"
            )
      context_dict["dhcpd_settings_form"] = \
            r66.forms.DhcpdSettingsForm (instance = \
              p.dhcpd_settings, prefix="dhcpd"
            )
      context_dict["netiface_profile_form"] = \
            r66.forms.NetIfaceProfileForm (instance = \
              p, prefix="profile"
            )
    else:
      context_dict["net_settings_form"] = \
            r66.forms.NetSettingsForm(instance = \
              None, prefix="net"
            )
      context_dict["net_settings_extended_form"] = \
            r66.forms.NetSettingsExtendedForm(instance = \
              None, prefix="netextended"
            )
      context_dict["wifi_settings_form"] = \
            r66.forms.WirelessSettingsForm (instance = \
              None, prefix="wifi"
            )
      context_dict["dhcpd_settings_form"] = \
            r66.forms.DhcpdSettingsForm (instance = \
              None, prefix="dhcpd"
            )
      context_dict["netiface_profile_form"] = \
            r66.forms.NetIfaceProfileForm (instance = \
              None, prefix="profile"
            )


    return render_to_response('r66/interface_profile.html', context)


def interfaces_index (request):
    _first_netiface_profile = None
    try:
        _first_netiface_profile \
          = r66.models.NetIfaceProfile.objects.all()[0].id
    except Exception:
        _first_netiface_profile = None

    return interfaces(request, _first_netiface_profile)


def interfaces_new (request):
    return interfaces(request, None)



from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from django.core import serializers
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.core import serializers


from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from r66 import helpers
import r66.forms
import r66.models

@login_required
def logout_user(request):
    logout(request)
    return redirect( reverse('r66-home',args=["interfaces"]) )

def login_user(request):
    username = password = ''
    error_messages = []
    messages = []
    context_dict = RequestContext(request, {
            'title': 'Login',
            'content_description': 'Introduce username and password to access into the admin panel',
            'error_messages': error_messages,
            'messages': messages,
            })
    context_dict["page_id"] = "login"
    next_ = request.GET.get('next')
    context_dict["next"] = next_

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_ = request.POST.get('next')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                messages.append(state)
                if next_:
                    return redirect(next_)
            else:
                state = "Your account is not active, please contact the site admin."
                error_messages.append(state)
        else:
            state = "Your username and/or password were incorrect."
            error_messages.append(state)
        context_dict["username"] = username

    return render_to_response('r66/auth.html',context_dict)


@login_required
def success(request):

    context_dict = RequestContext(request, {
            'title': 'Successful operation',
            'content_description': 'Operation successful.',
            })
    context_dict["page_id"] = "success"
    return render_to_response('r66/success.html', context_dict)


@login_required
def home(request, page_id):
    context_dict = helpers._create_context(request)
    context_dict["page_id"] = page_id
    context = RequestContext(request, context_dict)

    if page_id == "ppp3g":
      context_dict["title"] = "PPP/3G"
      context_dict["content_description"] = "PPP/3G devices managed by R66"

      ppp_list = r66.models.NetPPP.objects.all()
      if len(ppp_list)==0:
          ppp = r66.models.NetPPP()
          ppp.save()
      else:
          ppp = ppp_list[0]

      context_dict["3gppp_form"] = \
            r66.forms.NetPPPForm(instance = \
              ppp, prefix="3gppp"
            )
 
      return render_to_response('r66/ppp3g.html', context)


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


@login_required
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


@login_required
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

    net_settings = None
    wifi_settings = None
    dhcpd_settings = None
    try:
        net_settings = p.net_settings
    except Exception:
        net_settings = None
    try:
        wifi_settings = p.wifi_settings
    except Exception:
        wifi_settings = None
    try:
        dhcpd_settings = p.dhcpd_settings
    except Exception:
        dhcpd_settings = None


    context_dict["net_settings_form"] = \
            r66.forms.NetSettingsForm(instance = \
              net_settings, prefix="net"
            )
    context_dict["net_settings_extended_form"] = \
            r66.forms.NetSettingsExtendedForm(instance = \
              net_settings, prefix="netextended"
            )
    context_dict["wifi_settings_form"] = \
            r66.forms.WirelessSettingsForm (instance = \
              wifi_settings, prefix="wifi"
            )
    context_dict["wifi_settings_none_form"] = \
            r66.forms.WirelessSettingsNoneForm (instance = \
              wifi_settings, prefix="wifinone"
            )
    context_dict["wifi_settings_wep_form"] = \
            r66.forms.WirelessSettingsWepForm (instance = \
              wifi_settings, prefix="wifiwep"
            )
    context_dict["wifi_settings_wpa_form"] = \
            r66.forms.WirelessSettingsWpaForm (instance = \
              wifi_settings, prefix="wifiwpa"
            )

    context_dict["wifi_settings_hostapd_form"] = \
            r66.forms.WirelessSettingsHostapdForm (instance = \
              wifi_settings, prefix="wifihostapd"
            )

    context_dict["dhcpd_settings_form"] = \
            r66.forms.DhcpdSettingsForm (instance = \
              dhcpd_settings, prefix="dhcpd"
            )
    context_dict["dhcpd_settings_extended_form"] = \
            r66.forms.DhcpdSettingsExtendedForm (instance = \
              dhcpd_settings, prefix="dhcpdextended"
            )
    context_dict["netiface_profile_form"] = \
            r66.forms.NetIfaceProfileForm (instance = \
              p, prefix="profile"
            )
    context_dict["netiface_profile_extended_form"] = \
            r66.forms.NetIfaceProfileExtendedForm (instance = \
              p, prefix="profileextended"
            )



    return render_to_response('r66/interface_profile.html', context)

@login_required
def interfaces_index (request):
    _first_netiface_profile = None
    try:
        _first_netiface_profile \
          = r66.models.NetIfaceProfile.objects.all()[0].id
    except Exception:
        _first_netiface_profile = None

    return interfaces(request, _first_netiface_profile)


@login_required
def interfaces_new (request):
    return interfaces(request, None)


@login_required
def index(request):
    return home(request, "interfaces")

@login_required
def anyother(request):
    return home(request, "anyother")








@login_required
def cifs(request, profile_id=None):
    page_id = "cifs"

    context_dict = helpers._create_context(request)
    context_dict["page_id"] = page_id
    context_dict["selected_profile"] = profile_id
    context = RequestContext(request, context_dict)

    context_dict["title"] = "CIFS service"
    context_dict["content_description"] = "CIFS/SMB server managed by R66"

    try:
      cifs = r66.models.CifsSettings.objects.all()[0]
    except Exception:
      cifs = r66.models.CifsSettings()


    context_dict["samba_settings_form"] = \
            r66.forms.CifsSettingsForm(instance = \
              cifs, prefix="cifs"
            )

    return render_to_response('r66/cifs.html', context)



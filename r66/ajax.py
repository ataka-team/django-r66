from django.utils import simplejson
from dajaxice.core import dajaxice_functions
import netutils
import models
import helpers
import forms

from django.core import serializers

from dajaxice.decorators import dajaxice_register

@dajaxice_register
def search_devices(request):
    ifaces = netutils.get_interfaces_names()
    wifi_ifaces = netutils.get_wifi_interfaces_names()

    res = {}

    for i in ifaces:
        res[i]=netutils.get_interface_info(i)
        if netutils.is_wifi_interface(i):
           res[i]["wifi"]=netutils.get_wifi_interface_info(i)
        if netutils.is_bridge(i):
           res[i]["bridge"]=netutils.get_bridge_interface_info(i)

        try:
           _objs = models.NetIface.objects.filter(name=i)
           if len(_objs) > 0:
              res[i]["added"]=True
        except ValueError:
           pass


    return simplejson.dumps(res)


@dajaxice_register
def get_netifaces(request):
    ifaces = models.NetIface.objects.all()

    data = serializers.serialize('json', ifaces,
        fields=('name','description', 'enabled'))

    return data


@dajaxice_register
def get_netiface_profiles(request):
    iface_profiles = models.NetIfaceProfile.objects.all()

    data = serializers.serialize('json', iface_profiles,
        fields=('name','description', 'enabled', 'netiface', 'netiface_type'))

    return data


@dajaxice_register
def send_netiface_profile(request, form):
    message = []
    print form
    form_dict = helpers.serialized_array_to_dict(form)
    form = form_dict

    p = None
    try:
      profile_id = form_dict["selected_profile"]
      p = r66.models.NetIfaceProfile.objects.get(pk=profile_id)
    except Exception:
      p = None

    f0 = None
    try:
        f0 = forms.NetIfaceProfileForm(form, instance = \
              p, prefix="profile"
        )
    except Exception:
        f0 = forms.NetIfaceProfileForm(form,
                    prefix="profile"
        )


    f1 = None
    try:
        f1 = forms.NetSettingsForm(form, instance = \
              p.net_settings, prefix="net"
        )
    except Exception:
        f1 = forms.NetSettingsForm(form,
                    prefix="net"
        )


    net_settings_extended_form = None
    try:
        net_settings_extended_form = \
                forms.NetSettingsExtendedForm(form, instance = \
              p.net_settings, prefix="netextended"
        )
    except Exception:
        net_settings_extended_form = \
                forms.NetSettingsExtendedForm(form,
                    prefix="netextended"
        )


    f2 = None
    try:
        f2 = forms.WirelessSettingsForm(form, instance = \
              p.wifi_settings, prefix="wifi"
        )

    except Exception:
        f2 = forms.WirelessSettingsForm(form,
                    prefix="wifi"
        )


    f3 = None
    try:
        f3 = forms.DhcpdSettingsForm(form, instance = \
              p.dhcpd_settings, prefix="dhcpd"
        )

    except Exception:
        f3 = forms.DhcpdSettingsForm(form,
                    prefix="dhcpd"
        )

    valid = True
    if not f0.is_valid():
        valid = False
        e = f0.errors
        message = message + [e.as_ul()]
    if not f1.is_valid():
        valid = False
        e = f1.errors
        message = message + [e.as_ul()]
    if not net_settings_extended_form.is_valid():
        valid = False
        e = net_settings_extended_form.errors
        message = message + [e.as_ul()]
    if not f2.is_valid():
        valid = False
        e = f2.errors
        message = message + [e.as_ul()]
    if not f3.is_valid():
        valid = False
        e = f3.errors
        message = message + [e.as_ul()]

    if valid:
        f1.save()
        f2.save()
        f3.save()
        net_settings_extended_form.save()
        f0.save()

    return simplejson.dumps({'status':message})



@dajaxice_register
def add_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # Already exists 
      pass
    else:
      _netiface = models.NetIface(enabled=False, name=name)
      _netiface.save()

    return search_devices(request)

@dajaxice_register
def delete_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs.delete()
    else:
      pass

    return search_devices(request)

@dajaxice_register
def enable_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=True
      _objs[0].save()
    else:
      pass

    return get_netifaces(request)

@dajaxice_register
def disable_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=False
      _objs[0].save()
    else:
      pass

    return get_netifaces(request)

@dajaxice_register
def get_netbridges(request):
    bridges = models.NetBridge.objects.all()

    # res = {}

    data = serializers.serialize('json', bridges,
        fields=('name','description', 'enabled'))

    return data


@dajaxice_register
def add_netbridge(request,name, description=""):
    _objs = models.NetBridge.objects.filter(name=name)
    if len(_objs)>0: # Already exists 
      pass
    else:
      _netbridge = models.NetBridge(enabled=False, name=name,
              description=description)
      _netbridge.save()

    return get_netbridges(request)

@dajaxice_register
def delete_netbridge(request,name):
    _objs = models.NetBridge.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs.delete()
    else:
      pass

    return get_netbridges(request)

@dajaxice_register
def enable_netbridge(request,name):
    _objs = models.NetBridge.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=True
      _objs[0].save()
    else:
      pass

    return get_netbridges(request)

@dajaxice_register
def disable_netbridge(request,name):
    _objs = models.NetBridge.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=False
      _objs[0].save()
    else:
      pass

    return get_netbridges(request)



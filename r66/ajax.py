from django.utils import simplejson
from django.core import serializers
from dajaxice.decorators import dajaxice_register
from django.conf import settings

from dajaxice.core import dajaxice_functions
import netutils
import models
import helpers
import forms

import os
import subprocess

def _deletefile(filename):
  subprocess.Popen( "rm -f " + filename,
          shell=True, bufsize=0,
          stdout=open('/dev/null','w'),
          stderr=open('/dev/null','w'))


def _writefile(strings,filename):
    aux = filename.split(os.sep)[0:-1]
    _d = ""
    for i in aux:
        _d = _d + i + os.sep
        try:
          os.mkdir(_d)
        except Exception:
          pass
    f = open(filename, 'w')
    f.write(strings)
    f.close()

@dajaxice_register
def configuration_changed(request):
    status = models.get_status()

    res = status.to_dict()
    return simplejson.dumps(res)

@dajaxice_register
def apply_changes(request):
    messages = []
    status = models.get_status()

    network_interfaces = ""
    ntp_conf = ""
    dhcpd_conf = "log-facility local7;\n\n"

    ppp = models.NetPPP.objects.all()
    for p in ppp:
        _deletefile(settings.R66_ETC_DIR
                    + "/ppp/peers/r66")
        _deletefile(settings.R66_ETC_DIR
                    + "/ppp/r66.chat")

        if p.enabled:
            strings = p.to_peer()
            _writefile(strings, settings.R66_ETC_DIR
                    + "/ppp/peers/r66")
            strings = p.to_chat()
            _writefile(strings, settings.R66_ETC_DIR
                    + "/ppp/r66.chat")

    _deletefile(settings.R66_ETC_DIR
                    + "/hostapd/*.conf")
    _deletefile(settings.R66_ETC_DIR
                    + "/wpa_supplicant/*.conf")


    netifaces = models.NetIface.objects.all()
    for n in netifaces:
      try:
        # TODO: Clean previous files for each device

        # print "> " + str(n)
        p = n.get_enabled_profile() # can be none
        if n.enabled and p:
            network_interfaces += p.to_network_interfaces()
            type_ = p.netiface_type
            if type_ == "bridge":
                # wifi can be only master mode
                if n.wifi_device:
                    strings = p.to_hostapd_conf()
                    _writefile(strings, settings.R66_ETC_DIR
                        + "/hostapd/" + n.name + ".conf")


            if type_ == "internal":
                # cannot be p.dhcp == True
                _tmp = p.to_ntp_conf()
                if _tmp != "":
                    ntp_conf = _tmp

                # wifi can be only master mode
                if n.wifi_device:
                    strings = p.to_hostapd_conf()
                    _writefile(strings, settings.R66_ETC_DIR
                        + "/hostapd/" + n.name + ".conf")


                if p.dhcpd_settings  \
                        and p.dhcpd_settings.enabled:
                    dhcpd_conf += p.to_dhcpd_conf()


            if type_ == "external":
                if not p.net_settings.dhcp:
                    _tmp = p.to_ntp_conf()
                    if _tmp != "":
                        ntp_conf = _tmp


                # wifi can be only client mode
                if n.wifi_device:
                    strings = p.to_wpa_supplicant_conf()
                    _writefile(strings, settings.R66_ETC_DIR
                        + "/wpa_supplicant/" + n.name + ".conf")

            if type_ == "unused":
                pass # nothing to do

      except Exception, e:
          messages.append(str(e))

    strings = network_interfaces
    _writefile(strings, settings.R66_ETC_DIR
                        + "/network/interfaces")

    strings = ntp_conf
    _writefile(strings, settings.R66_ETC_DIR
                        + "/ntp.conf")

    strings = dhcpd_conf
    _writefile(strings, settings.R66_ETC_DIR
                        + "/dhcp/dhcpd.conf")


    res = {"status":messages}

    if len (messages)== 0:
        # status.unmark_as_changed()
        pass

    return simplejson.dumps(res)


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
        fields=('name','description', 'enabled', 'wifi_device',
            'enabled_profile'))

    return data


@dajaxice_register
def get_netiface_profiles(request):
    iface_profiles = models.NetIfaceProfile.objects.all()

    data = serializers.serialize('json', iface_profiles,
        fields=('name','description', 'enabled', 'netiface', 'netiface_type'))

    return data


@dajaxice_register
def delete_netiface_profile(request, id):
    message = []
    p = None
    try:
      profile_id = int(id)
      p = models.NetIfaceProfile.objects.get(pk=profile_id)
    except Exception, e:
      messages.append(str(e))


    if p.net_settings:
        p.net_settings.delete()

    if p.wifi_settings:
        p.wifi_settings.delete()

    if p.dhcpd_settings:
        p.dhcpd_settings.delete()

    if p:
        p.delete()

    return simplejson.dumps({'status':message})


@dajaxice_register
def send_3gppp(request, form):
    message = []
    form_dict = helpers.serialized_array_to_dict(form)
    form = form_dict

    ppp_list = models.NetPPP.objects.all()
    if len(ppp_list)==0:
          ppp = models.NetPPP()
          ppp.save()
    else:
          ppp = ppp_list[0]


    netppp_form = forms.NetPPPForm(form, instance = \
              ppp, prefix="3gppp"
        )

    valid = True
    if not netppp_form.is_valid():
        valid = False
        e = netppp_form.errors
        message = message + [e.as_ul()]

    if valid:
        ppp = netppp_form.save()

    return simplejson.dumps({'status':message})





@dajaxice_register
def send_netiface_profile(request, form):
    message = []
    form_dict = helpers.serialized_array_to_dict(form)
    form = form_dict
    p = None
    try:
      profile_id = int(form_dict["selected_profile"])
      p = models.NetIfaceProfile.objects.get(pk=profile_id)
    except Exception, e:
      p = models.NetIfaceProfile()

    net_settings = None
    wifi_settings = None
    dhcpd_settings = None
    try:
        net_settings = p.net_settings
    except Exception:
        net_settings = models.NetSettings()
    try:
        wifi_settings = p.wifi_settings
    except Exception:
        wifi_settings = models.WirelessSettings()
    try:
        dhcpd_settings = p.dhcpd_settings
    except Exception:
        dhcpd_settings = models.DhcpdSettings()


    netiface_profile_form = forms.NetIfaceProfileForm(form, instance = \
              p, prefix="profile"
        )

    netiface_profile_extended_form = forms.NetIfaceProfileExtendedForm(form, instance = \
              p, prefix="profileextended"
        )

    net_settings_form = forms.NetSettingsForm(form, instance = \
              net_settings, prefix="net"
        )

    net_settings_extended_form = \
                forms.NetSettingsExtendedForm(form, instance = \
              net_settings, prefix="netextended"
        )

    wireless_settings_form = forms.WirelessSettingsForm(form, instance = \
             wifi_settings, prefix="wifi"
        )
    wireless_settings_none_form = forms.WirelessSettingsNoneForm(form, instance = \
             wifi_settings, prefix="wifinone"
        )
    wireless_settings_wep_form = forms.WirelessSettingsWepForm(form, instance = \
             wifi_settings, prefix="wifiwep"
        )
    wireless_settings_wpa_form = forms.WirelessSettingsWpaForm(form, instance = \
             wifi_settings, prefix="wifiwpa"
        )
    wireless_settings_hostapd_form = forms.WirelessSettingsHostapdForm(form, instance = \
             wifi_settings, prefix="wifihostapd"
        )


    dhcpd_settings_form = forms.DhcpdSettingsForm(form, instance = \
              dhcpd_settings, prefix="dhcpd"
        )
    dhcpd_settings_extended_form = forms.DhcpdSettingsExtendedForm(form, instance = \
              dhcpd_settings, prefix="dhcpdextended"
        )



    valid = True
    if not netiface_profile_form.is_valid():
        valid = False
        e = netiface_profile_form.errors
        message = message + [e.as_ul()]
    if not netiface_profile_extended_form.is_valid():
        valid = False
        e = netiface_profile_form.errors
        message = message + [e.as_ul()]

    if not net_settings_form.is_valid():
        valid = False
        e = net_settings_form.errors
        message = message + [e.as_ul()]
    if not net_settings_extended_form.is_valid():
        valid = False
        e = net_settings_extended_form.errors
        message = message + [e.as_ul()]

    if not wireless_settings_form.is_valid():
        valid = False
        e = wireless_settings_form.errors
        message = message + [e.as_ul()]
    if not wireless_settings_none_form.is_valid():
        valid = False
        e = wireless_settings_none_form.errors
        message = message + [e.as_ul()]
    if not wireless_settings_wep_form.is_valid():
        valid = False
        e = wireless_settings_wep_form.errors
        message = message + [e.as_ul()]
    if not wireless_settings_wpa_form.is_valid():
        valid = False
        e = wireless_settings_wpa_form.errors
        message = message + [e.as_ul()]
    if not wireless_settings_hostapd_form.is_valid():
        valid = False
        e = wireless_settings_hostapd_form.errors
        message = message + [e.as_ul()]

    if not dhcpd_settings_form.is_valid():
        valid = False
        e = dhcpd_settings_form.errors
        message = message + [e.as_ul()]
    if not dhcpd_settings_extended_form.is_valid():
        valid = False
        e = dhcpd_settings_extended_form.errors
        message = message + [e.as_ul()]

    if valid:
        net_settings = net_settings_form.save()
        net_settings = forms.NetSettingsExtendedForm(form, instance = \
             net_settings, prefix="netextended"
        ).save()

        wifi_settings = wireless_settings_form.save()
        wifi_settings = forms.WirelessSettingsNoneForm(form, instance = \
             wifi_settings, prefix="wifinone"
        ).save()

        if form_dict["profile-netiface_type"] == "external":
          wifi_settings = forms.WirelessSettingsWepForm(form, instance = \
             wifi_settings, prefix="wifiwep"
          ).save()
          wifi_settings = forms.WirelessSettingsWpaForm(form, instance = \
             wifi_settings, prefix="wifiwpa"
          ).save()
        else:
          wifi_settings = forms.WirelessSettingsHostapdForm(form, instance = \
             wifi_settings, prefix="wifihostapd"
          ).save()


        dhcpd_settings = dhcpd_settings_form.save()
        dhcpd_settings = forms.DhcpdSettingsExtendedForm(form, instance = \
             dhcpd_settings, prefix="dhcpdextended"
        ).save()


        netiface_profile = netiface_profile_form.save()
        netiface_profile = forms.NetSettingsExtendedForm(form, instance = \
             netiface_profile, prefix="profileextended"
        ).save()

        netiface_profile.net_settings = net_settings
        netiface_profile.wifi_settings= wifi_settings
        netiface_profile.dhcpd_settings = dhcpd_settings
        netiface_profile.save()

        p = netiface_profile

    return simplejson.dumps({'status':message, 'profile_id':p.id})



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



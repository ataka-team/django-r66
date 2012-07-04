from django.utils import simplejson
from dajaxice.core import dajaxice_functions
import netutils
import models

from django.core import serializers

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

dajaxice_functions.register(search_devices)

def get_netifaces(request):
    ifaces = models.NetIface.objects.all()

    data = serializers.serialize('json', ifaces,
        fields=('name','description', 'enabled'))

    return data

dajaxice_functions.register(get_netifaces)

def get_netiface_profiles(request):
    iface_profiles = models.NetIfaceProfile.objects.all()

    data = serializers.serialize('json', iface_profiles,
        fields=('name','description', 'enabled', 'netiface', 'netiface_type'))

    return data

dajaxice_functions.register(get_netiface_profiles)

def get_netiface_profile_settings(request,id):
    try:
      _objs = models.NetIfaceProfile.objects.filter(id=id)
    except Exception, e:
      res = {"error": str(e)}
      return simplejson.dumps(res)

    data = serializers.serialize('json', _objs)
    return data

dajaxice_functions.register(get_netiface_profile_settings)



def add_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # Already exists 
      pass
    else:
      _netiface = models.NetIface(enabled=False, name=name)
      _netiface.save()

    return search_devices(request)
dajaxice_functions.register(add_netiface)

def delete_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs.delete()
    else:
      pass

    return search_devices(request)
dajaxice_functions.register(delete_netiface)

def enable_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=True
      _objs[0].save()
    else:
      pass

    return get_netifaces(request)
dajaxice_functions.register(enable_netiface)

def disable_netiface(request,name):
    _objs = models.NetIface.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=False
      _objs[0].save()
    else:
      pass

    return get_netifaces(request)
dajaxice_functions.register(disable_netiface)

def get_netbridges(request):
    bridges = models.NetBridge.objects.all()

    # res = {}

    data = serializers.serialize('json', bridges,
        fields=('name','description', 'enabled'))

    return data

dajaxice_functions.register(get_netbridges)

def add_netbridge(request,name, description=""):
    _objs = models.NetBridge.objects.filter(name=name)
    if len(_objs)>0: # Already exists 
      pass
    else:
      _netbridge = models.NetBridge(enabled=False, name=name,
              description=description)
      _netbridge.save()

    return get_netbridges(request)
dajaxice_functions.register(add_netbridge)

def delete_netbridge(request,name):
    _objs = models.NetBridge.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs.delete()
    else:
      pass

    return get_netbridges(request)
dajaxice_functions.register(delete_netbridge)

def enable_netbridge(request,name):
    _objs = models.NetBridge.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=True
      _objs[0].save()
    else:
      pass

    return get_netbridges(request)
dajaxice_functions.register(enable_netbridge)

def disable_netbridge(request,name):
    _objs = models.NetBridge.objects.filter(name=name)

    if len(_objs)>0: # exists 
      _objs[0].enabled=False
      _objs[0].save()
    else:
      pass

    return get_netbridges(request)
dajaxice_functions.register(disable_netbridge)



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
        try: # asume it is a wifi device
           wifi_ifaces.index(i)
           res[i]["wifi"]=netutils.get_wifi_interface_info(i)
        except ValueError:
           pass

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

    # res = {}

    data = serializers.serialize('json', ifaces,
        fields=('name','description', 'enabled'))

    # for i in ifaces:
    #     res[i]=netutils.get_interface_info(i)
    #     try: # asume it is a wifi device
    #        wifi_ifaces.index(i)
    #        res[i]["wifi"]=netutils.get_wifi_interface_info(i)
    #     except ValueError:
    #        continue

    # return simplejson.dumps(res)
    return data

dajaxice_functions.register(get_netifaces)

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


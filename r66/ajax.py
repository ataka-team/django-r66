from django.utils import simplejson
from dajaxice.core import dajaxice_functions
import netutils

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
           continue

    return simplejson.dumps(res)

dajaxice_functions.register(search_devices)


from django.db import models
from r66 import netutils
from django.utils.translation import ugettext_lazy as _


NETIFACE_TYPE_CHOICES = [
    ('bridge', _('Network bridge')),
    ('external', _('External network')),
    ('internal', _('Internal network')),
    ('unused', _('Unused network')),
]

WIFI_CHOICES = [
    ('WPA', _('WPA')),
    ('WEP', _('WEP')),
    ('NONE', _('NONE')),
]

WPA_KEY_MGMT_CHOICES = [
    ('WPA-PSK', _('WPA-PSK')),
    ('NONE', _('NONE')),
]
#    ('WPA-EAP', _('WPA-EAP')),

WPA_EAP_CHOICES = [
    ('TLS', _('TLS')),
    ('PEAP', _('PEAP')),
]

WPA_PAIRWISE_CHOICES = [
    ('TKIP', _('TKIP')),
    ('CCMP', _('CCMP')),
]

WEP_KEYMODE_CHOICES = [
    ('open', _("open")),
    ('restricted', _("restricted")),
]

def get_str_or_empty_str(obj):
    if obj:
        return obj
    return ""

class Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


class Status(models.Model):
    class Meta:
        verbose_name = 'Network Configuration state'

    changed = models.BooleanField(default=False)

    def mark_as_changed(self):
        self.changed = True
        self.save()

    def unmark_as_changed(self):
        self.changed = False
        self.save()

    def to_dict(self):
        res = {}
        res["changed"] = self.changed
        return res

def get_status():
    status = Status.objects.all()
    if len(status) == 0:
        status = Status()
        status.save()
    else:
        status = status[0]
    return status

class NetSettings(models.Model):
    class Meta:
        verbose_name = 'Network interface settings'

    ### external mode attributes

    # dynamic ip configuration
    dhcp = models.BooleanField(default=False)


    ### internal mode attributes

    # masquerade configuration
    masquerade = models.BooleanField(default=True)


    ### external & internal mode attributes

    # staticip configuration
    ip = models.IPAddressField(blank=True, null=True)
    netmask = models.IPAddressField(blank=True, null=True)
    dns1 = models.IPAddressField(blank=True, null=True)
    dns2 = models.IPAddressField(blank=True, null=True)
    gateway = models.IPAddressField(blank=True, null=True)
    ntp1 = models.IPAddressField(blank=True, null=True)
    ntp2 = models.IPAddressField(blank=True, null=True)

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(NetSettings, self).save(*args, **kwargs)

class WirelessSettings(models.Model):
    class Meta:
        verbose_name = 'Wireless settings'

    enabled=models.BooleanField(default=False)


    ssid = models.CharField(max_length=30,
        blank=True, null=True)

    wifi = models.CharField(max_length=30,
        choices=WIFI_CHOICES,
        default="NONE")

    # wpa
    wpa_priority = models.PositiveSmallIntegerField(
            blank=True, null=True,)
    wpa_scan_ssid = models.BooleanField(
        default=False)
    wpa_key_mgmt = models.CharField(max_length=30,
        choices=WPA_KEY_MGMT_CHOICES,
        blank=True, null=True)

    # None and WPA-PSK parameters
    wpa_psk = models.CharField(max_length=63,
        blank=True, null=True)
    # End. None and WPA-PSK parameters

    # WPA-EAP parameters
    wpa_eap = models.CharField(
        choices=WPA_EAP_CHOICES,
        max_length=30,
        blank=True, null=True)
    wpa_ca_cert = models.TextField(max_length=1000,
        blank=True, null=True)
    wpa_identity = models.CharField(max_length=100,
        blank=True, null=True)
    # End. WPA-EAP parameters


    # WPA-EAP + TLS parameters    
    wpa_client_cert = models.TextField(max_length=1000,
        blank=True, null=True)
    wpa_private_key  = models.TextField(max_length=1000,
        blank=True, null=True)
    wpa_private_key_passwd = models.CharField(max_length=100,
        blank=True, null=True)

    # WPA-EAP + PEAP parameters    
    wpa_password = models.CharField(max_length=100,
        blank=True, null=True)
    wpa_phase1 = models.CharField(max_length=100,
        blank=True, null=True)
    wpa_phase2 = models.CharField(max_length=100,
        blank=True, null=True)
    # phase2="auth=MSCHAPV2"
    # End. WPA-EAP + PEAP parameters    


    # wep
    wep_channel = models.IntegerField(
            blank=True, null=True)

    # wep_mode = managed
    # wep_mode = models.CharField(max_length=30,
    #         blank=True, null=True,)

    # wep_keymode = open
    wep_keymode = models.CharField(max_length=30,
            choices=WEP_KEYMODE_CHOICES,
            blank=True, null=True,)

    # wep_key1 = millavehexadecimal
    wep_key1 = models.CharField(max_length=250,
            blank=True, null=True,)

    # wep_key2 = s:millaveascii
    wep_key2 = models.CharField(max_length=250,
            blank=True, null=True,)

    wep_defaultkey = models.IntegerField(
            blank=True, null=True,)

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(WirelessSettings, self).save(*args, **kwargs)



class DhcpdSettings(models.Model):
    class Meta:
        verbose_name = 'DHCP daemon settings'

    enabled=models.BooleanField(default=False)

    authoritative=models.BooleanField(default=False)

    dns = models.CharField(_("Domain name server (domain-name-servers)"),
            max_length=100,
            blank=True, null=True,)

    domain_name = models.CharField(_("Domain name (domain-name)"),
            max_length=100,
            blank=True, null=True,)

    subnet = models.CharField(
            _("Subnet"),
            max_length=100,
            blank=True, null=True,)

    netmask = models.CharField(
            _("Netmask"),
            max_length=100,
            blank=True, null=True,)

    routers = models.CharField(_("Routers (routers)"),
            max_length=100,
            blank=True, null=True,)

    broadcast_address = models.CharField(
            _("Broadcast address (broadcast-address)"),
            max_length=100,
            blank=True, null=True,)

    default_lease_time = models.IntegerField(
            _("Default lease time (default-lease-time)"),
            blank=True, null=True,)

    max_lease_time = models.IntegerField(
            _("Max lease time (max-lease-time)"),
            blank=True, null=True,)

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(DhcpdSettings, self).save(*args, **kwargs)


class DhcpdSettingsHost(models.Model):
    class Meta:
        verbose_name = 'DHCP daemon settings'

    dhcp = models.ForeignKey(DhcpdSettings)

    mac = models.CharField(_("Ethernet MAC address"),
            max_length=100,)

    ip = models.IPAddressField()

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(DhcpdSettingsHost, self).save(*args, **kwargs)


# class NtpdSettings(models.Model):
#     class Meta:
#         verbose_name = 'Ntp daemon settings'
# 
#     enabled=models.BooleanField(default=False)
#     # TODO
# 
#     def __unicode__(self):
#         return self.name



class NetBridge(models.Model):
    class Meta:
        verbose_name = 'Network bridge'

    enabled=models.BooleanField(default=False)

    name = models.CharField(max_length=10)
    description = models.TextField(max_length=150)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(NetBridge, self).save(*args, **kwargs)

    def get_enabled_profile(self):
        related_profiles = \
NetBridgeProfile.objects.filter(bridge=self)

        for r in related_profiles:
            if r.enabled:
                return  r

        return None
        # raise Error("NetBridge (%s) hasn't got any profile enabled"
        #             % self.name)



class NetBridgeProfile(models.Model):
    class Meta:
        verbose_name = 'Network bridge profile'

    enabled=models.BooleanField(default=False)
    # TODO: Solo puede haber uno activo por cada Bridge

    description = models.TextField(max_length=150)

    bridge = models.ForeignKey(NetBridge)

    net_settings = models.ForeignKey(NetSettings,
            blank=True, null=True, on_delete=models.SET_NULL)

    dhcpd_settings = models.ForeignKey(DhcpdSettings,
            blank=True, null=True, on_delete=models.SET_NULL)

    # ntpd_settings = models.ForeignKey(NtpdSettings,
    #         blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(NetBridgeProfile, self).save(*args, **kwargs)




class NetIface(models.Model):
    class Meta:
        verbose_name = 'Network interface'

    enabled=models.BooleanField(default=False)

    wifi_device=models.BooleanField(default=False)

    netiface_type = models.CharField(_("Network interface type"),
            choices=NETIFACE_TYPE_CHOICES,
                        default='unused', max_length=100)


    name = models.CharField(max_length=10)
    description = models.TextField(max_length=150)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      self.wifi_device = netutils.is_wifi_interface(self.name)

      super(NetIface, self).save(*args, **kwargs)


    def get_enabled_profile(self):
        related_netiface_profiles = \
NetIfaceProfile.objects.filter(netiface=self)

        for r in related_netiface_profiles:
            if r.enabled:
                return r

        return None
        # raise Error("Netiface (%s) hasn't got any profile enabled"
        #             % self.name)












class NetIfaceProfile(models.Model):
    class Meta:
        verbose_name = 'Network interface profile'

    enabled=models.BooleanField(default=False)
    # TODO: Solo puede haber uno activo por cada NetIface

    description = models.TextField(max_length=150)

    netiface = models.ForeignKey(NetIface,
            blank=False, null=False )

    netiface_type = models.CharField(_("Network interface type"),
            choices=NETIFACE_TYPE_CHOICES,
                        default='unused',
                        max_length=100)

    bridge_profile = models.ForeignKey(NetBridgeProfile,
            blank=True, null=True)

    net_settings = models.ForeignKey(NetSettings,
            blank=True, null=True, on_delete=models.SET_NULL)

    wifi_settings = models.ForeignKey(WirelessSettings,
            blank=True, null=True, on_delete=models.SET_NULL)

    dhcpd_settings = models.ForeignKey(DhcpdSettings,
            blank=True, null=True, on_delete=models.SET_NULL)

    # ntpd_settings = models.ForeignKey(NtpdSettings,
    #         blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      if self.netiface and  self.enabled:
          # Search all NetIfaceProfile related with netiface
          # and demark as enabled
          related_netiface_profiles = \
NetIfaceProfile.objects.filter(netiface=self.netiface)

          for r in related_netiface_profiles:
              if r.enabled:
                  r.enabled = False
                  r.save()

          self.enabled = True

      super(NetIfaceProfile, self).save(*args, **kwargs)


    def _generate_static_params(self):
            name = self.netiface.name

            if not self.net_settings:
              raise Error("NetIfaceProfile for %s NetIface is wrong configured"
                % name)

            ip = ""
            if self.net_settings.ip:
                ip = self.net_settings.ip
            netmask=""
            if self.net_settings.netmask:
                netmask = self.net_settings.netmask
            gateway=""
            if self.net_settings.gateway:
                gateway = self.net_settings.gateway
            dns1=""
            if self.net_settings.dns1:
                dns1 = self.net_settings.dns1
            dns2 = ""
            if self.net_settings.dns2:
                dns2 = self.net_settings.dns2

            static_params = ""

            if ip == "":
                raise Error(\
              "IP for NetIface (%s) is empty"
              % name)

            if netmask == "":
                raise Error( "Netmask for NetIface (%s) is empty"
                        % name)

            static_params += "address " + ip + "\n"
            static_params += "netmask " + netmask + "\n"
            if gateway != "":
              static_params += "gateway " + gateway + "\n"

            if dns1 != "" or dns2 != "":
              static_params += "dns-nameservers " + \
                dns1 + " " + dns2 + "\n"

            return static_params

    def _generate_wifi_params(self):
            wifi_params = ""

            name = self.netiface.name

            sets = self.wifi_settings

            if not sets:
                raise Error(\
                  "NetIface %s is a wifi device but no WiFi settings was found"
                  % name)

            ssid = ""
            if sets.ssid:
                ssid = sets.ssid

            if not sets.enabled:
                return ""

            if sets.wifi == "NONE":
                return ""

            if sets.wifi == "WEP":
                if ssid != "":
                    wifi_params += "wireless_essid " + ssid + "\n"

                wifi_params += "wireless_mode managed" + "\n"

                wep_channel = ""
                if sets.wep_channel:
                    wep_channel = sets.wep_channel
                if wep_channel != "":
                    wifi_params += "wireless_channel " + wep_channel + "\n"

                wep_keymode = ""
                if sets.wep_keymode:
                    wep_keymode = sets.wep_keymode
                if wep_keymode != "":
                    wifi_params += "wireless_keymode " + wep_keymode + "\n"

                wep_key1 = ""
                if sets.wep_key1:
                    wep_key1 = sets.wep_key1
                if wep_key1 != "":
                    wifi_params += "wireless_key1 " + wep_key1 + "\n"

                wep_key2 = ""
                if sets.wep_key2:
                    wep_key2 = sets.wep_key2
                if wep_key2 != "":
                    wifi_params += "wireless_key2 " + wep_key2 + "\n"

                wep_defaultkey = ""
                if sets.wep_defaultkey:
                    wep_defaultkey = sets.wep_defaultkey
                if wep_defaultkey != "":
                    wifi_params += "wireless_defaultkey " + wep_defaultkey + "\n"



            if sets.wifi == "WPA":
                wifi_params += "wpa-driver wext\n"
                wifi_params += \
                  "/etc/wpa_supplicant/wpa_supplicant_%s.conf\n" % name

            return wifi_params



    def to_network_interfaces(self):


        name = self.netiface.name
        is_wifi = self.netiface.wifi_device

        type_ = self.netiface_type

        if not self.net_settings:
            raise Error("NetIfaceProfile for %s NetIface is wrong configured"
                % name)

        if is_wifi and not self.wifi_settings:
            raise Error(\
              "NetIface %s is a wifi device but no WiFi settings was found"
              % name)


        ### Network configuration depends on netiface_type ...

        if type_ == "bridge":
            res = \
'''
auto %s
iface %s inet manual
'''
            return res % (name,name)

        if type_ == "internal":

            res = \
'''
auto %s
iface %s inet static
%s
'''
            static_params = self._generate_static_params()
            # no wifi params needed because internal netiface wifi is only
            # available on master mode and this setup is configurable on
            # hostapd conffile.
            return res % (name, name,static_params)

        if type_ == "external":

            res = \
'''
auto %s
iface %s inet %s
%s
%s
'''
            if self.net_settings.dhcp:
                mode = "dhcp"
                static_params = ""
            else:
                mode = "static"
                static_params = self._generate_static_params()

            if is_wifi:
                wifi_params = self._generate_wifi_params()
            else:
                wifi_params = ""

            return res % (name, name, mode, static_params, wifi_params)


        if type_ == "external":
            pass

        if type_ == "unused":
            return "\n"

        return "\n"

    def to_wpa_supplicant_conf(self):
        skeleton = \
'''
ctrl_interface=/var/run/wpa_supplicant

network={
%s
}

'''
        wpa_params = ""

        name = self.netiface.name
        is_wifi = self.netiface.wifi_device
        type_ = self.netiface_type

        if not is_wifi:
            return ""

        sets = self.wifi_settings

        if not sets:
            raise Error(\
              "NetIface %s is a wifi device but no WiFi settings was found"
              % name)


        if sets.wpa_scan_ssid:
            wpa_params += "scan_ssid=1\n"
        else:
            wpa_params += "scan_ssid=0\n"

        ssid = ""
        if sets.ssid:
            ssid= sets.ssid
        wpa_params += 'ssid="%s"\n' % ssid


        if sets.wpa_key_mgmt=="NONE":
            wpa_psk = ""
            if sets.wpa_psk:
                wpa_psk= sets.wpa_psk
            wpa_psk = netutils.get_wpa_passphrase(\
                        ssid, wpa_psk)
            wpa_params += 'psk="%s"\n' % wpa_psk


        if sets.wpa_key_mgmt=="WPA-PSK":
            wpa_params += "key_mgmt=WPA-PSK\n"
            wpa_psk = ""
            if sets.wpa_psk:
                wpa_psk = sets.wpa_psk
            wpa_psk = netutils.get_wpa_passphrase(\
                        ssid, wpa_psk)
            wpa_params += 'psk="%s"\n' % wpa_psk

        return skeleton % wpa_params

    def to_dhcpd_conf(self):
        skeleton = \
'''
subnet %s netmask %s {
   interface %s

   ddns-update-style none;

%s

   pool {
        allow unknown-clients;
   }

}

'''
        dhcpd_params = ""

        name = self.netiface.name

        sets = self.dhcpd_settings

        if not sets:
            return ""

        if not sets.enabled:
            return ""

        if not self.net_settings:
            raise Error("NetIfaceProfile for %s NetIface is wrong configured"
                % name)

        subnet = get_str_or_empty_str(sets.subnet)
        if subnet == "":
            raise Error("DHCPD subnet is needed for %s NetIface"
                % name)
        netmask = get_str_or_empty_str(sets.netmask)
        if netmask == "":
            raise Error("DHCPD netmask is needed for %s NetIface"
                % name)

        if sets.authoritative:
            dhcpd_params += "option authoritative;\n"

        dns = get_str_or_empty_str(sets.dns)
        if dns != "":
            dhcpd_params += "option domain-name-servers " + dns + " ;\n"
        domain_name = get_str_or_empty_str(sets.domain_name)
        if domain_name != "":
            dhcpd_params += "option domain-name " + domain_name + " ;\n"

        routers = get_str_or_empty_str(sets.routers)
        if routers != "":
            dhcpd_params += "option routers " + routers + " ;\n"
        broadcast_address = get_str_or_empty_str(sets.broadcast_address)
        if broadcast_address != "":
            dhcpd_params += "option broadcast-address " + broadcast_address + " ;\n"
        default_lease_time = get_str_or_empty_str(sets.default_lease_time)
        if default_lease_time != "":
            dhcpd_params += "option default-lease-time " + default_lease_time + " ;\n"
        max_lease_time = get_str_or_empty_str(sets.max_lease_time)
        if max_lease_time != "":
            dhcpd_params += "option max_lease_time " + max_lease_time + " ;\n"




        return skeleton % (subnet,netmask,name,dhcpd_params)


    def to_hostapd_conf(self):
        skeleton = \
'''
interface=%s
ssid=%s
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=%s
wpa=2
wpa_passphrase=%s
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

'''
        hostapd_params = ""

        name = self.netiface.name
        is_wifi = self.netiface.wifi_device
        type_ = self.netiface_type

        if not is_wifi:
            return ""

        sets = self.wifi_settings

        if not sets:
            raise Error(\
              "NetIface %s is a wifi device but no WiFi settings was found"
              % name)

        if sets.wpa_scan_ssid:
            ignore_broadcast_ssid = "0"
        else:
            ignore_broadcast_ssid = "1"

        ssid = get_str_or_empty_str(sets.ssid)
        wpa_passphrase = get_str_or_empty_str(sets.wpa_psk)
        return skeleton % (name, ssid, ignore_broadcast_ssid, wpa_passphrase)

    def to_ntp_conf(self):
        skeleton = \
'''driftfile /var/lib/ntp/ntp.drift

statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable

server 0.ubuntu.pool.ntp.org
server 1.ubuntu.pool.ntp.org
%s

restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery
restrict 127.0.0.1
restrict ::1
'''
        profile = self

        if not profile.net_settings:
            return ""

        if not profile.net_settings.ntp1:
            ntp1 = ""
        else:
            ntp1 = profile.net_settings.ntp1

        if not profile.net_settings.ntp2:
            ntp2 = ""
        else:
            ntp2 = profile.net_settings.ntp2

        if ntp1 == "" and ntp2 == "":
            return ""

        servers = ""
        if ntp1 != "":
            servers = servers + "server " + ntp1 + "\n"
        if ntp2 != "":
            servers = servers + "server " + ntp2 + "\n"

        return skeleton % servers




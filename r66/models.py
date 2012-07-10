from django.db import models
from django.conf import settings
from r66 import netutils
from django.utils.translation import ugettext_lazy as _

PPP_MODE_CHOICES = [
    ('3g-only', _('3G only')),
    ('3g-pref', _('3G preference')),
    ('gprs-only', _('GPRS only')),
    ('gprs-pref', _('GPRS preference')),
    ('none', _('None')),
]

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

    metric = models.IntegerField(blank=True, null=True)

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

    broadcast_address = models.CharField(
            _("Broadcast address (broadcast-address)"),
            max_length=100,
            blank=True, null=True,)

    range_min = models.IPAddressField(blank=True, null=True)

    range_max = models.IPAddressField(blank=True, null=True)

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

    enabled_profile = models.ForeignKey('NetIfaceProfile',
            related_name='enabled_profile',
            blank=True, null=True,)

    name = models.CharField(max_length=10)
    description = models.TextField(max_length=150)

    def __unicode__(self):
        return self.name


    def get_enabled_profile(self):
        related_netiface_profiles = \
NetIfaceProfile.objects.filter(netiface=self)

        for r in related_netiface_profiles:
            if r.enabled:
                return r

        return None
        # raise Error("Netiface (%s) hasn't got any profile enabled"
        #             % self.name)



    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      self.wifi_device = netutils.is_wifi_interface(self.name)

      self.enabled_profile = self.get_enabled_profile()

      super(NetIface, self).save(*args, **kwargs)










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

      if self.netiface:

         self.netiface.enabled_profile = self
         self.netiface.save()

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


    def _generate_metric_params(self):
            name = self.netiface.name

            if not self.net_settings:
              raise Error("NetIfaceProfile for %s NetIface is wrong configured"
                % name)

            metric = get_str_or_empty_str(self.net_settings.metric)

            metric_params = ""

            if metric != "":
                metric_params += "metric %s\n" % str(metric)

            return metric_params


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
              metric = get_str_or_empty_str(self.net_settings.metric)
              if metric != "":
                  metric = " metric %s" % str(metric)
              static_params += "post-up ip route add default via " + gateway + metric + "\n"

              # static_params += "post-down ip rule delete table " + name + "\n"
              # static_params += "post-up ip rule add table " + name + " priority 32767\n"
              # static_params += "post-up ip route add default via " + gateway + " table " + name + metric + "\n"

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

            if self.netiface_type == "bridge" \
                    or self.netiface_type == "internal":
                params = ""
                params += \
                  "pre-up /usr/sbin/hostapd -B -P /var/run/hostapd_%s.pid %s/hostapd/%s.conf\n" \
                  % (name, settings.R66_ETC_DIR, name)
                params += \
                  "post-down kill -9 `cat /var/run/hostapd_%s.pid`" % (name)
                return params

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
                  "wpa-conf %s/wpa_supplicant/%s.conf\n" \
                  % (settings.R66_ETC_DIR, name)


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
%s
'''
            if is_wifi:
                wifi_params = self._generate_wifi_params()
            else:
                wifi_params = ""
            params = static_params + wifi_params
            return res % (name, name,params)

        if type_ == "internal":

            res = \
'''
auto %s
iface %s inet static
%s
'''
            metric_params = self._generate_metric_params()
            static_params = self._generate_static_params()
            if is_wifi:
                wifi_params = self._generate_wifi_params()
            else:
                wifi_params = ""
            params = metric_params + static_params + wifi_params
            return res % (name, name,params)

        if type_ == "external":

            res = \
'''
auto %s
iface %s inet %s
%s
%s
%s
'''
            metric_params = self._generate_metric_params()

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

            return res % (name, name, mode, metric_params, static_params, wifi_params)


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
            wpa_params += 'psk=%s\n' % wpa_psk

        return skeleton % wpa_params

    def to_dhcpd_conf(self):
        skeleton = \
'''
subnet %s netmask %s {
   interface %s;

   ddns-update-style none;

%s

        allow unknown-clients;

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
            dhcpd_params += "authoritative;\n"

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
            dhcpd_params += "default-lease-time " + str(default_lease_time) + " ;\n"
        max_lease_time = get_str_or_empty_str(sets.max_lease_time)
        if max_lease_time != "":
            dhcpd_params += "max-lease-time " + str(max_lease_time) + " ;\n"

        range_min = get_str_or_empty_str(sets.range_min)
        range_max = get_str_or_empty_str(sets.range_max)
        dhcpd_params += "range " + str(range_min) + " " + str(range_max)+ " ;\n"




        return skeleton % (subnet,netmask,name,dhcpd_params)


    def to_hostapd_conf(self):
        skeleton = \
'''
interface=%s
ssid=%s
channel=1
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














class NetPPP(models.Model):
    class Meta:
        verbose_name = '3G ppp'

    enabled=models.BooleanField(default=False)

    user = models.CharField(max_length=100,
            blank=True, null=True)
    password = models.CharField(max_length=100,
            blank=True, null=True)

    apn = models.CharField(max_length=100,
            blank=True, null=True)

    pin = models.CharField(max_length=10,
            blank=True, null=True)

    mode = models.CharField(_("Mode"),
            choices=PPP_MODE_CHOICES,
                        default='3g-pref',
                        max_length=100)

    def save(self, *args, **kwargs):
      get_status().mark_as_changed()

      super(NetPPP, self).save(*args, **kwargs)



    def to_peer(self):
        skeleton = '''
ttyUSB0
921600
lock
crtscts
modem
passive
novj
# defaultroute
noipdefault
usepeerdns
noauth
hide-password
persist
holdoff 10
maxfail 0
# debug

%s

connect "/usr/sbin/chat -v -t15 -f %s/ppp/r66.chat"

'''


        if not self.enabled:
            return ""

        peer_params = ""
        user = get_str_or_empty_str(self.user)
        if user != "":
            peer_params += 'user %s\n' % user
        password = get_str_or_empty_str(self.password)
        if password != "":
            peer_params += 'password %s\n' % password
        return skeleton % (peer_params, settings.R66_ETC_DIR)



    def to_chat(self):
        skeleton = '''
ABORT 'BUSY'
ABORT 'NO CARRIER'
ABORT 'VOICE'
ABORT 'NO DIALTONE'
ABORT 'NO DIAL TONE'
ABORT 'NO ANSWER'
ABORT 'DELAYED'
REPORT CONNECT
TIMEOUT 6
'' 'ATQ0'
'OK-AT-OK' 'ATZ'
TIMEOUT 3
'OK' '%s'
'OK\d-AT-OK' 'ATI'
'OK' 'ATZ'
'OK' 'ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0'
'OK' '%s'
'OK-AT-OK' 'AT+CGDCONT=1,"IP","%s"'
'OK' 'ATDT*99***1#'
TIMEOUT 30
CONNECT ''

'''


        if not self.enabled:
            return ""

        pin = get_str_or_empty_str(self.pin)
        if pin != "":
            pin = 'AT+CPIN=%s' % pin
        else:
            pin = 'AT'

        mode = get_str_or_empty_str(self.mode)
        if mode == "3g-pref":
            mode = "AT\^SYSCFG=2,2,3fffffff,0,1"
        if mode == "3g-only":
            mode = "AT\^SYSCFG=14,2,3fffffff,0,1"
        if mode == "gprs-pref":
            mode = "AT\^SYSCFG=2,1,3fffffff,0,0"
        if mode == "gprs-only":
            mode = "AT\^SYSCFG=13,1,3fffffff,0,0"
        if mode == "none":
            mode = "AT"

        apn = get_str_or_empty_str(self.apn)

        return skeleton % (pin,mode,apn)



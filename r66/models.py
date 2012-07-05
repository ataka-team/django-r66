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
    ('WPA-EAP', _('WPA-EAP')),
    ('WPA-PSK', _('WPA-PSK')),
    ('IEEE8021X', _('IEEE8021X')),
    ('NONE', _('NONE')),
]

WPA_PROTO_CHOICES = [
    ('WPA', _('WPA')),
    ('WPA2', _('WPA2')),
]

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


class Error(Exception):
    def __init__(self, value, _object):
        self.value = value
        self._object = _object
    def __str__(self):
        return str(self._object) + " - " + repr(self.value)


class Status(models.Model):
    class Meta:
        verbose_name = 'Network Configuration state'

    changed = models.BooleanField(default=False)

    def mark_as_changed():
        self.changed = True
        self.save()

    def unmark_as_changed():
        self.changed = False
        self.save()

    def to_dict():
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
    wpa_scan_ssid = models.PositiveIntegerField(
        blank=True, null=True)
    wpa_proto = models.CharField(max_length=30,
        choices=WPA_PROTO_CHOICES,
        blank=True, null=True)
    wpa_key_mgmt = models.CharField(max_length=30,
        choices=WPA_KEY_MGMT_CHOICES,
        blank=True, null=True)
    wpa_psk = models.CharField(max_length=250,
        blank=True, null=True)
    wpa_eap = models.CharField(
        choices=WPA_EAP_CHOICES,
        max_length=30,
        blank=True, null=True)
    wpa_pairwise = models.CharField(max_length=30,
        choices=WPA_PAIRWISE_CHOICES,
        blank=True, null=True)
    wpa_ca_cert = models.TextField(max_length=1000,
        blank=True, null=True)
    wpa_private_key  = models.TextField(max_length=1000,
        blank=True, null=True)
    wpa_private_key_passwd = models.TextField(max_length=1000,
        blank=True, null=True)
    wpa_identity = models.CharField(max_length=100,
        blank=True, null=True)
    wpa_password = models.CharField(max_length=100,
        blank=True, null=True)
    wpa_phase2 = models.TextField(max_length=1000,
        blank=True, null=True)


    # phase2="auth=MSCHAPV2"


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







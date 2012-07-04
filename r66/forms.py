import django.forms
from django.utils.translation import ugettext_lazy as _

from r66 import  models

class NetSettingsForm(django.forms.ModelForm):
    class Meta:
        model = models.NetSettings
        fields = ("dhcp", "masquerade")

class NetSettingsExtendedForm(django.forms.ModelForm):
    class Meta:
        model = models.NetSettings
        exclude = ("dhcp", "masquerade")

class WirelessSettingsForm(django.forms.ModelForm):
    class Meta:
        model = models.WirelessSettings

class DhcpdSettingsForm(django.forms.ModelForm):
    class Meta:
        model = models.DhcpdSettings

class NetIfaceProfileForm(django.forms.ModelForm):
    class Meta:
        model = models.NetIfaceProfile
        exclude = ('net_settings',
                   'wifi_settings',
                   'dhcpd_settings',
                   )


class NetBridgeProfileForm(django.forms.ModelForm):
    class Meta:
        model = models.NetBridgeProfile
        exclude = ('net_settings',
                   'dhcpd_settings',
                   )





class NNetIfaceProfileForm(django.forms.Form):

    enabled=django.forms.BooleanField()

    description = django.forms.CharField(max_length=150, widget=django.forms.widgets.Textarea())
    netiface = django.forms.ModelChoiceField(queryset=models.NetIface.objects.all())

    netiface_type = django.forms.ChoiceField(
            choices=models.NETIFACE_TYPE_CHOICES)

    bridge_profile = django.forms.ModelChoiceField(queryset=models.NetBridgeProfile.objects.all())



    ### net_settings

    # dynamic ip configuration
    dhcp = django.forms.BooleanField()


    ### internal mode attributes

    # masquerade configuration
    masquerade = django.forms.BooleanField()


    ### external & internal mode attributes

    # staticip configuration
    ip = django.forms.IPAddressField()
    netmask = django.forms.IPAddressField()
    dns1 = django.forms.IPAddressField()
    dns2 = django.forms.IPAddressField()
    gateway = django.forms.IPAddressField()
    ntp1 = django.forms.IPAddressField()
    ntp2 = django.forms.IPAddressField()


    ### END. net_settings





    ### BEGIN. wifi_settings

    wifi_enabled=django.forms.BooleanField()


    ssid = django.forms.CharField(max_length=30
        )


    # wpa
    wpa_scan_ssid = django.forms.IntegerField(
        )
    wpa_proto = django.forms.ChoiceField(
        choices=models.WPA_PROTO_CHOICES
        )
    wpa_key_mgmt = django.forms.ChoiceField(
        choices=models.WPA_KEY_MGMT_CHOICES
        )
    wpa_psk = django.forms.CharField(max_length=250
        )
    wpa_eap = django.forms.ChoiceField(
        choices=models.WPA_EAP_CHOICES
        )
    wpa_pairwise = django.forms.ChoiceField(
        choices=models.WPA_PAIRWISE_CHOICES
        )
    wpa_ca_cert = django.forms.CharField(max_length=1000
        )
    wpa_private_key  = django.forms.CharField(max_length=1000
        )
    wpa_private_key_passwd = django.forms.CharField(max_length=1000
        )
    wpa_identity = django.forms.CharField(max_length=100
        )
    wpa_password = django.forms.CharField(max_length=100
        )
    wpa_phase2 = django.forms.CharField(max_length=1000
        )


    # phase2="auth=MSCHAPV2"


    # wep
    wep_channel = django.forms.IntegerField(
            )

    # wep_mode = managed
    # wep_mode = django.forms.CharField(max_length=30
    #         )

    # wep_keymode = open
    wep_keymode = django.forms.ChoiceField(
            choices=models.WEP_KEYMODE_CHOICES
            )

    # wep_key1 = millavehexadecimal
    wep_key1 = django.forms.CharField(max_length=250
            )

    # wep_key2 = s:millaveascii
    wep_key2 = django.forms.CharField(max_length=250
            )

    wep_defaultkey = django.forms.IntegerField(
            )




    ### END. wifi_settings


    ### BEGIN. dhcpd_settings

    dhcpd_enabled=django.forms.BooleanField()

    dhcpd_authoritative=django.forms.BooleanField()

    dhcpd_dns = django.forms.CharField(
            max_length=100
            )

    dhcpd_domain_name = django.forms.CharField(
            max_length=100
            )

    dhcpd_subnet = django.forms.CharField(
            max_length=100
            )

    dhcpd_netmask = django.forms.CharField(
            max_length=100
            )

    dhcpd_routers = django.forms.CharField(
            max_length=100
            )

    dhcpd_broadcast_address = django.forms.CharField(
            max_length=100
            )

    dhcpd_default_lease_time = django.forms.IntegerField(
            )

    dhcpd_max_lease_time = django.forms.IntegerField(
            )


    ### END. dhcpd_settings

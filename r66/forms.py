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
        fields = ("enabled",)

class WirelessSettingsNoneForm(django.forms.ModelForm):
    class Meta:
        model = models.WirelessSettings
        fields = ("ssid",
                "wifi"
                )

class WirelessSettingsWpaForm(django.forms.ModelForm):
    class Meta:
        model = models.WirelessSettings
        fields = ("wpa_scan_ssid",
                "wpa_key_mgmt",
                "wpa_psk",
                )

class WirelessSettingsHostapdForm(django.forms.ModelForm):
    class Meta:
        model = models.WirelessSettings
        fields = (
                "ssid",
                "wpa_scan_ssid",
                "wpa_psk",
                )

class WirelessSettingsWepForm(django.forms.ModelForm):
    class Meta:
        model = models.WirelessSettings
        fields = (
                "wep_channel",
                "wep_keymode",
                "wep_key1",
                "wep_key2",
                "wep_defaultkey",
                )

class DhcpdSettingsForm(django.forms.ModelForm):
    class Meta:
        model = models.DhcpdSettings
        fields = ('enabled',
                   )

class DhcpdSettingsExtendedForm(django.forms.ModelForm):
    class Meta:
        model = models.DhcpdSettings
        exclude = ('enabled',
                   )


class NetIfaceProfileForm(django.forms.ModelForm):
    class Meta:
        model = models.NetIfaceProfile
        exclude = ('net_settings',
                   'wifi_settings',
                   'dhcpd_settings',
                   'bridge_profile',
                   )

class NetIfaceProfileExtendedForm(django.forms.ModelForm):
    class Meta:
        model = models.NetIfaceProfile
        fields = ('bridge_profile',
                   )


class NetBridgeProfileForm(django.forms.ModelForm):
    class Meta:
        model = models.NetBridgeProfile
        exclude = ('net_settings',
                   'dhcpd_settings',
                   )


class NetPPPForm(django.forms.ModelForm):
    class Meta:
        model = models.NetPPP




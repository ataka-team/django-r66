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




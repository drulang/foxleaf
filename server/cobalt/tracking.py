from django.conf import settings
from mixpanel import Mixpanel

mp = Mixpanel(settings.MIXPANEL_TOKEN)

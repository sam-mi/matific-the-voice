from django.conf import settings
from django.utils import timezone
from slugify import slugify
from the_voice.__init__ import __version__

def site_context(request):
    """
    Sitewide Context Processor
    """
    return {
        'SITE_NAME': settings.SITE_NAME,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'AUTHOR': settings.AUTHOR,
        'VERSION': __version__,
        # 'DASHBOARD_URL': settings.DASHBOARD_URL,
        # 'META': settings.META,
        'DEBUG': settings.DEBUG,
        'NOW': timezone.now(),
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'SITE_URL': settings.SITE_URL,
        'DATETIME_INPUT_FORMAT': 'F j, Y, g:i A', # JS
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
        'FACEBOOK_URL': slugify(settings.SITE_NAME),
        'TWITTER_URL': slugify(settings.SITE_NAME),
    }

from .models import SiteSettings


def site_logo(request):
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None

    return {
        'site_logo': settings
    }



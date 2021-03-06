import os
from django.conf import settings


DIV_PREFIX = getattr(
    settings, 'FLATPAGES_DIV_PREFIX', "django_staticpages_edit"
)
USE_TEMPLATE_DROPDOWN = getattr(
    settings, "FLATPAGES_USE_TEMPLATE_DROPDOWN", True
)
TEMPLATE_FILES_REGEXP = getattr(
    settings, 'FLATPAGES_ADMIN_REGEXP', r'.*\.d?html?'
)
USE_MINIFIED = getattr(
    settings, 'FLATPAGES_USE_MINIFIED', not getattr(settings, 'DEBUG')
)
TEMPLATE_DIR = getattr(
    settings, "FLATPAGES_TEMPLATE_DIR",
    os.path.join((settings.TEMPLATES[0]['DIRS'] if hasattr(settings,'TEMPLATES') else settings.TEMPLATE_DIRS)[0], 'flatpages')
)
USE_ADMIN_AREA_TINYMCE = getattr(settings, "FLATPAGES_TINYMCE_ADMIN", True)
USE_FRONTED_TINYMCE = getattr(settings, "FLATPAGES_TINYMCE_FRONTEND", True)

if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    MEDIA_URL = os.path.join(
        getattr(settings, 'STATIC_URL', ''), 'flatpages_tinymce'
    )
else:
    MEDIA_URL = getattr(
        settings, 'FLATPAGES_MEDIA_URL',
        os.path.join(settings.MEDIA_URL, 'flatpages_tinymce')
    )

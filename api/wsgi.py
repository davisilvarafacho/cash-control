import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
os.environ.setdefault('DJANGO_SECRET_KEY', '_tck0vm30&m2z6@b^08i9h(t_v4(ov$aezs$pzxa2z)$k0d82e')
os.environ.setdefault('DJANGO_DEBUG', 'False')

application = get_wsgi_application()

from django.conf import settings

API_MODULE = getattr(settings, 'API_MODULE', 'api')
API_HANDLER = getattr(settings, 'API_HANDLER', 'handlers')

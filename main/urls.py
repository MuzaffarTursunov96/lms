
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponseRedirect
from django.utils import translation

def redirect_to_default_language(request):
    language = translation.get_language_from_request(request)
    return HttpResponseRedirect(f'/{language}/')



urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', redirect_to_default_language),
    path('api-auth/', include('rest_framework.urls'))
    
]

# Language-prefixed URLs
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('lms.urls')),
    path('accounts/', include('account.urls')),
    path('quiz/', include('quiz.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
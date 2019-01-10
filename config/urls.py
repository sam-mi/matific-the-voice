from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import TemplateView, RedirectView
from django.views import defaults as default_views



admin.site.site_header = "The Voice"

urlpatterns = [

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # User management
    url(r'^users/', include(('the_voice.users.urls', 'users'), namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # url(r'^google49e555173b47eaf1.html',
    #     TemplateView.as_view(template_name='google49e555173b47eaf1.html')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [

    url(r'', include('legal.urls')),

    url(r'^favicon.ico$', RedirectView.as_view(
        url=staticfiles_storage.url('icons/favicons/favicon.ico'),
        permanent=True),
        name="favicon"
        ),
    url(r'^robots.txt$', RedirectView.as_view(
        url=staticfiles_storage.url('robots.txt'),
        permanent=True),
        name="robots_txt"
        ),


    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

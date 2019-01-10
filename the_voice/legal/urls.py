from django.conf.urls import url

from . import views

urlpatterns = [

    url('^terms-of-service/$',
        views.terms_of_service,
        name="terms-of-service"),

    url('^privacy-policy/$',
        views.privacy_policy,
        name="privacy-policy"),
]

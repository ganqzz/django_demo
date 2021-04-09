from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r"^$", views.Home.as_view(), name="home"),
    url(r"^admin/", admin.site.urls),
    url(r"^accounts/", include("accounts.urls")),
    url(r"^accounts/", include("django.contrib.auth.urls")),  # settings.LOGIN/LOGOUT_REDIRECT_URL
    url(r"^posts/", include("posts.urls")),
    url(r"^communities/", include("communities.urls")),
]
# urlpatterns += staticfiles_urlpatterns()

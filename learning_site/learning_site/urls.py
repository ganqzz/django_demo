from django.conf.urls import url, include
from django.contrib import admin
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import debug_toolbar

from rest_framework import routers

from review_api import views as api_views

from . import views
from . import settings

router = routers.DefaultRouter()
router.register(r'courses', api_views.CourseViewSet)
router.register(r'reviews', api_views.ReviewViewSet)

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),  # Debug Toolbar
    url(r'^admin/', admin.site.urls),
    url(r'^courses/', include('courses.urls')),
    url(r'^suggest/', views.suggestion_view, name="suggestion"),
    url(r'^$', views.home, name="home"),

    url(r'^api_top/$', api_views.top, name='api_top'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/v1/', include('review_api.urls')),
    url(r'^api/v2/', include((router.urls, 'apiv2',))),  # 2nd param: app_name
]

# DEBUG=Trueでのみ有効。開発中にSTATICFILES_DIRS以外を参照する場合のみ必要
# urlpatterns += staticfiles_urlpatterns('another_location')

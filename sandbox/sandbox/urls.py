from django.contrib import admin
from django.urls import path, include

import debug_toolbar

from . import views

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),  # Debug Toolbar
    path('admin/', admin.site.urls),

    path('', views.top, name='top'),
    path('', include('user_profile.urls')),  # no app_name
    path('forum/', include('forum.urls')),
    path('sandbox/', include('sbxapp.urls')),
    path('pizza/', include('pizza.urls')),
    path('teams/', include('teams.urls')),
    path('no_slash', views.trailing_slash),
    path('slash/', views.trailing_slash),
    path('params/', views.params),
]

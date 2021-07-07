from django.contrib import admin

from . import models

admin.site.register(models.DtDemo)
admin.site.register(models.Simple)
admin.site.register(models.Hash)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post)

admin.site.site_title = 'Sandbox Admin'
admin.site.site_header = 'Sandbox Admin Panel'
admin.site.index_title = 'Sandbox site administration'

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from login.models import *
# Register your models here.
admin.site.register(Clans)
admin.site.register(Quests)
admin.site.register(Users)


class characterAdmin(admin.ModelAdmin):

    list_per_page = 1500
   list_display = ('user_id','name','class_field','gender','health','level','experience','clan')
admin.site.register(Characters, characterAdmin)
   
    
class activeLoginsAdmin(admin.ModelAdmin):

    list_per_page = 1500
    list_display = ('user_id','session_key','character_id')
    readonly_fields = ('character_id','user_id')
admin.site.register(ActiveLogins, activeLoginsAdmin)


class itemsAdmin(admin.ModelAdmin):
    list_per_page = 1500
    list_display = ('character_id','slot','item','amount')
    readonly_fields = ('character_id',)
admin.site.register(Inventory, itemsAdmin)

	
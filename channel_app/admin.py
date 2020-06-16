from django.contrib import admin

# Register your models here.
# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class UtilisateurAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'photo', 'statut', 'date_add', 'date_upd')
    list_filter = (
        'user',
        'statut',
        'date_add',
        'date_upd',
        'id',
        'user',
        'photo',
        'statut',
        'date_add',
        'date_upd',
    )


class ChatAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'message',
        'statut',
        'date_add',
        'date_upd',
    )
    list_filter = (
        'user',
        'statut',
        'date_add',
        'date_upd',
        'id',
        'user',
        'message',
        'statut',
        'date_add',
        'date_upd',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Utilisateur, UtilisateurAdmin)
_register(models.Chat, ChatAdmin)

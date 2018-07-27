from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from nodes.models import BasicNode, ALNode


class MyAdmin(TreeAdmin):
    form = movenodeform_factory(BasicNode)


class ALNodeAdmin(TreeAdmin):
    form = movenodeform_factory(ALNode)


admin.site.register(BasicNode, MyAdmin)
admin.site.register(ALNode, ALNodeAdmin)

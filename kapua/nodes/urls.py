from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from nodes.views import SubTreeListView, TreeListView, move

router = DefaultRouter()


urlpatterns = [
    url('(?P<pk>[0-9])/subtree/', SubTreeListView.as_view()),
    url('nodes', TreeListView.as_view()),
    url('move', move),
    ]

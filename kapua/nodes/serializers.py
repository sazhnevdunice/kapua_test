from rest_framework import serializers

from nodes.models import ALNode


class ListALNodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ALNode
        fields = ('id', 'name', 'parent',)

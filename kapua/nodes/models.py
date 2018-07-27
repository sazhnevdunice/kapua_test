from django.db import models
from treebeard.al_tree import AL_Node
from treebeard.mp_tree import MP_Node


class BasicNode(MP_Node):
    name = models.CharField(max_length=30)

    node_order_by = ['name']

    def __str__(self):
        return 'Category: %s' % self.name


class ALNode(AL_Node):
    name = models.CharField(max_length=30)

    node_order_by = ['parent']
    parent = models.ForeignKey('self',
                               related_name='children_set',
                               null=True,
                               db_index=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name

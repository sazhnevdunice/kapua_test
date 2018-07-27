from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from nodes.models import ALNode
from nodes.serializers import ListALNodesSerializer


class SubTreeListView( generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    serializer_class = ListALNodesSerializer
    queryset = ALNode.objects.all()

    def list(self, request, *args, **kwargs):
        node_id = self.kwargs['pk']
        try:
            sbtree_root = ALNode.objects.get(id=node_id)
            data = ALNode.dump_bulk(parent=sbtree_root)
            return Response(data)
        except ALNode.DoesNotExist:
            return Response('Node with given id does not exist')


class TreeListView(generics.ListAPIView):
    serializer_class = ListALNodesSerializer
    queryset = ALNode.objects.all()


@transaction.non_atomic_requests
@api_view(http_method_names=['GET', 'POST'])
def move(request):
    if request.method == 'POST':
        node_id = request.data['node_id']
        target_id = request.data['target_id']

        node = ALNode.objects.get(id=node_id)
        target = ALNode.objects.get(id=target_id)
        node.move(target=target, pos='sorted-child')
        return Response("Node was moved")
    else:
        return Response("Pass node and target to move node")

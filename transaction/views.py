from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.models import APIRequestLog

from transaction.serializers import TransactionSerializer

class ListTransactionsView(APIView):
    serializer_class = TransactionSerializer
    model = APIRequestLog
    
    def get_queryset(self):
        return self.model.objects.all()
    
    def get(self, *args, **kwargs):
        transactions = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(transactions.data, status=status.HTTP_200_OK)
    
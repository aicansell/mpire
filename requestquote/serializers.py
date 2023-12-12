from rest_framework import serializers

from requestquote.models import RequestQuote

class RequestQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQuote
        fields = ['id', 'product', 'requestuser', 'message']
        
class RequestQuoteListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    requestuser = serializers.SerializerMethodField()
    vendorname = serializers.SerializerMethodField()
    
    class Meta:
        model = RequestQuote
        fields = ['id', 'product', 'requestuser', 'created_at', 'mark_read', 'message', 'vendorname']
    
    def get_product(self, obj):
        return obj.product.name
    
    def get_requestuser(self, obj):
        return obj.requestuser.get_full_name()
        
    def get_vendorname(self, obj):
        return obj.product.created_by.get_full_name()

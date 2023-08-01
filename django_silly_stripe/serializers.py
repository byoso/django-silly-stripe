from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.models import Price, Product

if dss_conf["AUTO_SET"] == "SPA":
    from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = [
            'id',
        ]


class PriceSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = '__all__'
        read_only_fields = [
            'id',
        ]

    def get_product(self, obj):
        serializer = ProductSerializer(obj.product)
        return serializer.data

import json

import stripe

from django.shortcuts import redirect
from django.http import (
    JsonResponse,
    )
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import permission_required


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.helpers import user_creates_new_customer
from django_silly_stripe.models import (
    Product,
    Price,
    Customer,
    Subscription,
    )
from django_silly_stripe.serializers import (
    PriceSerializer,
)


@api_view(['POST'])
def checkout(request):
    if not request.user.is_authenticated or not request.user.is_active:
        return JsonResponse({"message": "Permission denied"}, status=403)
    if request.method == 'POST':
        data = json.loads(request.body)
        # print("===data: ", data)
        price_id = data["priceId"]

        stripe.api_key = dss_conf["DSS_SECRET_KEY"]
        user = request.user
        if not hasattr(user, 'customer'):
            # print("===new_customer_data: ", new_customer_data)
            user_creates_new_customer(user)

        else:
            if dss_conf['SUBSCRIBE_ONLY_ONCE']:
                product = Price.objects.get(id=price_id).product
                if Subscription.objects.filter(
                        customer=user.customer,
                        product=product,
                        status='active',
                        ).exists():
                    return JsonResponse(
                        {"message": "You already have an active subscription"},
                        status=403,
                        )

        try:
            # print("===request.META['HTTP_HOST']: ", request.META['HTTP_HOST'])
            session = stripe.checkout.Session.create(
                customer=user.customer.id,
                success_url=dss_conf['SUCCESS_URL'],
                cancel_url=dss_conf['SUCCESS_URL'],
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    # For metered billing, do not pass quantity
                    'quantity': 1
                }],
            )
            # print('session id: ', session.id)
            # print('session : ', session)
        except Exception as e:
            # print(e)
            return JsonResponse(
                {"message": "Backend error in a stripe session creation"},
                status=500,
                )

        return JsonResponse(
            {
                "message": "Subscription parameters sent to build the checkout page",
                "url": session.url,
            },
            status=200,
            )


@api_view(['GET'])
def portal(request):
    # print("===portal")
    if not request.user.is_authenticated or not request.user.is_active:
        return JsonResponse({"message": "Permission denied"}, status=403)
    if request.method != 'GET':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    stripe.api_key = dss_conf["DSS_SECRET_KEY"]
    user = request.user
    if not hasattr(user, 'customer'):
        # print("===new_customer_data: ", new_customer_data)
        user_creates_new_customer(user)

    stripe.billing_portal.Configuration.create(
            business_profile={
                "headline": "Cactus Practice partners with Stripe for simplified billing.",
            },
            features={"invoice_history": {"enabled": True}},
        )

    session = stripe.billing_portal.Session.create(
        customer=user.customer.id,
        return_url=dss_conf['PORTAL_BACK_URL'],
    )
    return JsonResponse({'url': session.url}, status=200)


@api_view(['PUT'])
def subscription_cancel(request):
    # print("===subscription_cancel")
    if not request.user.is_authenticated or not request.user.is_active:
        return JsonResponse({"message": "Permission denied"}, status=403)
    if request.method == 'PUT':
        data = json.loads(request.body)
        # print("===data: ", data)
        sub_id = data["subId"]
        if not Subscription.objects.filter(id=sub_id).exists():
            return JsonResponse(
                {"message": "Subscription not found"},
                status=404,
                )
        if not Subscription.objects.get(id=sub_id).customer.user == request.user:
            return JsonResponse(
                {"message": "Permission denied"},
                status=403,
                )
        stripe.api_key = dss_conf["DSS_SECRET_KEY"]
        try:
            if dss_conf['SUBSCRIPTION_CANCEL'] == 'PERIOD':
                stripe.Subscription.modify(
                    sub_id,
                    cancel_at_period_end=True,
                    )
            elif dss_conf['SUBSCRIPTION_CANCEL'] == 'NOW':
                stripe.Subscription.delete(sub_id)
            else:
                return JsonResponse(
                    {"message": "Subscription cancelation mode not configured"},
                    status=500,
                    )

        except Exception as e:
            # print(e)
            return JsonResponse(
                {"message": "An error occured, please try again later."},
                status=500,
                )

        return JsonResponse(
            {"message": "Subscription canceled successfully."},
            status=200,
            )

# ====================================================================
# Additionnal views usable in your projects, you have to create the urls
# yourself.


@api_view(['GET'])
def get_plans(request):
    """List all plans, no authentication required"""
    prices = Price.objects.all()
    serializer = PriceSerializer(prices, many=True)

    return Response(serializer.data)

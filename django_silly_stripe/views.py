import json
from pprint import pprint

import stripe

from django.shortcuts import redirect
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponse,
    HttpResponseForbidden
    )
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.helpers import user_creates_new_customer
from django_silly_stripe.models import Product, Price
from django_silly_stripe.helpers import color as c

@csrf_exempt
def webhook(request):
    if request.method != 'POST':
        return HttpResponseBadRequest({"message": "Method not allowed"})
    stripe_payload = request.body
    print("===WEBHOOK: stripe_payload: ")
    pprint(stripe_payload)

    try:
        event = stripe.Event.construct_from(
        json.loads(stripe_payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def checkout(request):
    if not request.user.is_authenticated or not request.user.is_active:
        return HttpResponseForbidden({"message": "Permission denied"})
    if request.method == 'POST':
        data = json.loads(request.body)
        print("===data: ", data)
        price_id = data["priceId"]

        stripe.api_key = dss_conf["DSS_SECRET_KEY"]
        user = request.user
        if not hasattr(user, 'customer'):
            new_customer_data = stripe.Customer.create(
                email=request.user.email,
                name=request.user.username,
                metadata={
                    'user_id': request.user.id,
                }
            )
            print("===new_customer_data: ", new_customer_data)
            user_creates_new_customer(
                user,
                new_customer_data,
            )

        try:
            print("===request.META['HTTP_HOST']: ", request.META['HTTP_HOST'])
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
            print('session id: ', session.id)
            print('session : ', session)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest({"message": "Backend error in a stripe session creation"})

        return JsonResponse({
            "message": "Subscription parameters sent to build the checkout page",
            "url": session.url,
            })


@permission_required('is_superuser')
def initialize_dss_from_stripe(request):
    Product.objects.all().delete()
    Price.objects.all().delete()
    stripe.api_key = dss_conf["DSS_SECRET_KEY"]
    products = stripe.Product.list(limit=100)
    for product in products:
        new_product = Product(
            id=product.id,
            name=product.name,
            description=product.description,
            metadata=product.metadata,
            images=product.images,
            active=product.active,
        )
        new_product.save()
    prices = stripe.Price.list(limit=100)
    for price in prices:
        new_price = Price(
            id=price.id,
            product=Product.objects.get(id=price.product),
            unit_amount=price.unit_amount,
            currency=price.currency,
            recurring_interval=price.recurring['interval'],
            recurring_interval_count=price.recurring['interval_count'],
            metadata=price.metadata,
            active=price.active,
        )
        new_price.save()
    messages.add_message(
        request, messages.SUCCESS, (
            'Database succesfully updated from Stripe with products and prices'
            )
        )
    return redirect('admin:index')

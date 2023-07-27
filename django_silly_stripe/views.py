import json

import stripe

from django.shortcuts import redirect
from django.http import (
    JsonResponse,
    )
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.helpers import user_creates_new_customer
from django_silly_stripe.models import (
    Product,
    Price,
    Customer,
    Subscription,
    )


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


@csrf_exempt
def webhook(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    stripe_payload = request.body
    # print("===WEBHOOK: stripe_payload: ")
    # print(stripe_payload)

    try:
        event = stripe.Event.construct_from(
        json.loads(stripe_payload), stripe.api_key
        )
        # print("=== event type: ", event.type)
    except ValueError:
        # Invalid payload
        return JsonResponse({"message": "Invalid payload"}, status=400)

    # Handle the event
    match event.type:
        case "customer.subscription.updated":
            sub_id = event.data.object.id
            # print(event)
            if not Subscription.objects.filter(id=sub_id).exists():
                sub = Subscription(
                    id=sub_id,
                    customer=Customer.objects.get(id=event.data.object.customer),
                    product=Product.objects.get(id=event.data.object.plan.product),
                    status=event.data.object.status,
                    start_time=event.data.object.current_period_start,
                    end_time=event.data.object.current_period_end,
                    cancel_at_period_end=event.data.object.cancel_at_period_end,
                )
                sub.save()
            else:
                sub = Subscription.objects.get(id=sub_id)
                sub.status = event.data.object.status
                sub.start_time = event.data.object.current_period_start
                sub.end_time = event.data.object.current_period_end
                sub.cancel_at_period_end = event.data.object.cancel_at_period_end
                sub.save()

        case "customer.subscription.deleted":
            sub_id = event.data.object.id
            if Subscription.objects.filter(id=sub_id).exists():
                sub = Subscription.objects.get(id=sub_id)
                sub.delete()

        case _:
            # print('Unhandled event type {}'.format(event.type))
            pass

    return JsonResponse({"message": "event handeled"}, status=200)


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


# ======================================================================
# Admin interface views

@permission_required('is_staff')
def initialize_dss_from_stripe(request):
    """Initializer in the admin interface"""
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

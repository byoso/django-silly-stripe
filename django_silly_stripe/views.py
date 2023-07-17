
from django.http import JsonResponse, HttpResponseBadRequest
import stripe
import json

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.helpers import user_creates_new_customer


def checkout(request):
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
            )
            print("===new_customer_data: ", new_customer_data)
            user_creates_new_customer(
                user,
                new_customer_data,
            )

        try:
            print("===request.META['HTTP_HOST']: ", request.META['HTTP_HOST'])
            session = stripe.checkout.Session.create(
                customer=user.customer.stripe_id,
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

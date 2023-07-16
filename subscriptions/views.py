from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import stripe
import json

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf




def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("===data: ", data)
        price_id = data["priceId"]

        stripe.api_key = dss_conf["DSS_SECRET_KEY"]

        try:
            session = stripe.checkout.Session.create(
                customer='cus_OFZMIvPNMVVAsz',
                success_url='http://localhost:8000/',
                # success_url='https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:8000/',
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



# class CreateCheckoutSession(APIView):
#     def post(self, request):
#         price_id = request.data.get("priceId")

#         try:
#             session = stripe.checkout.Session.create(
#                 customer='cus_OFZMIvPNMVVAsz',
#                 success_url='http://localhost:8080/?#/account',
#                 # success_url='https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url='http://localhost:8080/?#/account',
#                 mode='subscription',
#                 line_items=[{
#                     'price': price_id,
#                     # For metered billing, do not pass quantity
#                     'quantity': 1
#                 }],
#             )
#             print('session id: ', session.id)
#             print('session : ', session)
#         except Exception as e:
#             print(e)
#             return Response({"message": "Backend error in a stripe session creation"}, 400)

#         return Response({"message": "Subscription parameters sent to build the checkout page"})

#     def get(self, request):
#         pass


# class Webhook(APIView):

#     def post(self, request):
#         print("=== webhook POST===")
#         print(request.data)
#         return Response({"message": "webhook received"})

#     def get(self, request):
#         print("=== webhook GET ===")
#         print(request.data)
#         return Response({"message": "webhook received"})

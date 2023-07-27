import stripe

from django.urls import path
from django.http import HttpResponseServerError
from django.contrib.auth import get_user_model

from . import views
from .conf import SILLY_STRIPE as dss_conf
from django.db.models.signals import pre_save
from .models import Customer

urlpatterns = [
    path(
        dss_conf['DSS_PREFIX']+'initialize_dss_from_stripe/',
        views.initialize_dss_from_stripe,
        name='initialize_dss_from_stripe'
        )
]

if dss_conf['USE_CHECKOUT']:
    urlpatterns += [
        path(dss_conf['DSS_PREFIX']+'checkout/', views.checkout, name='dss_checkout'),
    ]

if dss_conf['USE_SUBSCRIPTIONS_CANCEL']:
    urlpatterns += [
        path(
            dss_conf['DSS_PREFIX']+'subscription_cancel/',
            views.subscription_cancel,
            name='dss_subscription_cancel'
            ),
    ]

if dss_conf['USE_WEBHOOK']:
    urlpatterns += [
        path(dss_conf['DSS_PREFIX']+'webhook/', views.webhook, name='dss_webhook'),
    ]

if dss_conf['USE_PORTAL']:
    urlpatterns += [
        path(dss_conf['DSS_PREFIX']+'portal/', views.portal, name='dss_portal'),
    ]

# Signal on user's email updated changes stripe customer's email

User = get_user_model()


def user_email_update_customer(sender, instance, **kwargs):
    """Sends an update to stripe when a user's
    email is changed.
    """
    if Customer.objects.filter(user=instance).exists() and \
            (instance.email != instance.customer.email
             or instance.username != instance.customer.name):
        try:
            db_customer = Customer.objects.get(user=instance)
            stripe.api_key = dss_conf["DSS_SECRET_KEY"]
            stripe_customer = stripe.Customer.modify(
                db_customer.id,
                email=instance.email,
                name=instance.username,
                )
            db_customer.email = stripe_customer.email
            db_customer.name = stripe_customer.name
            db_customer.save()

        except stripe.error.StripeError:
            return HttpResponseServerError(
                "Service unavailable. Please try again later."
            )


pre_save.connect(user_email_update_customer, sender=User)

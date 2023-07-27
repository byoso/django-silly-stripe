import stripe

from .models import Customer
from django.db.models import Q
from django.db.models import QuerySet


from .conf import SILLY_STRIPE as dss_conf


def user_creates_new_customer(user):
    """If a user does not have a customer, creates one.
    Returns the user."""
    if hasattr(user, 'customer'):
        return user
    stripe.api_key = dss_conf["DSS_SECRET_KEY"]
    new_customer_data = stripe.Customer.create(
        email=user.email,
        name=user.username,
        metadata={
            'user_id': user.id,
        }
    )
    new_customer = Customer(
        id=new_customer_data.id,
        user=user,
    )
    new_customer.save()
    user.save()
    return user


def get_user_subscriptions(user):
    try:
        subscriptions = user.customer.subscriptions.filter(
            Q(status="active") | Q(status="trialing")
        )
    except AttributeError:
        subscriptions = None
    return subscriptions

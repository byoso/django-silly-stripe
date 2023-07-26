
from .models import Customer, Subscription
from django.db.models import Q

# color parameters: style;background (30 is none);foreground
color = {
    "end": "\x1b[0m",
    "info": "\x1b[0;30;36m",
    "success": "\x1b[0;30;32m",
    "warning": "\x1b[0;30;33m",
    "danger": "\x1b[0;30;31m",
}

DSS_CONFIG_ERROR = (
    f"{color['warning']}DJANGO-SILLY-STRIPE IS NOT CONFIGURED PROPERLY."
    "\nCheck the configuration in the admin panel."
    f"{color['end']}"

    )


def user_creates_new_customer(user, data):
    new_customer = Customer(
        id=data["id"],
        user=user,
    )
    new_customer.save()
    user.save()
    return user


def get_user_subscriptions(user):
    subscriptions = user.customer.subscriptions.filter(
        Q(status="active") | Q(status="trialing")
    )
    return subscriptions

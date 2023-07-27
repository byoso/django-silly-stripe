

import stripe
from stripe.error import AuthenticationError, InvalidRequestError
from django.conf import settings

# from .models import StripeConfig, SillyStripeConfig

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


SILLY_STRIPE = {
    # Basic settings
    'DSS_SECRET_KEY': 'sk_xxxxxx',
    'DSS_PUBLIC_KEY': 'pk_xxxxxx',
    'DSS_RESTRICTED_KEY': 'rk_xxxxxx',  # optionnal
    'DSS_WEBHOOK_SECRET': 'wk_xxxxxx',
    'DSS_PREFIX': 'dss/',
    # Django Silly Stripe Endpoints
    'USE_CHECKOUT': True,
    'USE_SUBSCRIPTIONS_CANCEL': True,
    'USE_WEBHOOK': True,
    'USE_PORTAL': True,
    # Checkout settings
    'SUCCESS_URL': 'https://example.com/checkout_success',
    'CANCEL_URL': 'https://example.com/checkout_cancel',
    # Subscriptions settings
    'SUBSCRIPTION_CANCEL': 'PERIOD',  # 'PERIOD' or 'NOW' (beware with 'NOW': no refund)
    'SUBSCRIBE_ONLY_ONCE': True,
    # Portal settings
    'PORTAL_BACK_URL': 'https://example.com/back_from_portal',
}

for key in settings.SILLY_STRIPE:
    SILLY_STRIPE[key] = settings.SILLY_STRIPE[key]



import stripe
from stripe.error import AuthenticationError, InvalidRequestError
from django.conf import settings

from .helpers import DSS_CONFIG_ERROR
# from .models import StripeConfig, SillyStripeConfig


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



import stripe
from stripe.error import AuthenticationError, InvalidRequestError
from django.conf import settings

from .helpers import DSS_CONFIG_ERROR
# from .models import StripeConfig, SillyStripeConfig


SILLY_STRIPE = {
      'DSS_PREFIX': 'dss/',
      'USE_CHECKOUT': True,
      'SUCCESS_URL': None,
      'CANCEL_URL': None,
}

for key in settings.SILLY_STRIPE:
    SILLY_STRIPE[key] = settings.SILLY_STRIPE[key]



import stripe
from stripe.error import AuthenticationError, InvalidRequestError
from django.conf import settings

from .helpers import DSS_CONFIG_ERROR
# from .models import StripeConfig, SillyStripeConfig


SILLY_STRIPE = {
}

for key in settings.SILLY_STRIPE:
    SILLY_STRIPE[key] = settings.SILLY_STRIPE[key]

# if not SillyStripeConfig.objects.all().exists():
#     silly_stripe_config = SillyStripeConfig.objects.create()
# else:
#     silly_stripe_config = SillyStripeConfig.objects.first()


def check_stripe_configuration(config_name):
    # if config_name is None or \
    #         not StripeConfig.objects.filter(name=config_name).exists():
    #     print(DSS_CONFIG_ERROR)
    #     return

    # stripe_config = StripeConfig.objects.get(name=config_name)
    # try:
    #     stripe.api_key = stripe_config.secret_key
    #     stripe.Customer.list()
    # except AuthenticationError:
    #     print(DSS_CONFIG_ERROR)
        return

    # Do stuff here

    # print('=== Customers: ', stripe.Customer.list())
    # print('=== Products: ', stripe.Product.list())
    # print('=== Prices: ', stripe.Price.list())


# if silly_stripe_config.run_config:
#     check_stripe_configuration(silly_stripe_config.config_name)

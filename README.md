# Django Silly Stripe

It is a wrapper based on the use of python's stripe API. The aim is
to make it as simple as possible to use.

For now, only stripe checkout is supported, in order to handle subscriptions
only.

## Installation

`pip install django-silly-stripe`

`./manage.py migrate`

**settings.py**
```python
INSTALLED_APPS = [
    'django_silly_stripe',  # <-- BEFORE admin>

    # ...
]


SILLY_STRIPE = {
    # keys (should be imported from environment)
    'DSS_SECRET_KEY': 'sk_xxxxxx'
    'DSS_PUBLIC_KEY': 'pk_xxxxxx',
    'DSS_RESTRICTED_KEY': 'rk_xxxxxx',  # optionnal
    'DSS_WEBHOOK_SECRET': 'wk_xxxxxx',
    # ... read the wiki to see more options
}

```

**urls.py**
```python

urlpatterns = [
    # ...
    path('', include('django_silly_stripe.urls')),
]
```

### Once you have created your products (and prices) witin stripe online:
Go in the admin interface, and press the big green button
"Stripe: get prices & products" to populate the database with them.


### Read the wiki to integrate DSS within your application
[wiki](https://github.com/byoso/django-silly-stripe/wiki)

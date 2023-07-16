# Django Silly Stipe

**WIP: not ready to use**

It is a wrapper based on the use of python's stripe API. The aim is
to make it as simple as possible to use.

## Installation

`pip install django-silly-stripe`

**settings.py**
```python
INSTALLED_APPS = [
    # ...
    'django_silly_stripe',
]

SILLY_STRIPE = {
    'config_name': 'test' # or whatever name your first config will be
}

```

**urls.py**
```python

urlpatterns = [
    # ...
    path('stripe/', include('django_silly_stripe.urls')),
]
```

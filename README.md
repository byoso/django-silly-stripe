# Django Silly Stripe

**WIP: not ready to use**

It is a wrapper based on the use of python's stripe API. The aim is
to make it as simple as possible to use.

For now, only stripe checkout is supported, with less then 100 products
and 100 prices. Good to make subscriptions easily, but nothing too fancy.

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



## Classic Django usage

In a classic template
**some_page.html**
```html
<script>
let subscribe = document.getElementById('subscribe');
document.addEventListener('DOMContentLoaded', () => {
  subscribe.addEventListener('click', () => {
    axios({
      method: 'post',
      url: '{% url "dss_checkout" %}',
      data: {
        // the price id should be given via the context of the view,
        // not hard coded like here
        'priceId': 'price_1NT4BqCyzfytDBEqarffvBjA',
      },
      headers: {
        'X-CSRFToken': '{{ csrf_token }}',
      }
    }).then(response => {
      console.log(response.data);
      window.location.href = response.data.url;
    }).catch(error => {
      console.log(error);
    })
  });
});

</script>

```

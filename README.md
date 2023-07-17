# Django Silly Stipe

**WIP: not ready to use**

It is a wrapper based on the use of python's stripe API. The aim is
to make it as simple as possible to use.

For now, only stripe checkout is supported.

## Installation

`pip install django-silly-stripe`

**settings.py**
```python
INSTALLED_APPS = [
    # ...
    'django_silly_stripe',
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

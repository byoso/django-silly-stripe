from .conf import SILLY_STRIPE as dss_conf
from django.urls import path
from . import views


urlpatterns = [
]

if dss_conf['USE_CHECKOUT']:
    urlpatterns += [
        path(dss_conf['DSS_PREFIX']+'checkout/', views.checkout, name='dss_checkout'),
    ]

from rest_framework import routers
from django.urls import path

from .api import EnterpriseViewSet, EnterprisePartnerView, EnterprisePotentialView, ConventionViewSet, EnterpriseGET

router = routers.DefaultRouter()
router.register('enterprise', EnterpriseViewSet, 'enterprise')
router.register('convention', ConventionViewSet, 'convention')

urlpatterns = router.urls

urlpatterns += [
    path('enterprise/partner', EnterprisePartnerView.as_view()),
    path('enterprise/potential', EnterprisePotentialView.as_view()),
    path('enterprise/register', EnterpriseGET.as_view()),

]

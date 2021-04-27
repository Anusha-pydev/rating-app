from apis import views
from django.urls import path

urlpatterns = [
    path(
        "calculate-premium/",
        views.CalculatePremiumView.as_view(),
        name="calculate-premium",
    ),
]

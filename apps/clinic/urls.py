from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.clinic import views

router = DefaultRouter()
router.register(r"medical-chart", views.MedicalChartViewSet, basename="StaticMenu")
router.register(r"record", views.RecordViewSet, basename="StaticMenu")
router.register(r"form", views.FormViewSet, basename="StaticMenu")
router.register(r"question", views.QuestionViewSet, basename="StaticMenu")
router.register(r"answer", views.AnswerViewSet, basename="StaticMenu")

urlpatterns = [
    path("api/", include(router.urls)),
]

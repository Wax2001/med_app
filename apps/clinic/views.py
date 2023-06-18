from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.clinic import serializers
from apps.clinic import models


@swagger_auto_schema(request_body=serializers.MedicalChartSerializer)
class MedicalChartViewSet(viewsets.ModelViewSet):
    queryset = models.MedicalChart.objects.all()
    serializer_class = serializers.MedicalChartSerializer

    # @swagger_auto_schema(
    #     operation_description="Get average stats",
    #     operation_summary="Get average stats",
    # )
    # @action(detail=True, methods=["post"])
    # def average_stats(self, request, pk=None):



@swagger_auto_schema(request_body=serializers.RecordSerializer)
class RecordViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
    action_serializers = {
        "create": serializers.CreateRecordSerializer,
        "list": serializers.DetailRecordSerializer,
        "retrieve": serializers.DetailRecordSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(RecordViewSet, self).get_serializer_class()

    @swagger_auto_schema(
        operation_description="Create record",
        operation_summary="Create record",
        request_body=serializers.CreateRecordSerializer,
    )
    def create(self, request):
        serializer = serializers.CreateRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = models.Record.objects.create(medical_chart=serializer.validated_data.get("medical_chart"))
        for answer in serializer.validated_data.get("answers"):
            answer["record"] = record
            models.Answer.objects.create(**answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_description="List record",
        operation_summary="List record",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Retrieve record",
        operation_summary="Retrieve record",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@swagger_auto_schema(request_body=serializers.FormSerializer)
class FormViewSet(viewsets.ModelViewSet):
    queryset = models.Form.objects.all()
    serializer_class = serializers.FormSerializer


@swagger_auto_schema(request_body=serializers.QuestionSerializer)
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


@swagger_auto_schema(request_body=serializers.AnswerSerializer)
class AnswerViewSet(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

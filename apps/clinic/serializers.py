from django.utils import timezone
from rest_framework import serializers

from apps.clinic import models


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Record
        fields = "__all__"


class CreateAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=models.Question.objects.all(), required=True)
    text = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
    number = serializers.FloatField(required=False)

    class Meta:
        model = models.Answer
        fields = (
            "question",
            "text",
            "date",
            "number",
        )


class CreateRecordSerializer(serializers.ModelSerializer):
    medical_chart = serializers.PrimaryKeyRelatedField(queryset=models.MedicalChart.objects.all(), required=True)
    answers = serializers.ListField(child=CreateAnswerSerializer(), required=True)

    class Meta:
        model = models.Record
        fields = (
            "medical_chart",
            "answers",
            "id",
        )

    def validate(self, attrs):
        if not attrs.get("answers"):
            raise serializers.ValidationError("Answers are required")
        
        med_chart = attrs.get("medical_chart")
        question = attrs.get("answers")[0].get("question")

        if question.form.age_from and (timezone.now().date() - med_chart.birth_date).days/365 < question.form.age_from:
            raise serializers.ValidationError("Age is not in range")
        
        if question.form.age_to and (timezone.now().date() - med_chart.birth_date).days/365 > question.form.age_to:
            raise serializers.ValidationError("Age is not in range")

        for answer in attrs.get("answers"):
            if answer.get("question").form != question.form:
                raise serializers.ValidationError("Questions are not in the same form")
            
            for type in models.Question.types:
                if answer.get(type) is not None and answer.get("question").type != type:
                    raise serializers.ValidationError(f"You can't choose {type} for this question")
            
            if answer.get("date") and answer.get("date") > timezone.now().date():
                raise serializers.ValidationError("You can't choose future dates")
            
            if answer.get("number"):
                if answer.get("question").lower_bound and answer.get("number") < answer.get("question").lower_bound:
                    raise serializers.ValidationError("Number is not in range")
                if answer.get("question").upper_bound and answer.get("number") > answer.get("question").upper_bound:
                    raise serializers.ValidationError("Number is not in range")
        
        return super().validate(attrs)


class DetailAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = (
            "question_id",
            "question_text",
            "response",
        )


class DetailRecordSerializer(serializers.ModelSerializer):
    answers = DetailAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Record
        fields = (
            "medical_chart",
            "created_at",
            "answers",
            "id",
        )


class MedicalChartSerializer(serializers.ModelSerializer):
    records = DetailRecordSerializer(many=True, read_only=True)

    class Meta:
        model = models.MedicalChart
        fields = (
            # "average_stats",
            "name",
            "surname",
            "birth_date",
            "records",
            "id",
            "created_at",
        )


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = "__all__"

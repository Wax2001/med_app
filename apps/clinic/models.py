from django.db import models
from uuid import uuid4


class BaseMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


class MedicalChart(BaseMixin):
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class Record(BaseMixin):
    medical_chart = models.ForeignKey(MedicalChart, on_delete=models.CASCADE, related_name='records')


class Form(BaseMixin):
    name = models.CharField(max_length=255, null=True, blank=True)
    age_from = models.IntegerField(null=True, blank=True)
    age_to = models.IntegerField(null=True, blank=True)


class Question(BaseMixin):
    DATE = "date"
    TEXT = "text"
    NUMBER = "number"

    types = [DATE, TEXT, NUMBER]

    response_type_choices = [
        (DATE, "Date"),
        (TEXT, "Text"),
        (NUMBER, "Number"),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=response_type_choices, default=TEXT)
    lower_bound = models.IntegerField(null=True, blank=True)
    upper_bound = models.IntegerField(null=True, blank=True)


class Answer(BaseMixin):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)

    @property
    def question_text(self):
        return self.question.text
    
    @property
    def response(self):
        return self.text or self.date or self.number

import coreapi
from rest_framework import filters


class QuestionFilter(filters.BaseFilterBackend):
    
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="form",
                location="query",
                required=False,
                type="str",
                description="Form id",
            ),
        ]
    
    def filter_queryset(self, request, queryset, view):
        if not queryset:
            return queryset
        
        if request.query_params.get("form"):
            return queryset.filter(form_id=request.query_params.get("form"))
        return queryset
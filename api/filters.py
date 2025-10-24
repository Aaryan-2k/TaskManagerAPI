import django_filters
from task.models import TaskModel

class TaskFilter(django_filters.FilterSet):
    is_completed=django_filters.BooleanFilter(field_name='completed')
    class Meta:
        model=TaskModel
        fields=['is_completed',]


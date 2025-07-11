from django.contrib import admin

# Register your models here.

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm, ChoiceInlineFormset
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    form = ChoiceForm
    formset = ChoiceInlineFormset


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline, )
    list_display = ['html', 'is_published']
    list_filter = ['is_published']
    search_fields = ['html', 'choices__html']
    actions = None
    form = QuestionForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True  # Always allow editing



admin.site.register(Question, QuestionAdmin)

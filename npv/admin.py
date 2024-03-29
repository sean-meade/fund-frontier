from django.contrib import admin
from .models import Evaluation, Project

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('name' , 'discount_rate')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'evaluation', 'initial_investment', 'period',
        'npv', 'payback_period', 'annualized_npv', 'consider_further', 'rank',
    )
    list_filter = ('evaluation', 'consider_further', 'period',)
    search_fields = ('name', 'evaluations__name', )

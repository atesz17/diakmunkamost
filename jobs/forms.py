from django import forms

from .models import Job


class AllJobSearchForm(forms.Form):

    ORDER_BY_LIST = [
        (0, 'Fizetés szerint növekvő'),
        (1, 'Fizetés szerint csökkenő')
    ]

    job_types = forms.MultipleChoiceField(
        choices=Job.JOB_TYPES,
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
        label='Munka típusa')
    min_salary = forms.IntegerField(
        required=False,
        label='Minumum órabér (Ft/óra)')
    order_by = forms.ChoiceField(
        choices=ORDER_BY_LIST,
        widget=forms.widgets.RadioSelect,
        label="Rendezés fizetés szerint",
    )

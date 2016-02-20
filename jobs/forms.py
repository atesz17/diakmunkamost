from django import forms

from .models import JobType


class AllJobSearchForm(forms.Form):

    NOVEKVO = 0
    CSOKKENO = 1

    ORDER_BY_LIST = [
        (NOVEKVO, 'Fizetés szerint növekvő'),
        (CSOKKENO, 'Fizetés szerint csökkenő')
    ]

    job_types = forms.ModelMultipleChoiceField(
        queryset=JobType.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False,
        label='Munka típusa'
    )
    min_salary = forms.IntegerField(
        required=False,
        label='Minumum órabér (Ft/óra)'
    )
    order_by = forms.ChoiceField(
        choices=ORDER_BY_LIST,
        initial=CSOKKENO,
        widget=forms.widgets.RadioSelect,
        label="Rendezés fizetés szerint",
    )

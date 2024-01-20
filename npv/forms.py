from django import forms
from django.core.validators import MaxValueValidator

class NPV_Form(forms.Form):
    initial_investment = forms.FloatField(label="Initial investment")
    #this limits it to 100%
    discount_rate = forms.FloatField(label="Discount Rate", validators=[MaxValueValidator(100)])
    cash_flow_year_1 = forms.FloatField()
    cash_flow_year_count = forms.FloatField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(NPV_Form, self).__init__(*args, **kwargs)
        self.fields['cash_flow_year_count'].initial = 1

        for index in range(2, int(extra_fields) + 1):
            self.fields['cash_flow_year_{index}'.format(index=index)] = \
                forms.FloatField()
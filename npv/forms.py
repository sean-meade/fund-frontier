from django import forms

class NPV_Form(forms.Form):
    initial_investment = forms.FloatField(label="Initial investment")
    discount_rate = forms.FloatField(label="Discount Rate")
    cash_flow_year_1 = forms.FloatField()
    cash_flow_year_count = forms.FloatField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(NPV_Form, self).__init__(*args, **kwargs)
        self.fields['cash_flow_year_count'].initial = extra_fields  # Set to the number of cash flows

        for index in range(2, int(extra_fields)):  # start from 2 to extra_fields inclusive
            # generate extra fields in the number specified via extra_fields
            self.fields[f'cash_flow_year_{index}'] = forms.FloatField()  # Use f-string for cleaner syntax

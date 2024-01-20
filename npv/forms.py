from django import forms


class NPV_Form(forms.Form):
    # TODO: Limit discount_rate to be max 100%
    initial_investment = forms.FloatField(label="Initial investment")
    discount_rate = forms.FloatField(label="Discount Rate")
    cash_flow_year_1 = forms.FloatField()
    cash_flow_year_count = forms.FloatField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(NPV_Form, self).__init__(*args, **kwargs)
        self.fields['cash_flow_year_count'].initial = 1

        for index in range(2, int(extra_fields) + 1):
            # generate extra fields in the number specified via extra_fields
            self.fields[f'cash_flow_year_{index}'] = forms.FloatField()  # Use f-string for cleaner syntax

class ContactForm(forms.Form):
    # Define your form fields here
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


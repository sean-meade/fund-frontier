from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class Evaluation_Form(forms.Form):
    evaluation_name = forms.CharField(label="Evaluation Name")
    discount_rate = forms.FloatField(label="Discount Rate", validators=[MaxValueValidator(100), MinValueValidator(0)])
    note = forms.CharField(label="Note")


class Project_Form(forms.Form):
    initial_investment = forms.FloatField(label="Initial investment")
    project_name = forms.CharField(label="Project Name")
    #TODO: add seperate cash flow per project
    cash_flow_year_1 = forms.FloatField()
    cash_flow_year_count = forms.FloatField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(Project_Form, self).__init__(*args, **kwargs)
        self.fields['cash_flow_year_count'].initial = 1

        for index in range(2, int(extra_fields) + 1):

            self.fields['cash_flow_year_{index}'.format(index=index)] = \
                forms.FloatField()
            # generate extra fields in the number specified via extra_fields
            self.fields[f'cash_flow_year_{index}'] = forms.FloatField()  # Use f-string for cleaner syntax

class ContactForm(forms.Form):
    # Define your form fields here
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)



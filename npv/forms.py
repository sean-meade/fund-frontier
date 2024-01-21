from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class Evaluation_Form(forms.Form):
    evaluation_name = forms.CharField(label="Evaluation Name")
    discount_rate = forms.FloatField(label="Discount Rate(%)", widget=forms.NumberInput(attrs={'type': 'number', 'step': '0.01', 'class': 'percentage'}), validators=[MaxValueValidator(100), MinValueValidator(0)])
    note = forms.CharField(label="Note(optional)", required=False)


class Project_Form(forms.Form):
    initial_investment = forms.FloatField(label="Initial investment", widget=forms.NumberInput(attrs={'type': 'number', 'class': 'currency'}))
    project_name = forms.CharField(label="Project Name")
    cash_flow_year_1 = forms.FloatField(label = "Cash flow year 1 $", widget=forms.NumberInput(attrs={'type': 'number', 'class': 'currency'}))
    cash_flow_year_count = forms.FloatField(widget=forms.HiddenInput())

    
    def __init__(self, *args, **kwargs):
        # set extra to zero this is then passed to the view when you're collecting the form data
        # e.g. form = Project_Form(request.POST, extra=request.POST.get('cash_flow_year_count', 0))
        extra_fields = kwargs.pop('extra', 0)

        # when the form is initialized set the count to 1
        super(Project_Form, self).__init__(*args, **kwargs)
        self.fields['cash_flow_year_count'].initial = 1

        # For all of the extra fields
        for index in range(2, int(extra_fields) + 1):

            # Make sure the newly added cash flows are floats
            self.fields[f'cash_flow_year_{index}'] = forms.FloatField()

class ContactForm(forms.Form):
    # Define your form fields here
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


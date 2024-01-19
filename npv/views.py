from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evaluation, Project
from .forms import NPV_Form, ContactForm

# Utility functions
def calculate_NPV(cash_flows, discount_rate):
    """
    Calculate the Net Present Value (NPV) of a series of cash flows.
    """
    npv = sum(cashflow / ((1 + discount_rate)**t) for t, cashflow in enumerate(cash_flows))
    return npv

# Views
def base(request):
    context = {'some_key': 'some_value'}  # Replace with actual context data
    return render(request, 'base.html', context)

def about(request):
    context = {'some_key': 'some_value'}  # Replace with actual context data
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            pass  # Implement the action
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required
def calculate_NPV_form(request):
    if request.method == "POST":
        form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count', 0))
        if form.is_valid():
            evaluation = get_object_or_404(Evaluation, pk=1)  # Assuming an Evaluation instance exists with id=1
            # ... rest of your existing code ...
    else:
        form = NPV_Form()
    return render(request, "npv/calculate-npv.html", {"form": form})

@login_required
def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})
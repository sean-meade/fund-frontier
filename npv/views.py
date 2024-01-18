from django.shortcuts import render, get_object_or_404
from .models import Evaluation, Project
from .forms import NPV_Form
from django.contrib.auth.decorators import login_required

def calculate_NPV(cash_flows, discount_rate):

    """
    Input parameters:
        cash_flows (list of floats and/or ints): cash flows in (negative) and out (positive) of investment
        discount_rate (float): float representing the discount rate percentage (it represents the rate at which future cash flows are adjusted to their present value)

    Output:
        npv (float or int): Net Present Value - metric used to evaluate the profitability of an investment or project.
    """

    # set variable to hold npv value
    npv = 0

    for t, cashflow in enumerate(cash_flows):
        # sum each of the cash flows together for their respective time period (t)
        npv = npv + cashflow/((1 + discount_rate)**t)

    return npv


def calculate_NPV_form(request):
    if request.method == "POST":
        form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count', 0))
        if form.is_valid():
            # Fetch or create an Evaluation instance
            # For simplicity, let's fetch an existing Evaluation (you might want to create or select one based on your form)
            evaluation = get_object_or_404(Evaluation, pk=1)  # assuming there's an Evaluation with id=1

            # Get form data
            initial_investment = form.cleaned_data["initial_investment"]
            discount_rate = evaluation.discount_rate  # Assuming you want to use the discount rate from the Evaluation
            period = int(form.cleaned_data["cash_flow_year_count"])
            project_name = 'New Project'  # Set a project name or get it from form
            
            # Create a new Project instance
            project = Project.objects.create(
                evaluation=evaluation,
                name=project_name,
                initial_investment=initial_investment,
                period=period,
            )
            
            # Assuming you have a way to get annual net cash flows from the form
            # For now, let's assume it's a fixed value like in your placeholder logic
            project.save()  # Save the project instance to calculate and store NPV and other metrics automatically
            
            return render(request, "npv/calculate-npv.html", {"form": form, "npv": project.npv})
    else:
        form = NPV_Form()

    return render(request, "npv/calculate-npv.html", {"form": form})


def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from .forms import NPV_Form
from .models import Project, Evaluation

def calculate_npv_form(request):

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count'))
        # check whether it's valid:
        # create a form instance and populate it with data from the request:
        form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count'))
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Create list for cash flows by adding initial investment
            cash_flows = []
            # Loop through each cash flow and add to cash flow list
            for i in range(1, int(form.cleaned_data["cash_flow_year_count"])):
                cash_flows.append(form.cleaned_data["cash_flow_year_"+str(i)])
            print("cash_flows", cash_flows)
            # save discount rate
            discount_rate = form.cleaned_data["discount_rate"]
            # render page with npv value
            evaluation = Evaluation.objects.create(
                name = "evaluation_name",
                discount_rate = discount_rate,
                note = "note",
                number_of_projects = 1
            )
            evaluation.save()
            project = Project.objects.create(
                 evaluation=evaluation,
                 name="project_name",
                 initial_investment=(form.cleaned_data["initial_investment"]),
                 period= len(cash_flows) - 1)
            project.calculate_npv(cash_flows)
            project.save()
           
            return render(request, "npv/calculate-npv.html", {"form": form}) 
    form = NPV_Form()       
    return render(request, "npv/calculate-npv.html", {"form": form})
    

def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})
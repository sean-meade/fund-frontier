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
# def calculate_npv_form(request):






# def calculate_NPV_form_2(request):
#     if request.method == "POST":
#         form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count', 0))
#         if form.is_valid():
#             # Fetch or create an Evaluation instance
#             evaluation = Evaluation.objects.first()  # Fetch the first Evaluation instance
#             if not evaluation:
#                 # If there's no Evaluation instance, create one
#                 evaluation = Evaluation.objects.create(discount_rate=form.cleaned_data["discount_rate"])

#             # Get form data
#             initial_investment = form.cleaned_data["initial_investment"]
#             period = int(form.cleaned_data["cash_flow_year_count"])
#             project_name = 'New Project'  # Set a project name or get it from form

#             # Create a new Project instance
#             project = Project.objects.create(
#                 evaluation=evaluation,
#                 name=project_name,
#                 initial_investment=initial_investment,
#                 period=period,
#             )

#             # Assuming you have a way to get annual net cash flows from the form
#             for year in range(1, period + 1):
#                 cash_flow = form.cleaned_data[f'cash_flow_year_{year}']
#                 # Add the cash flow to the project
#                 project.cash_flows.create(year=year, amount=cash_flow)

#             project.save()  # Save the project instance to calculate and store NPV and other metrics automatically

#             return redirect('list-projects')  # Redirect to the list of projects after successful form submission
#     else:
#         form = NPV_Form()

#     return render(request, "npv/calculate-npv.html", {"form": form})
# def calculate_npv_form(request):






# def calculate_NPV_form_2(request):
#     if request.method == "POST":
#         form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count', 0))
#         if form.is_valid():
#             # Fetch or create an Evaluation instance
#             evaluation = Evaluation.objects.first()  # Fetch the first Evaluation instance
#             if not evaluation:
#                 # If there's no Evaluation instance, create one
#                 evaluation = Evaluation.objects.create(discount_rate=form.cleaned_data["discount_rate"])

#             # Get form data
#             initial_investment = form.cleaned_data["initial_investment"]
#             period = int(form.cleaned_data["cash_flow_year_count"])
#             project_name = 'New Project'  # Set a project name or get it from form

#             # Create a new Project instance
#             project = Project.objects.create(
#                 evaluation=evaluation,
#                 name=project_name,
#                 initial_investment=initial_investment,
#                 period=period,
#             )

#             # Assuming you have a way to get annual net cash flows from the form
#             for year in range(1, period + 1):
#                 cash_flow = form.cleaned_data[f'cash_flow_year_{year}']
#                 # Add the cash flow to the project
#                 project.cash_flows.create(year=year, amount=cash_flow)

#             project.save()  # Save the project instance to calculate and store NPV and other metrics automatically

#             return redirect('list-projects')  # Redirect to the list of projects after successful form submission
#     else:
#         form = NPV_Form()

#     return render(request, "npv/calculate-npv.html", {"form": form})
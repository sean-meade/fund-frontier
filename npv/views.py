from django.shortcuts import render, get_object_or_404
from .models import Evaluation, Project, CashFlow
from .forms import NPV_Form, ContactForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


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
        form = NPV_Form(request.POST, extra=request.POST.get(
            'cash_flow_year_count', 0))
        if form.is_valid():
            # Create list for cash flows
            cash_flows = []

            print("form.cleaned_data", form.cleaned_data)
            # Loop through each cash flow and add to cash flow list

            for i in range(1, int(form.cleaned_data["cash_flow_year_count"]) + 1):
                cash_flows.append(form.cleaned_data["cash_flow_year_"+str(i)])

            # Save discount rate
            discount_rate = float(form.cleaned_data["discount_rate"]) / 100


            # Create a new evaluation
            evaluation = Evaluation.objects.create(
                name=form.cleaned_data["evaluation_name"],
                discount_rate=discount_rate,
                note=form.cleaned_data["note"],
                number_of_projects=1,
                period=len(cash_flows) - 1,
                user = request.user
            )
            evaluation.save()

            # Create a new project
            project = Project.objects.create(
                evaluation=evaluation,
                name=form.cleaned_data["project_name"],
                initial_investment=form.cleaned_data["initial_investment"],
                period=len(cash_flows) - 1
            )

            project.calculate_npv(cash_flows)
            project.calculate_payback_period(cash_flows)
            project.save()
            
            for i, cash_flow in enumerate(cash_flows, start=1):
                CashFlow.objects.create(
                    project=project,
                    year=i,
                    amount=cash_flow,
                )


            # Create a second project
            project2 = Project.objects.create(
                evaluation=evaluation,

                name=form.cleaned_data["project_name_2"],
                initial_investment=form.cleaned_data["initial_investment"],
                period=len(cash_flows) - 1
            )
            
            for i, cash_flow in enumerate(cash_flows, start=1):
                CashFlow.objects.create(
                    project=project,
                    year=i,
                    amount=cash_flow,
                )

            project2.calculate_npv(cash_flows)
            project2.calculate_payback_period(cash_flows)
            project2.save()


            project3 = Project.objects.create(
                evaluation=evaluation,
                name=form.cleaned_data["project_name_3"],
                initial_investment=form.cleaned_data["initial_investment"],
                period=len(cash_flows) - 1
            )
            
            for i, cash_flow in enumerate(cash_flows, start=1):
                CashFlow.objects.create(
                    project=project,
                    year=i,
                    amount=cash_flow,
                )
            project3.calculate_npv(cash_flows)
            project3.calculate_payback_period(cash_flows)
            project3.save()

            # Rank the projects
            projects_same_evaluation = Project.objects.filter(evaluation=evaluation).order_by('npv').values_list('id', flat=True)

            for rank, project_id in enumerate(projects_same_evaluation):
                project_by_id = Project.objects.get(id=project_id)
                setattr(project_by_id, 'rank', rank+1)
                project_by_id.save()

            return render(request, "npv/calculate-npv.html", {"form": form}) 

    form = NPV_Form()       
    return render(request, "npv/calculate-npv.html", {"form": form})


@login_required
def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})


@login_required
def list_evaluation_projects(request, evaluation_id):
    evaluation = Evaluation.objects.get(id=evaluation_id)

    projects = Project.objects.filter(evaluation=evaluation)
    return render(request, "npv/list-projects.html", {"projects": projects, "evaluation_name": evaluation.name})
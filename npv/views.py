import json
from django.shortcuts import render, get_object_or_404
from .models import Evaluation, Project, CashFlow
from .forms import Project_Form, Evaluation_Form, ContactForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def base(request):
    context = {'some_key': 'some_value'}  # Replace with actual context data
    return render(request, 'base.html', context)


def about(request):
    context = {'some_key': 'some_value'}  # Replace with actual context data
    return render(request, 'npv/about.html', context)


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
def create_evaluation(request):
    if request.method == "POST":
        # get data from form
        form = Evaluation_Form(request.POST)
        if form.is_valid():
            # Create list for cash flows
            cash_flows = []

            # Save discount rate
            discount_rate = float(form.cleaned_data["discount_rate"]) / 100

            # Create a new evaluation
            evaluation = Evaluation.objects.create(
                name=form.cleaned_data["evaluation_name"],
                discount_rate=discount_rate,
                note=form.cleaned_data["note"],
                period=len(cash_flows) - 1,
                user = request.user
            )
            evaluation.save()

            form=Project_Form()

            # Send an empty project form and the evaluation id to the add project page
            return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation.id}) 

    # first coming to the page (with a GET request) display an empty evaluation form
    form = Evaluation_Form()       
    return render(request, "npv/create-evaluation.html", {"form": form})

@login_required
def add_project(request, evaluation_id):
    if request.method == "POST":
        # get project data from the form
        form = Project_Form(request.POST, extra=request.POST.get(
            'cash_flow_year_count', 0))
        if form.is_valid():

            # Create list for cash flows
            cash_flows = []

            # Loop through each cash flow and add to cash flow list
            for i in range(1, int(form.cleaned_data["cash_flow_year_count"]) + 1):
                cash_flows.append(form.cleaned_data["cash_flow_year_"+str(i)])

            evaluation = Evaluation.objects.get(id=evaluation_id)

            # Create a new project
            project = Project.objects.create(
                evaluation=evaluation,
                name=form.cleaned_data["project_name"],
                initial_investment=form.cleaned_data["initial_investment"],
                period=len(cash_flows) - 1
            )

            # Call the calculate_npv and calculate_payback_period method 
            # in the model using the projects cash flows
            project.calculate_npv(cash_flows)
            project.calculate_payback_period(cash_flows)
            project.save()
            
            # Create CashFlow rows for each cash flow for the project
            for i, cash_flow in enumerate(cash_flows, start=1):
                CashFlow.objects.create(
                    project=project,
                    year=i,
                    amount=cash_flow,
                )
                
            # If the user uses the complete evaluation button
            if 'complete_eval' in request.POST:
                # Rank the projects
                projects_same_evaluation = Project.objects.filter(evaluation=evaluation).order_by('npv').values_list('id', flat=True)

                for rank, project_id in enumerate(projects_same_evaluation):
                    project_by_id = Project.objects.get(id=project_id)
                    setattr(project_by_id, 'rank', rank+1)
                    project_by_id.save()

                # And add the number of projects to the evaluation
                evaluation.number_of_projects = len(projects_same_evaluation)
                evaluation.save()
                
                # call the list_evaluation_projects so the user views the list of projects for the eval
                return list_evaluation_projects(request, evaluation_id)

            # Otherwise move on to the next empty for for the project
            form = Project_Form()

            return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation.id}) 

    # display an empty page when you call this page (I dont think is actually ever hit 
    # unless the user goes directly to the url)
    form = Project_Form()       
    return render(request, "npv/add-project.html", {"form": form})
            

@login_required
def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})


@login_required
def list_evaluation_projects(request, evaluation_id):
    evaluation = Evaluation.objects.get(id=evaluation_id)

    projects = Project.objects.filter(evaluation=evaluation).order_by('rank')
    return render(request, "npv/list-projects.html", {"projects": projects, "evaluation_name": evaluation.name})


@login_required
def edit_evaluation(request, evaluation_id):
    if request.method == "POST":
        # get the updated data for the evaluation
        form = Evaluation_Form(request.POST)
        if form.is_valid():
            # Create list for cash flows
            cash_flows = []

             # Save discount rate
            discount_rate = float(form.cleaned_data["discount_rate"]) / 100

            # Save edited info of the evaluation
            evaluation = Evaluation.objects.create(
                name=form.cleaned_data["evaluation_name"],
                discount_rate=discount_rate,
                note=form.cleaned_data["note"],
                period=len(cash_flows) - 1,
                user = request.user
            )
            evaluation.save()

        # go back to list of evaluations
        evaluations = Evaluation.objects.all().order_by('-id')
        return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})
    
    # Get the evaluation you want to edit
    evaluation = Evaluation.objects.get(id=evaluation_id)

    # grab the data
    data = {
            'discount_rate': evaluation.discount_rate,
            'evaluation_name': evaluation.name, 
            'note': evaluation.note}
    
    # Populate the form with that data
    form = Evaluation_Form(initial=data)

    return render(request, "npv/edit-eval.html", {"form": form, "evaluation_id":evaluation_id, "eval_name": evaluation.name})


@login_required
def edit_project(request, project_id):
    if request.method == "POST":
        # get the updated data of the project
        form = Project_Form(request.POST, extra=request.POST.get(
            'cash_flow_year_count', 0))
        if form.is_valid():
            # Create list for cash flows
            cash_flows = []

            # Loop through each cash flow and add to cash flow list
            for i in range(1, int(form.cleaned_data["cash_flow_year_count"]) + 1):
                cash_flows.append(form.cleaned_data["cash_flow_year_"+str(i)])

            # Update the data and save the project
            project = Project.objects.get(id=project_id)
            project.name=form.cleaned_data["project_name"]
            project.initial_investment=form.cleaned_data["initial_investment"]
            project.period=len(cash_flows) - 1
            project.calculate_npv(cash_flows)
            project.calculate_payback_period(cash_flows)
            project.save()
            
            # Loop through cash flows and update amounts
            # TODO: is the year right here? Too tired right now ....
            for i, cash_flow in enumerate(cash_flows, start=1):
                # if the cashflow already existed update it
                try:
                    cash_flow_instance = CashFlow.objects.get(project=project,
                                                         year=i)
                # otherwise create a new one
                except:
                    cash_flow_instance = CashFlow.objects.create(
                    project=project,
                    year=i,
                    amount=cash_flow,
                )
                cash_flow_instance.save()
                
            # Preform the ranking again with the projects
            projects_same_evaluation = Project.objects.filter(evaluation=project.evaluation).order_by('npv').values_list('id', flat=True)
            for rank, project_id in enumerate(projects_same_evaluation):
                project_by_id = Project.objects.get(id=project_id)
                setattr(project_by_id, 'rank', rank+1)
                project_by_id.save()
                
            return list_evaluation_projects(request, project.evaluation.id)

    # When first coming to the edit page get the data for the project you want to edit
    project = Project.objects.get(id=project_id)

    # This is used to send the cash flows (except the first one) to the JavaScript on edit-project.html
    cash_flows_dict = {}
    # form data
    data = {}
    # all cash flows relaated to the project
    cash_flows = CashFlow.objects.filter(project=project)
    for cash_flow in cash_flows:
        # This may not actuall be neccesary but collect them all for the form
        data["cash_flow_year_" + str(cash_flow.year)] = cash_flow.amount
        # Add them to the dict that we're sending to the JS on the edit-project.html page
        cash_flows_dict[str(cash_flow.year)] = float(cash_flow.amount)

    # remove the first one because cash_flow_year_1 field is already there
    cash_flows_dict.pop("1")

    # add in the remaining two for the form
    data["initial_investment"] = project.initial_investment
    data["project_name"] = project.name

    # add data to the form
    form = Project_Form(initial=data)

    return render(request, "npv/edit-project.html", {"form": form, "project_id":project_id, "project_name": project.name, "cash_flows_dict": json.dumps(cash_flows_dict)})

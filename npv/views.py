import json
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404
from .models import Evaluation, Project, CashFlow
from .forms import Project_Form, Evaluation_Form
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# TODO: Just realized none of this is filtered by user so everyone can see and edit each others projects

def base(request):
    return render(request, 'npv/about.html')

def contact(request):
    return render(request, 'npv/contact.html')

@login_required
def create_evaluation(request):
    # If Create Evaluation button is clicked
    if request.method == "POST":
        # get data from the submitted form
        form = Evaluation_Form(request.POST)

        if form.is_valid():
            # Save discount rate
            discount_rate = float(form.cleaned_data["discount_rate"]) / 100
            # Try to create a new evaluation
            try:
                evaluation = Evaluation.objects.create(
                    name=form.cleaned_data["evaluation_name"],
                    discount_rate=discount_rate,
                    note=form.cleaned_data["note"],
                    user = request.user
                )
                evaluation.save()

                # Send an empty project form and the evaluation id to the add project page
                form=Project_Form()
                return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation.id})
            # otherwise tell them they already have an eval by that name and give them the filled out form again 
            except ValidationError as e:
                list(messages.get_messages(request))
                messages.error(request, "You already have an evaluation by that name.")
                return render(request, "npv/create-evaluation.html", {"form": form})

    # first coming to the page (with a GET request) display an empty evaluation form
    form = Evaluation_Form()       
    return render(request, "npv/create-evaluation.html", {"form": form})


@login_required
def add_project(request, evaluation_id):
    # Get current evaluation the project belongs to
    evaluation = Evaluation.objects.get(id=evaluation_id)
    # If submitting a new project
    if request.method == "POST":
        # get project data from the form
        form = Project_Form(request.POST, extra=request.POST.get(
            'cash_flow_year_count', 0))
        
        # If the form is valid
        if form.is_valid():
            # Create list for cash flows
            cash_flows = []

            # TODO: Possibly a better way to do this using the existing data in 
            # the values in form.cleaned_data.get("cash_flow_year_count") this
            # May involve changing the methods that calculate npv and payback period
            # TODO: Repeated code in edit needs refactoring
            # Loop through each cash flow and add to cash flow list
            cash_flow_year_count = form.cleaned_data.get("cash_flow_year_count")
            # if cash flows exists
            if cash_flow_year_count is not None:
                # Foe every year
                for i in range(1, int(cash_flow_year_count) + 1):
                    # Create the string for the dict key
                    cash_flow_key = "cash_flow_year_" + str(i)
                    # If that key is in the incoming data
                    if cash_flow_key in form.cleaned_data:
                        # Add that value to the list
                        cash_flows.append(form.cleaned_data[cash_flow_key])
            # Try to create the project
            try:
                project = Project.objects.create(
                    evaluation=evaluation,
                    name=form.cleaned_data["project_name"],
                    initial_investment=float(form.cleaned_data["initial_investment"]),
                    period=len(cash_flows)
                )
            # If there is a problem raise the error to user
            except ValidationError as e:
                print(e)
                list(messages.get_messages(request))
                messages.error(request, e)
                # On error of creation present user with the form they were using
                return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation_id})
            

            # Call the calculate_npv and calculate_payback_period method 
            # in the model using the projects cash flows
            project.calculate_npv(cash_flows)
            project.calculate_annualized_npv()
            project.calculate_payback_period(cash_flows)

            # Try to save the project
            try:
                project.save()
            # Present error to user and logs
            except ValidationError as e:
                print(e)
                list(messages.get_messages(request))
                messages.error(request, e)
                # On error of creation present user with the form they were using
                return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation_id})
            
            # Create CashFlow objects for each cash flow and reference the current project
            for i, cash_flow in enumerate(cash_flows, start=1):
                CashFlow.objects.create(
                    project=project,
                    year=i,
                    amount=float(cash_flow),
                )
                
        # If the user uses the complete evaluation button
        if 'complete_eval' in request.POST:
            try:
                evaluation.rank_eval_projects()
            # If there is an error report it back to user and log
            except ValidationError as e:
                print(e)
                list(messages.get_messages(request))
                messages.error(request, 'Error updating rankings of projects for evaluation.')
                # On error of evaluation present user with the form they were using
                return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation_id})
            
            
            # show list of projects for the eval
            projects = Project.objects.filter(evaluation=evaluation).order_by('rank')
            return render(request, "npv/list-projects.html", {"projects": projects, "evaluation_name": evaluation.name})


    # Give empty form for adding new project
    form = Project_Form()
    return render(request, "npv/add-project.html", {"form": form, "evaluation_id": evaluation.id}) 
           

@login_required
def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})


@login_required
def list_evaluation_projects(request, evaluation_id):
    evaluation = Evaluation.objects.get(id=evaluation_id)
    projects = Project.objects.filter(evaluation=evaluation).order_by('rank')
    return render(request, "npv/list-projects.html", {"projects": projects, "evaluation_name": evaluation.name, "evaluation_id": evaluation_id})


@login_required
def edit_evaluation(request, evaluation_id):
    # Get the relevant evaluation
    evaluation = Evaluation.objects.get(id=evaluation_id)
    # If editing 
    # TODO: Should this be a PUT or a PATCH?
    if request.method == "POST":
        # get the updated data for the evaluation
        form = Evaluation_Form(request.POST)
        if form.is_valid():
            # Save discount rate
            discount_rate = float(form.cleaned_data["discount_rate"]) / 100

             # Update info of the evaluation
            evaluation.name = form.cleaned_data["evaluation_name"]
            evaluation.discount_rate = discount_rate
            evaluation.note = form.cleaned_data["note"]
            evaluation.user = request.user
            evaluation.save()       

        # go back to list of evaluations
        evaluations = Evaluation.objects.all().order_by('-id')
        return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})

    # On first coming to the page (with a GET request)
    # grab the data
    data = {
            'discount_rate': (evaluation.discount_rate)*100,
            'evaluation_name': evaluation.name, 
            'note': evaluation.note}
    
    # Populate the form with that data
    form = Evaluation_Form(initial=data)
    return render(request, "npv/edit-eval.html", {"form": form, 
                                                  "evaluation_id":evaluation_id, 
                                                  "eval_name": evaluation.name})


@login_required
def edit_project(request, project_id):
    # TODO: Repeated code in add project needs refactoring
    if request.method == "POST":
        # get the updated data of the project
        form = Project_Form(request.POST, extra=request.POST.get(
            'cash_flow_year_count', 0))
        if form.is_valid():
            # Create list for cash flows
            cash_flows = []

            # Loop through each cash flow and add to cash flow list
            cash_flow_year_count = form.cleaned_data.get("cash_flow_year_count")
            if cash_flow_year_count is not None:
                for i in range(1, int(cash_flow_year_count) + 1):
                    cash_flow_key = "cash_flow_year_" + str(i)
                    if cash_flow_key in form.cleaned_data:
                        cash_flows.append(form.cleaned_data[cash_flow_key])

            # Update the data and save the project
            project = Project.objects.get(id=project_id)
            project.name=form.cleaned_data["project_name"]
            project.initial_investment=form.cleaned_data["initial_investment"]
            project.period=len(cash_flows)
            project.calculate_npv(cash_flows)
            project.calculate_payback_period(cash_flows)
            project.save()

            project.evaluation.rank_eval_projects()
            
            # Loop through cash flows and update amounts
            # TODO: is the year right here? Too tired right now ....
            for i, cash_flow in enumerate(cash_flows, start=1):
                # if the cashflow already existed update it
                try:
                    cash_flow_instance = CashFlow.objects.get(project=project,
                                                         year=i)
                    cash_flow_instance.amount = cash_flow
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
                
            return render(request, "npv/edit-project.html", {"form": form, "project_id":project_id, 
                                                     "project_name": project.name, 
                                                     "cash_flows_dict": json.dumps(cash_flows_dict)})

    # When first coming to the edit page get the data for the project you want to edit
    project = Project.objects.get(id=project_id)

    # This is used to send the cash flows (except the first one) to the JavaScript on edit-project.html
    cash_flows_dict = {}
    # form data
    data = {}
    # all cash flows relaated to the project
    cash_flows = CashFlow.objects.filter(project=project)
    cash_flows_count = CashFlow.objects.filter(project=project).count()
    for cash_flow in cash_flows:
        # This may not actuall be neccesary but collect them all for the form
        data["cash_flow_year_" + str(cash_flow.year)] = cash_flow.amount
        # Add them to the dict that we're sending to the JS on the edit-project.html page
        cash_flows_dict[str(cash_flow.year)] = float(cash_flow.amount)
    
    data['cash_flow_year_count'] = cash_flows_count

    # add in the remaining two for the form
    data["initial_investment"] = project.initial_investment
    data["project_name"] = project.name

    # add data to the form
    form = Project_Form(initial=data, extra=cash_flows_count)

    return render(request, "npv/edit-project.html", {"form": form, "project_id":project_id, 
                                                     "project_name": project.name, 
                                                     "cash_flows_dict": json.dumps(cash_flows_dict)})


@login_required
def delete_project(request, project_id, evaluation_id):
    # Get the evaluation and related projects for when it is deleted
    evaluation = Evaluation.objects.get(id=evaluation_id)
    projects = Project.objects.filter(evaluation=evaluation)

    # Try to get the project and delete it
    try:
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        # Update the rankings for the evaluation projects after deleting project
        evaluation.rank_eval_projects()

        # If it is the last project
        if not projects:
            # Delete the evaluation
            evaluation.delete()
            # And get all remaining evaluations and display list
            evaluations = Evaluation.objects.all().order_by('-id')
            return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})
        else:
            # If there are more projects for the related evalutaion display them
            return render(request, "npv/list-projects.html", {"projects": projects, 
                                                              "evaluation_name": evaluation.name, 
                                                              "evaluation_id": evaluation.pk})
    # If the above fails show list of projects for evaluation.
    except:
        return render(request, "npv/list-projects.html", {"projects": projects, 
                                                              "evaluation_name": evaluation.name, 
                                                              "evaluation_id": evaluation.pk})    

@login_required
def delete_evaluation(request, evaluation_id):
    # Try to get and delete the evaluation
    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)
        evaluation.delete()
    # If you can't do nothing
    except:
        pass

    # And show the list of evaluations
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})

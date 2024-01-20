from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evaluation, Project
from .forms import NPV_Form, ContactForm


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
    

            # process the data in form.cleaned_data as required
            # Create list for cash flows by adding initial investment
            cash_flows = []
            # Loop through each cash flow and add to cash flow list
            print("form.cleaned_data", form.cleaned_data)
            for i in range(1, int(form.cleaned_data["cash_flow_year_count"]) + 1):
                cash_flows.append(form.cleaned_data["cash_flow_year_"+str(i)])
            # TODO: save cash flows for a project
            # save discount rate
            discount_rate = form.cleaned_data["discount_rate"] / 100
            
            # Calculate the npv
            # render page with npv value
            
            # TODO: Create input field for evaluation name and note
            evaluation = Evaluation.objects.create(
                name = "evaluation_name_new",
                discount_rate = discount_rate,
                note = "note",
                number_of_projects = 1,
                period= len(cash_flows) - 1
            )
            evaluation.save()
            
            # TODO: Try except for projects
            # - Create input field for name
            # - BUG: adding an extra project for some reason?
            project = Project.objects.create(
                 evaluation=evaluation,
                 name="project_name_44_new",
                 initial_investment=(form.cleaned_data["initial_investment"]),
                 period= len(cash_flows) - 1)
            project.calculate_npv(cash_flows)
            project.calculate_payback_period(cash_flows)
            project.save()
            project2 = Project.objects.create(
                 evaluation=evaluation,
                 name="project_name_3_new",
                 initial_investment=(form.cleaned_data["initial_investment"]),
                 period= len(cash_flows) - 1)
            project2.calculate_npv(cash_flows)
            project2.calculate_payback_period(cash_flows)
            project2.save()


            try:
                projects_same_evaluation = Project.objects.filter(evaluation=evaluation).order_by('npv').values_list('id', flat=True)
                print("projects_same_period", projects_same_evaluation)

                for rank, project_id in enumerate(projects_same_evaluation):
                    print("rank, project_id", rank, project_id)
                    project_by_id = Project.objects.get(id=project_id)
                    print("project", project_by_id)
                    setattr(project_by_id, 'rank', rank+1)
                    project_by_id.save()
            except:
                print("could not rank")
           
            return render(request, "npv/calculate-npv.html", {"form": form}) 
    
    else:
        form = NPV_Form()

        return render(request, "npv/calculate-npv.html", {"form": form})

@login_required
def list_evaluations(request):
    evaluations = Evaluation.objects.all().order_by('-id')
    return render(request, "npv/list-evaluations.html", {"evaluations": evaluations})
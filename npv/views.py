from django.shortcuts import render

from npv.forms import NPV_Form

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
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count'))
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Create list for cash flows by adding initial investment
            cash_flows = [-(form.cleaned_data["initial_investment"])]
            # Loop through each cash flow and add to cash flow list
            for i in range(1, int(form.cleaned_data["cash_flow_year_count"])):
                cash_flows.append(form.cleaned_data["cash_flow_year_"+str(i)])
            # save discount rate
            discount_rate = form.cleaned_data["discount_rate"]
            # Calculate the npv
            npv = calculate_NPV(cash_flows, discount_rate)
            # render page with npv value
            return render(request, "npv/calculate-npv.html", {"form": form, "npv": npv})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NPV_Form()

    return render(request, "npv/calculate-npv.html", {"form": form})
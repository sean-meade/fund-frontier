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
    if request.method == "POST":
        form = NPV_Form(request.POST, extra=request.POST.get('cash_flow_year_count', 0))
        if form.is_valid():
            cash_flows = [-(form.cleaned_data["initial_investment"])]
            cash_flow_year_count = int(form.cleaned_data["cash_flow_year_count"])
            
            for i in range(1, cash_flow_year_count + 1):
                cash_flow_key = f"cash_flow_year_{i}"
                if cash_flow_key in form.cleaned_data:
                    cash_flows.append(form.cleaned_data[cash_flow_key])
            
            discount_rate = form.cleaned_data["discount_rate"]
            npv = calculate_NPV(cash_flows, discount_rate)
            
            return render(request, "npv/calculate-npv.html", {"form": form, "npv": npv})
    else:
        form = NPV_Form()

    return render(request, "npv/calculate-npv.html", {"form": form})
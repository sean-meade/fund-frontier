from django.db import models
from django.core.validators import MinValueValidator
import numpy_financial as npf



class Evaluation(models.Model):
    """
    Model representing an evaluation with a name and discount rate.
    """
    name = models.CharField(max_length=255)
    # TODO: Do we limit the amount here?
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    number_of_projects = models.IntegerField(validators=[MinValueValidator(2)], help_text="Minimum number of projects required is 2")
    note = models.CharField(max_length=200)
    # TODO: add relationship to user

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    Model representing a project with various financial metrics and calculations.
    """
    CONSIDER_FURTHER_CHOICES = [
        ('yes', 'Yes'),
        ('rejected', 'Rejected'),
    ]

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    initial_investment = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.IntegerField()

    # Fields to store calculated values
    npv = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    payback_period = models.IntegerField(null=True, blank=True)
    annualized_npv = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    # New field to indicate whether to consider further or reject
    consider_further = models.CharField(
        max_length=10, choices=CONSIDER_FURTHER_CHOICES, default='yes')

    # New field for ranking
    rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_npv(self):
        # Fetch related Annual_net_cashflow instances for the project
        cash_flows_input = self.annual_net_cashflows.value_list('value', flat= True)
        # concact the initial investment to the cashflow
        cash_flows = [-self.initial_investment] + list(cash_flows_input)
        # calucalte the NPV for all cashflow starting including the initial investment
        npv_value = npf.npv(self.evaluation.discount_rate / 100, cash_flows)
        self.npv = round(npv_value, 2)
        if self.npv < 0:
            self.consider_further = 'rejected'

        return self.npv


    def calculate_payback_period(self, cash_flows_input):
        """
        Calculate Payback Period for the project.
        """
        cumulative_cash_flow = -self.initial_investment
        for year, cash_flow in enumerate(cash_flows_input, start=1):
            cumulative_cash_flow += cash_flow
            if cumulative_cash_flow >= 0:
                self.payback_period = year
                return self.payback_period
        return None


    def calculate_annualized_npv(self):
        """
        Calculate Annualized NPV for the project if the periods are different.
        """
        try:
            npv_value = self.npv
            # Aresent value interest factor of annuity (PVIFA)
            pvifa = (1-(1 + Evaluation.discount_rate) ** (Project.period))/ (Evaluation.discount_rate)
            # Annualized npv
            annualized_npv = npv_value / pvifa
            self.annualized_npv = round(annualized_npv, 2)
            return self.annualized_npv
        except:
            return None  # Periods are the same, skip annualization
        
        
    def save(self, *args, **kwargs):
        """
        Override the save method to update the rank before saving the project.
        """
        self.calculate_annualized_npv()
        super().save(*args, **kwargs)

class Annual_net_cashflow(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='annual_net_cashflows')

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User


class Evaluation(models.Model):
    """
    Model representing an evaluation with a name and discount rate.
    """
    name = models.CharField(max_length=255)
    # TODO: to 2 decimal places
    discount_rate = models.FloatField()
    note = models.CharField(max_length=200)
    number_of_projects = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    initial_investment = models.FloatField()
    period = models.IntegerField()

    # Fields to store calculated values
    npv = models.FloatField(
        null=True, blank=True)
    payback_period = models.IntegerField(null=True, blank=True)
    annualized_npv = models.FloatField(null=True, blank=True)

    # New field to indicate whether to consider further or reject
    consider_further = models.CharField(
        max_length=10, choices=CONSIDER_FURTHER_CHOICES, default='yes')

    # New field for ranking
    rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_npv(self, cash_flows_input):
        if not isinstance(cash_flows_input, list):
            raise ValueError("cash_flows_input must be a list")
        cash_flows = [-self.initial_investment] + cash_flows_input
        npv_value = sum(cash_flow / ((1 + float(self.evaluation.discount_rate)) ** t) for t, cash_flow in enumerate(cash_flows))
        self.npv = round(npv_value, 2)
        if self.npv < 0:
            self.consider_further = 'rejected'
        else:
            self.consider_further = 'accepted'
        self.save()
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
        Calculate Equivalent Annual Annuity (EAA) for the project if the periods are different.
        """
        try:
            npv_value = self.npv
            discount_rate = float(self.evaluation.discount_rate)
            annualized_npv = npv_value * discount_rate / (1 - (1 + discount_rate) ** -self.period)
            self.annualized_npv = round(annualized_npv, 2)
            return self.annualized_npv
        except Exception as e:
            print(f"Error calculating annualized NPV: {e}")
            return None
        
        
    def save(self, *args, **kwargs):
        """
        Override the save method to update the rank before saving the project.
        """
        self.calculate_annualized_npv()
        super().save(*args, **kwargs)

class CashFlow(models.Model):
    """
    Model representing a cash flow for a specific year of a project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    year = models.IntegerField()
    amount = models.FloatField()

    def __str__(self):
        return f'Year {self.year}: {self.amount}'
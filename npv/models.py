from django.db import models


class Evaluation(models.Model):
    """
    Model representing an evaluation with a name and discount rate.
    """
    name = models.CharField(max_length=255)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.CharField(max_length=200)
    number_of_projects = models.IntegerField()

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

    def calculate_npv(self, cash_flows_input):
        # cash_flows = [1,2,3,4]
        cash_flows = [-self.initial_investment] + cash_flows_input
        print("cash_flows", cash_flows)
        npv_value = sum(cash_flow / ((1 + self.evaluation.discount_rate / 100) ** t)for t, cash_flow in enumerate(cash_flows))
        # npv_value = 100.00
        print("npv_value", npv_value)
        self.npv = round(npv_value, 2)
        print("self.npv", self.npv)

        if self.npv < 0:
            self.consider_further = 'rejected'

        return self.npv


    def calculate_payback_period(self):
        """
        Calculate Payback Period for the project.
        """
        cumulative_cash_flow = -self.initial_investment
        for year, cash_flow in enumerate(self.annual_net_cash_flows(), start=1):
            cumulative_cash_flow += cash_flow
            if cumulative_cash_flow >= 0:
                self.payback_period = year
                return self.payback_period
        return None

    def annual_net_cash_flows(self):
        """
        Generator function to yield annual net cash flows for each year.
        """
        # Implement the actual logic to calculate or retrieve annual net cash flows
        for year in range(1, self.period + 1):
            # Placeholder: Yield a constant value or implement your logic
            yield 10000  # Replace with actual logic

    def calculate_annualized_npv(self):
        """
        Calculate Annualized NPV for the project if the periods are different.
        """
        if self.period != self.period:
            npv_value = self.calculate_npv()
            annualized_npv = npv_value / \
                ((1 + self.evaluation.discount_rate / 100) ** self.period - 1)
            self.annualized_npv = round(annualized_npv, 2)
            return self.annualized_npv
        else:
            return None  # Periods are the same, skip annualization

    # def update_rank(self):
    #     """
    #     Update the project's rank based on NPV and period criteria.
    #     """
        
    #     if self.npv > 0 and self.period == self.period:
    #         projects_same_period = Project.objects.filter(
    #             evaluation=self.evaluation, npv__gt=0, period=self.period
    #         ).order_by('-npv')
    #         # 
    #         rank = list(projects_same_period).index(self) + 1
    #         self.rank = rank
    #     elif self.npv > 0 and self.period != self.period:
    #         projects_diff_period = Project.objects.filter(
    #             evaluation=self.evaluation, npv__gt=0, period__ne=self.period
    #         ).order_by('-annualized_npv')
    #         rank = list(projects_diff_period).index(self) + 1
    #         self.rank = rank
    #     else:
    #         self.rank = None

    def save(self, *args, **kwargs):
        """
        Override the save method to update the rank before saving the project.
        """
        # self.update_rank()
        super().save(*args, **kwargs)


class AnnualNetCashFlows(models.Model): 

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cash_flow_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    period = models.IntegerField()
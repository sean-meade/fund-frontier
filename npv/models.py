from django.db import models


class Evaluation(models.Model):
    """
    Model representing an evaluation with a name and discount rate.
    """
    name = models.CharField(max_length=255)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.CharField(max_length=200)
    number_of_projects = models.IntegerField()
    period = models.IntegerField()

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
        npv_value = sum(cash_flow / ((1 + self.evaluation.discount_rate / 100) ** t) for t, cash_flow in enumerate(cash_flows))
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
            annualized_npv = npv_value / ((1 + self.evaluation.discount_rate / 100) ** self.period - 1)
            self.annualized_npv = round(annualized_npv, 2)
            return self.annualized_npv
        except:
            return None  # Periods are the same, skip annualization
        
    # def update_rank(self):
    #     """
    #     Update the project's rank based on NPV and period criteria.
    #     """
    #     print("")
    #     print("")
    #     print("")
    #     print("self.name", self.name)
    #     print("We hit the rank")
    #     print("npv", self.npv)
    #     print("self.period", self.period)
    #     print("self.evaluation.period", self.evaluation.period)
        

    #     if self.npv is not None and self.npv > 0 and self.period == self.evaluation.period:
    #         print("We have passed the if statement")
    #         projects_same_evaluation = Project.objects.all( 
    #                                                       ).order_by('npv').values_list('id', flat=True)
    #         print("projects_same_period", projects_same_evaluation)
    #         for rank, project_id in enumerate(projects_same_evaluation):
    #             print("rank, project_id", rank, project_id)
    #             project = Project.objects.get(id=project_id)
    #             print("project", project)
    #             setattr(project, 'rank', rank+1)
                
            
        # elif self.npv is not None and self.npv > 0 and self.period == self.evaluation.period:
        #     projects_diff_period = Project.objects.filter(
        #         evaluation=self.evaluation, npv__gt=0, period=self.period
        #     ).order_by('annualized_npv').values_list('id', flat=True)
        #     rank = projects_diff_period.index(self) + 1
        #     self.rank = rank
        # else:
        #     self.rank = None
        
    def save(self, *args, **kwargs):
        """
        Override the save method to update the rank before saving the project.
        """
        self.calculate_annualized_npv()
        # self.update_rank()
        super().save(*args, **kwargs)
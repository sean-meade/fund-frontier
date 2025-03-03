from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from decimal import Decimal


class Evaluation(models.Model):
    """
    Model representing an evaluation with a name and discount rate.
    """
    name = models.CharField(max_length=255)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, 
                                        validators=[MinValueValidator(0), 
                                                    MaxValueValidator(1)])
    note = models.CharField(max_length=200, null=True, blank=True)
    number_of_projects = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def rank_eval_projects(self):
        # List of projects ranked by npv
            projects_same_evaluation = list(Project.objects.filter(evaluation=self).order_by('npv'))
            # For every project using the position (starting at 1) as the rank
            for rank, project in enumerate(projects_same_evaluation, 1):
                # Set rank of project
                project.rank = rank
                # Try save the project with new rank
                project.save()
            
            # And add the number of projects to the evaluation and save
            self.number_of_projects = len(projects_same_evaluation)
            self.save()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Check to see if the evaluation already exists
        try:
            eval = Evaluation.objects.get(user=self.user, name=self.name, id=self.pk)
            exists = True
        # set exists to False if not
        except Exception as e:
            print("Not an existing evaluation. Creating a new one...")
            exists = False

        # If it exists
        if exists:
            fields_to_check = [
                'name',
                'discount_rate',
                'note',
                'number_of_projects'
            ]

            updated = False
            # Check all fields
            for field in fields_to_check:
                # Value of possible update
                new_value = getattr(self, field)
                # Value of current value
                current_value = getattr(eval, field)

                # Special handling for discount_rate to convert to Decimal before comparison
                if field == 'discount_rate':
                    new_value = Decimal(new_value)
                    current_value = Decimal(current_value)

                # If the incoming value is not equal to current value
                if current_value != new_value:
                    # Set the new value for the field
                    setattr(eval, field, new_value)
                    # And mark as to be updated
                    updated = True

            # If Evaluation needs updating
            if updated:
                # Save the evaluation with new values
                super(Evaluation, eval).save(*args, **kwargs)
            # Else no update required
            else:
                print("No update required")
        # If it doesn't exist create it
        else:
            super(Evaluation, self).save(*args, **kwargs)


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
    initial_investment = models.DecimalField(max_digits=10, decimal_places=2)  # store as decimal
    cash_flow_year_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # store as decimal
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

    # TODO: Comment and check all of these methods
    def calculate_npv(self, cash_flows_input):
        if not isinstance(cash_flows_input, list):
            raise ValueError("cash_flows_input must be a list")
        try:
            cash_flows = [-self.initial_investment] + cash_flows_input
            npv_value = sum(cash_flow / ((1 + float(self.evaluation.discount_rate)) ** t) for t, cash_flow in enumerate(cash_flows))
            self.npv = round(npv_value, 2)
            if self.npv < 0:
                self.consider_further = 'rejected'
            else:
                self.consider_further = 'accepted'
            self.save()
            return self.npv
        except ValueError as e:
            print("Failure in calculate_npv: ", e)
            raise ValueError("Could not calculate npv please check logs")


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
        except ValueError as e:
            raise ValueError(f"Error calculating annualized NPV: {e}")
        
        
    def save(self, *args, **kwargs):
        """
        Override the save method to update the Project before saving.
        """
        # Check to see if project exists
        try:
            proj = Project.objects.get(evaluation__user=self.evaluation.user,
                                    evaluation=self.evaluation,
                                    name=self.name, id=self.pk)
            exists = True
        except Project.DoesNotExist:
            exists = False

        # If it exists
        if exists:
            fields_to_check = [
                'name',
                'initial_investment',
                'npv',
                'consider_further',
                'cash_flow_year_1',
                'payback_period',
                'annualized_npv',
                'evaluation',
                'rank',
                'period'
            ]

            updated = False
            # Go through all fields
            for field in fields_to_check:
                # Get incoming value
                new_value = getattr(self, field)
                # If incoming is different to current
                if getattr(proj, field) != new_value:
                    # Set the new value for the field and make as to be updated
                    setattr(proj, field, new_value)
                    updated = True

            # If to be updated try and save
            if updated:
                try:
                    super(Project, proj).save(*args, **kwargs)
                except Exception as e:
                    print(e)
            else:
                print("No editing needed")
                return
        # If it doesn't exist create it
        else:
            # All current project names for evaluation
            project_names = Project.objects.filter(evaluation = self.evaluation).values_list('name', flat=True)
            # If the name is the same as an existing project for this evaluation inform the user
            if self.name in project_names:
                raise ValidationError('You already have an Project by that name.')
            # Create new Project
            super(Project, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        self.evaluation.number_of_projects -= 1
        self.evaluation.save()

        super(Project, self).delete(*args, **kwargs)


class CashFlow(models.Model):
    """
    Model representing a cash flow for a specific year of a project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    year = models.IntegerField()
    amount = models.FloatField()

    def __str__(self):
        return f'Year {self.year}: {self.amount}'

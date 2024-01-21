from django.test import TestCase
from decimal import Decimal
from .models import Evaluation, Project, Annual_net_cashflow

class ProjectModelTest(TestCase):
    def setUp(self):
    # Second Evaluation
        evaluation2 = Evaluation.objects.create(
            name="Test Evaluation 2",
            discount_rate=Decimal(7.5),
            number_of_projects=3,
            note="Test note 2"
        )

        self.project2 = Project.objects.create(
            evaluation = evaluation2,
            name = "Test Project 2",
            initial_investment = Decimal('15000.00'),
            period = 8,
        )

        self.project3 = Project.objects.create(
            evaluation = evaluation2,
            name = "Test Project 3",
            initial_investment = Decimal('25000.00'),
            period = 7,
        )

        self.project4 = Project.objects.create(
            evaluation = evaluation2,
            name = "Test Project 4",
            initial_investment = Decimal('20000.00'),
            period = 10,
        )

        # Annual_net_cashflow project 2
        Annual_net_cashflow.objects.create(
            value=Decimal('2000.00'),  # Adjust with the desired cash flow value
            project=self.project2
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('3000.00'),  # Adjust with the desired cash flow value
            project=self.project2
        )
        Annual_net_cashflow.objects.create(
            value=Decimal('3300.00'),  # Adjust with the desired cash flow value
            project=self.project2
        )
        Annual_net_cashflow.objects.create(
            value=Decimal('3630.00'),  # Adjust with the desired cash flow value
            project=self.project2
        )
        Annual_net_cashflow.objects.create(
            value=Decimal('3993.00 '),  # Adjust with the desired cash flow value
            project=self.project2
        )
        Annual_net_cashflow.objects.create(
            value=Decimal('4392.30 '),  # Adjust with the desired cash flow value
            project=self.project2
        )
        Annual_net_cashflow.objects.create(
            value=Decimal('4831.53'),  # Adjust with the desired cash flow value
            project=self.project2
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('5314.68'),  # Adjust with the desired cash flow value
            project=self.project2
        )


        # Annual_net_cashflow project 2
        Annual_net_cashflow.objects.create(
            value=Decimal('2000.00'),  # Adjust with the desired cash flow value
            project=self.project2
        )

        # Annual_net_cashflow project 3
        Annual_net_cashflow.objects.create(
            value=Decimal('2000.00'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2000.00'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2200.00'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2420.00'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2662.00'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2928.20'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2001.20'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('2201.10'),  # Adjust with the desired cash flow value
            project=self.project3
        )

        # Annual_net_cashflow to the fourth project
        Annual_net_cashflow.objects.create(
            value=Decimal('1000.00'),  
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('350.00'),  
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('360.00'),  
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('400.00'),  
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('600.00'),  
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('200.00'), 
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('10000.00'), 
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('5000.00'),  
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('5000.00'), 
            project=self.project4
        )

        Annual_net_cashflow.objects.create(
            value=Decimal('7000.00'), 
            project=self.project4
        )

def test_calculate_payback_period_second_evaluation(self):
    # Test payback period calculation for projects in the second evaluation

    # Project 2
    payback_period_project2 = self.project2.calculate_payback_period(
        [cf.value for cf in self.project2.annual_net_cashflows.all()]
    )
    self.assertIsNotNone(payback_period_project2)
    self.assertEqual(self.project2.payback_period, 5)

    # Project 3
    payback_period_project3 = self.project3.calculate_payback_period(
        [cf.value for cf in self.project3.annual_net_cashflows.all()]
    )
    self.assertIsNotNone(payback_period_project3)
    self.assertEqual(self.project3.payback_period, 3) 

    # Project 4
    payback_period_project4 = self.project4.calculate_payback_period(
        [cf.value for cf in self.project4.annual_net_cashflows.all()]
    )
    self.assertIsNotNone(payback_period_project4)
    self.assertEqual(self.project4.payback_period, 9)  



def test_calculate_annualized_npv_second_evaluation(self):
    # Test annualized NPV calculation for projects in the second evaluation

    # Project 2
    annualized_npv_project2 = self.project2.calculate_annualized_npv()
    self.assertIsNotNone(annualized_npv_project2)
    self.assertEqual(self.project2.annualized_npv, Decimal('3266.11')) 

    # Project 3
    annualized_npv_project3 = self.project3.calculate_annualized_npv()
    self.assertIsNotNone(annualized_npv_project3)
    self.assertEqual(self.project3.annualized_npv, Decimal('1653.47'))  
    # Project 4
    annualized_npv_project4 = self.project4.calculate_annualized_npv()
    self.assertIsNotNone(annualized_npv_project4)
    self.assertEqual(self.project4.annualized_npv, Decimal('3135.94'))  


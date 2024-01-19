from django.test import TestCase

from django.test import TestCase
from .models import Evaluation, Project

class EvaluationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Evaluation.objects.create(name='Test Evaluation', discount_rate=0.1, note='Test Note', number_of_projects=1)

    def test_name_label(self):
        evaluation = Evaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    # def test_discount_rate_label(self):
    #     evaluation = Evaluation.objects.get(id=1)
    #     field_label = evaluation._meta.get_field('discount_rate').verbose_name
    #     self.assertEqual(field_label, 'discount rate')

    # def test_note_label(self):
    #     evaluation = Evaluation.objects.get(id=1)
    #     field_label = evaluation._meta.get_field('note').verbose_name
    #     self.assertEqual(field_label, 'note')

    # def test_number_of_projects_label(self):
    #     evaluation = Evaluation.objects.get(id=1)
    #     field_label = evaluation._meta.get_field('number_of_projects').verbose_name
    #     self.assertEqual(field_label, 'number of projects')

class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        evaluation = Evaluation.objects.create(name='Test Evaluation', discount_rate=0.1, note='Test Note', number_of_projects=1)
        Project.objects.create(evaluation=evaluation, name='Test Project', initial_investment=10000, period=5)

    def test_name_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    # def test_initial_investment_label(self):
    #     project = Project.objects.get(id=1)
    #     field_label = project._meta.get_field('initial_investment').verbose_name
    #     self.assertEqual(field_label, 'initial investment')

    # def test_period_label(self):
    #     project = Project.objects.get(id=1)
    #     field_label = project._meta.get_field('period').verbose_name
    #     self.assertEqual(field_label, 'period')

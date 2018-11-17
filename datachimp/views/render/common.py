from django.shortcuts import redirect, render
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login

from datachimp.models.project import Project
from datachimp.models.membership import Membership
from datachimp.models.machinelearning_model import MachineLearningModel
from datachimp.views.render.base import BaseView


@method_decorator(login_required, name='dispatch')
class HomePageView(BaseView):
    template_name = "home.html"


class DocPageView(BaseView):
    template_name = "python_client_doc.html"


@method_decorator(login_required, name='dispatch')
class EvaluationDashboardView(BaseView):
    template_name = "model_evaluation_dashboard.html"

    def get_context_data(self, pk,  **kwargs):
        context = super(EvaluationDashboardView, self).get_context_data(**kwargs)
        project =  Project.objects.get(pk=pk)
        user = self.request.user

        # Check if the user has access to the project
        try:
            Membership.objects.get(user=user, project=project)
        except Membership.DoesNotExist:
            raise PermissionDenied("Oops, you don't have permission for this!")

        context['project'] = project

        return context


@method_decorator(login_required, name='dispatch')
class DataListView(BaseView):
    template_name = "data_list.html"

    def get_context_data(self, **kwargs):
        context = super(DataListView, self).get_context_data(**kwargs)
        project_id = self.kwargs['project_id']
        user = self.request.user
        project = Project.objects.get(pk = project_id)

        # Check if the user is the owner
        owner_flag = True if user == project.user else False

        # Check if the user has access to the project
        access = Membership.objects.filter(user=user, project=project).exists()
        if not access:
        	raise PermissionDenied("Oops, you don't have permission for this!")

        project_key = Membership.objects.get(user=user, project=project).key
        context['project'] = project
        context['project_key'] = project_key
        context['owner_flag'] = owner_flag

        return context


class LandingPageView(BaseView):
    template_name = "landing_page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)

        user = self.request.user
        if isinstance(user,AnonymousUser):
            context['logged_flag'] = False
        else:
            context['logged_flag'] = True

        return context


class PricingPageView(BaseView):
    template_name = "pricing.html"

    def get_context_data(self, **kwargs):
        context = super(PricingPageView, self).get_context_data(**kwargs)

        user = self.request.user
        if isinstance(user,AnonymousUser):
            context['logged_flag'] = False
        else:
            context['logged_flag'] = True

        return context

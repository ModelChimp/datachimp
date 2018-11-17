from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datachimp.enum import EvaluationMetric, PlatformLibraryType
from datachimp.models.membership import Membership
from datachimp.models.machinelearning_model import MachineLearningModel
from datachimp.models.data import Data
from datachimp.views.render.base import BaseView

from datachimp.utils.data_utils import dict_to_kv


@method_decorator(login_required, name='dispatch')
class DataDetailView(BaseView):
    template_name = "data_detail.html"

    def get_context_data(self, pk,  **kwargs):
        context = super(DataDetailView, self).get_context_data(**kwargs)
        data_obj = Data.objects.get(pk=pk)
        project = data_obj.project
        project_owner = data_obj.project.user
        user = self.request.user

        # Check if the user has access to the project
        access = Membership.objects.filter(user=user, project=project).exists()
        if not access:
            raise PermissionDenied("Oops, you don't have permission for this!")

        # Set an owner flag based on project_owner or model owner
        owner_flag = True if user == data_obj.user or user == project_owner  else False



        context['experiment_name'] = data_obj.name

        context['data_obj'] = data_obj
        context['owner_flag'] = owner_flag

        return context

def parse_epoch_data(data):
    metric_list = data['metric_list']
    evaluation_data = data['evaluation']
    result = {}

    for metric in metric_list:
        max_value = 0
        min_value = 0

        for i, evaluation in  enumerate(evaluation_data[metric]):
            if i == 0:
                max_value = evaluation['value']
                min_value = evaluation['value']

            if evaluation['value'] > max_value:
                max_value = evaluation['value']

            if evaluation['value'] < min_value:
                min_value = evaluation['value']

        max_metric_name = "%s (max)" % metric
        min_metric_name = "%s (min)" % metric

        result[max_metric_name] = max_value
        result[min_metric_name] = min_value

    return result

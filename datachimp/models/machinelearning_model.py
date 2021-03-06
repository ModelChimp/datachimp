from django.db import models
from django.contrib.postgres.fields import JSONField

from datachimp.enum import PlatformType
from datachimp.enum import PlatformLibraryType, ExperimentStatus
from datachimp.models.user import User
from datachimp.models.project import Project
from datachimp.utils.generate_uid import generate_uid


class MachineLearningModel(models.Model):
    name = models.CharField(max_length=200, blank=True, default='', null=True)
    algorithm = models.CharField(max_length=200, blank=True, default='', null=True)
    platform = models.CharField(max_length=200,
								blank=True, default='',
								choices=PlatformType.CHOICES,
                                null=True)
    platform_library = models.CharField(max_length=5,
										blank=True,
										default='',
										choices=PlatformLibraryType.CHOICES,
                                        null=True)
    experiment_id = models.CharField(max_length=70, unique=True, default=generate_uid)
    dataset_id = models.CharField(max_length=100, default='', null=True)
    status = models.CharField(max_length=5,
										blank=True,
										default=ExperimentStatus.COMPLETED,
										choices=ExperimentStatus.CHOICES,
                                        null=True)
    comment_count = models.IntegerField(default=0)
    labels = JSONField(null=True)

    features = JSONField(null=True)
    model_parameters = JSONField(null=True, default=dict)
    evaluation_parameters = JSONField(null=True)
    deep_learning_parameters = JSONField(default=list, null=True) #REMOVE
    epoch_durations = JSONField(null=True)

    ml_model_file = models.FileField(upload_to='model/', null=True)
    code_file = models.FileField(upload_to='code/', null=True)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='ml_model_project')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    experiment_start = models.DateTimeField(null=True)
    experiment_end = models.DateTimeField(null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)
    last_heart_beat = models.DateTimeField(auto_now=True)

    @property
    def short_name(self):
        if self.name == self.experiment_id:
            return self.name[:7]

        return self.name

    def __str__(self):
        return "%s" % (self.name,)

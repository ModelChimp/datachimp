from django.db import models
from django.contrib.postgres.fields import JSONField

from datachimp.models.user import User
from datachimp.models.project import Project
from datachimp.utils.generate_uid import generate_uid


class Data(models.Model):
    name = models.CharField(max_length=200, blank=True, default='', null=True)
    version_id = models.CharField(max_length=70, unique=True, default=generate_uid)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='data_project')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    files = JSONField(null=True)
    files_path = models.FileField(upload_to='data/', null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)

    @property
    def short_name(self):
        if self.name == self.experiment_id:
            return self.name[:7]

        return self.name

    def __str__(self):
        return "%s" % (self.name,)

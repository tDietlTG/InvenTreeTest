from __future__ import unicode_literals
# from django.utils.translation import ugettext as _

from django.db import models

from InvenTree.models import InvenTreeTree
from part.models import Part


class ProjectCategory(InvenTreeTree):
    """ ProjectCategory provides hierarchical organization of Project objects.
    Each ProjectCategory can contain zero-or-more child categories,
    and in turn can have zero-or-one parent category.
    """

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    @property
    def projects(self):
        return self.project_set.all()


class Project(models.Model):
    """ A Project takes multiple Part objects.
    A project can output zero-or-more Part objects
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class ProjectPartManager(models.Manager):
    """ Manager for handling ProjectParts
    """

    def create(self, *args, **kwargs):
        """ Test for validity of new ProjectPart before actually creating it.
        If a ProjectPart already exists that references the same:
        a) Part
        b) Project
        then return THAT project instead.
        """

        project_id = kwargs['project']
        part_id = kwargs['part']

        project_parts = self.filter(project=project_id, part=part_id)
        if len(project_parts) > 0:
            return project_parts[0]

        return super(ProjectPartManager, self).create(*args, **kwargs)


class ProjectPart(models.Model):
    """ A project part associates a single part with a project
    The quantity of parts required for a single-run of that project is stored.
    The overage is the number of extra parts that are generally used for a single run.
    """

    objects = ProjectPartManager()

    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    """
    # TODO - Add overage model fields

    # Overage types
    OVERAGE_PERCENT = 0
    OVERAGE_ABSOLUTE = 1

    OVARAGE_CODES = {
        OVERAGE_PERCENT: _("Percent"),
        OVERAGE_ABSOLUTE: _("Absolute")
    }

    overage = models.FloatField(default=0)
    overage_type = models.PositiveIntegerField(
        default=OVERAGE_ABSOLUTE,
        choices=OVARAGE_CODES.items())
    """

    # Set if the part is generated by the project,
    # rather than being consumed by the project
    output = models.BooleanField(default=False)

    def __str__(self):
        return "{quan} x {name}".format(
            name=self.part.name,
            quan=self.quantity)


class ProjectRun(models.Model):
    """ A single run of a particular project.
    Tracks the number of 'units' made in the project.
    Provides functionality to update stock,
    based on both:
    a) Parts used (project inputs)
    b) Parts produced (project outputs)
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    run_date = models.DateField(auto_now_add=True)

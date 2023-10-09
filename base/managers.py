from django.db import models


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

    
class ConfirmReviewManager(models.Manager):
    def get_queryset(self) :
        return super().get_queryset().filter(confirm=True)

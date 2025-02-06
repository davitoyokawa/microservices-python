from django.db import models

class Product(models.Model):
    title = models.CharField (verbose_name=("Title"), max_length=50)
    image = models.CharField (verbose_name=("image"), max_length=50)
    likes = models.PositiveIntegerField (default=0)
    total_ratings = models.PositiveIntegerField (default=0)
    ratings_count = models.PositiveIntegerField (default=0)

    def __str__(self):
        return self.title

class User(models.Model):
    pass

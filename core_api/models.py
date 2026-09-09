from django.db import models


class CarModel(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    per_km_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    def __str__(self):
        return self.name
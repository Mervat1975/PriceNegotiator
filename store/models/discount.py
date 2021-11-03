from django.db import models


class Discount(models.Model):
    amount_from = models.IntegerField()
    amount_to = models.IntegerField()
    discount_from = models.DecimalField(decimal_places=2, max_digits=4)
    discount_to = models.DecimalField(decimal_places=2, max_digits=4)

    @staticmethod
    def get_discount_by_id(id):
        try:
            return Discount.objects.get(id=id)
        except:
            return False

    @staticmethod
    def get_discount_all():
        try:
            return Discount.objects.all()
        except:
            return False

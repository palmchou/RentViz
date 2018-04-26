from django.db import models
from eaves.models.FloorPlan import FloorPlan


class Apartment(models.Model):
    code = models.CharField(max_length=32, db_index=True, unique=True)
    number = models.CharField(max_length=32)
    building_number = models.CharField(max_length=32)
    beds = models.IntegerField()
    baths = models.IntegerField()
    floor = models.IntegerField()
    floor_plan = models.ForeignKey(
        FloorPlan,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return str(self.floor_plan) + '-' + self.number


    @staticmethod
    def createFromJson(apt_data, fp):
        apt = {
            'code': apt_data['apartmentCode'],
            'number': apt_data['apartmentNumber'],
            'baths': apt_data['baths'],
            'beds': apt_data['beds'],
            'building_number': apt_data['buildingNumber'],
            'floor': apt_data['floor']
        }
        apt = Apartment.objects.create(
            code=apt['code'],
            number=apt['number'],
            baths=apt['baths'],
            beds=apt['beds'],
            building_number=apt['building_number'],
            floor=apt['floor'],
            floor_plan_id=fp.id
        )
        return apt

from django.db import models
from eaves.models.Community import Community


class FloorPlan(models.Model):
    uid = models.CharField(max_length=32, db_index=True, unique=True)
    eaves_id = models.CharField(max_length=32)
    size = models.IntegerField()
    image_url = models.CharField(max_length=2048)
    code_name = models.CharField(max_length=32)
    bedroom_type = models.CharField(max_length=32)
    community = models.ForeignKey(
        Community,
        on_delete=models.PROTECT,
    )
    custom_name = models.CharField(max_length=32, default='')

    def __str__(self):
        if self.custom_name:
            return str(self.community) + '-' + self.custom_name
        else:
            return str(self.community) + '-' + str(self.size)

    @staticmethod
    def createFromJson(fp_data):
        fp_uid = fp_data['communityCode'] + '-' + fp_data['floorPlanId']
        fp = {'eaves_id': fp_data['floorPlanId'],
              'size': fp_data['floorPlanSizeRange']['minSize'],
              'image_url': fp_data['floorPlanImage'],
              'code_name': fp_data['floorPlanName'],
              'bedroom_type': fp_data['floorPlanType'],
              'bath_type': fp_data['floorPlanBathType'],
              'comm_code': fp_data['communityCode'],
              'uid': fp_uid
              }
        try:
            comm = Community.objects.get(comm_code=fp['comm_code'])
        except Community.DoesNotExist:
            comm = Community.objects.create(comm_code=fp['comm_code'])
        floor_plan = FloorPlan.objects.create(
            uid=fp['uid'],
            eaves_id=fp['eaves_id'],
            size=fp['size'],
            image_url=fp['image_url'],
            code_name=fp['code_name'],
            bedroom_type=fp['bedroom_type'],
            community=comm
        )
        return floor_plan

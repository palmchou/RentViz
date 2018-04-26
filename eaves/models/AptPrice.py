from django.db import models
from eaves.models.Apartment import Apartment
from eaves.util import get_PST_now
from datetime import datetime
import pytz


class AptPrice(models.Model):
    effective_rent = models.IntegerField()
    amenitized_rent = models.IntegerField()
    available_date = models.DateField()
    queried_at = models.DateTimeField()
    is_promotion = models.BooleanField(default=False)
    apt = models.ForeignKey(
        Apartment,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return '%s: $%s @ %s' % (self.apt, self.effective_rent, str(self.available_date))

    @staticmethod
    def createFromJson(price_data, apt, qry_dt=None):

        def parse_date(date_value):
            dt = datetime.fromtimestamp(int(date_value[6:6+13]) / 1000)
            return pytz.timezone('US/Pacific').localize(dt).astimezone(pytz.utc).date()

        if not qry_dt:
            qry_dt = get_PST_now()

        return AptPrice.objects.create(
            effective_rent=price_data['effectiveRent'],
            amenitized_rent=price_data['amenitizedRent'],
            available_date=parse_date(price_data['availableDate']),
            queried_at=qry_dt,
            is_promotion=price_data['effectiveRent'] != price_data['amenitizedRent'],
            apt_id=apt.id
        )

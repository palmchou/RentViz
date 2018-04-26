# Generated by Django 2.0.4 on 2018-04-26 03:02

import gzip
import json
import os
import pytz
from datetime import datetime
from django.db import migrations
from eaves.models.FloorPlan import FloorPlan as eavesFlp
from eaves.models.AptPrice import AptPrice as eavesAptPrice
from eaves.models.Apartment import Apartment as eavesApartment

FloorPlan = None
Apartment = None
Community = None


def extract_data():
    dir_path = 'data'
    for tgz in os.listdir(dir_path):
        path = os.path.join(dir_path, tgz)
        print(path)
        qry_dt = pytz.timezone('US/Pacific').localize(datetime.strptime(tgz[:13], '%Y-%m-%d_%H'))
        with gzip.open(path, 'rb') as b:
            content = b.read()
            data = json.loads(content)
            parse_query_data(data['availableFloorPlanTypes'], qry_dt)
            print()


def parse_query_data(floor_types, qry_dt):
    for floor_type in floor_types:
        for floor_plan_data in floor_type['availableFloorPlans']:
            fp_uid = floor_plan_data['communityCode'] + '-' + floor_plan_data['floorPlanId']
            try:
                fp = FloorPlan.objects.get(uid=fp_uid)
            except FloorPlan.DoesNotExist:
                fp = eavesFlp.createFromJson(floor_plan_data)
            for pkgs in floor_plan_data['finishPackages']:
                for apt_data in pkgs['apartments']:
                    apt_code = apt_data['apartmentCode']
                    try:
                        apt = Apartment.objects.get(code=apt_code)
                    except Apartment.DoesNotExist:
                        apt = eavesApartment.createFromJson(apt_data, fp)
                        print('apt: %s created.' % str(apt))
                    eavesAptPrice.createFromJson(apt_data['pricing'], apt, qry_dt)


def populate(apps, schema_editor):
    global FloorPlan, Community, Apartment
    FloorPlan = apps.get_model('eaves', 'FloorPlan')
    Community = apps.get_model('eaves', 'Community')
    Apartment = apps.get_model('eaves', 'Apartment')
    extract_data()


def clean(apps, schema_editor):
    FloorPlan = apps.get_model('eaves', 'FloorPlan')
    Community = apps.get_model('eaves', 'Community')
    Apartment = apps.get_model('eaves', 'Apartment')
    AptPrice = apps.get_model('eaves', 'AptPrice')
    AptPrice.objects.all().delete()
    Apartment.objects.all().delete()
    FloorPlan.objects.all().delete()
    Community.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('eaves', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate, clean)
    ]

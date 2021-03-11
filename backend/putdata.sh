#!/bin/bash
rm db.sqlite3
cd common/migrations
rm 0*
cd ../../
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/Users.json
echo "VehicleOwner"
python manage.py loaddata fixtures/VehicleOwner.json
echo "Owner"
python manage.py loaddata fixtures/Owner.json
echo "VehicleModel"
python manage.py loaddata fixtures/VehicleModel.json
echo "Vehicle"
python manage.py loaddata fixtures/Vehicle.json
echo "Providers"
python manage.py loaddata fixtures/Providers.json
echo "Clusters"
python manage.py loaddata fixtures/Clusters.json
echo "Locations"
python manage.py loaddata fixtures/Locations.json
echo "Chstations"
python manage.py loaddata fixtures/ChargingStations.json
echo "chpoints"
python manage.py loaddata fixtures/ChargingPoints.json
echo "pay"
python manage.py loaddata fixtures/Payment.json
echo "session"
python manage.py loaddata fixtures/Session.json



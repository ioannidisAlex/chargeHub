import json

with open('raw datafiles/electric_vehicles_data.json') as ve:
    vehicles = json.load(ve)

database_ve = {}
database_ve['cars'] = []
for v in vehicles['data']:
    vehicle = {}
    vehicle['id']=v['id']
    vehicle['engine_type'] = v['type']
    vehicle['release_year'] = v['release_year']
    vehicle['brand'] = v['brand']
    vehicle['variant'] = v['variant']
    vehicle['model'] = v['model']
    vehicle['ac_ports'] = v['ac_charger']['ports']
    vehicle['ac_usable_phases'] = v['ac_charger']['usable_phases']
    vehicle['ac_max_power'] = v['ac_charger']['max_power']
    vehicle['ac_charging_power'] = v['ac_charger']['power_per_charging_point']
    if v['dc_charger']==None:
        vehicle['dc_ports'] = 'none'
        vehicle['dc_max_power'] = 'none'
        vehicle['dc_charging_curve'] = 'none'
        vehicle['is_default_curve'] = 'none'
    else:
        vehicle['dc_ports'] = v['dc_charger']['ports']
        vehicle['dc_max_power'] = v['dc_charger']['max_power']
        vehicle['dc_charging_curve'] = v['dc_charger']['charging_curve']
        vehicle['is_default_curve'] = v['dc_charger']['is_default_charging_curve']
    vehicle['usable_battery_size'] = v['usable_battery_size']
    vehicle['average_energy_consumption'] = v['energy_consumption']['average_consumption']
    
    database_ve['cars'].append(vehicle)

with open('final data/VehicleModel.json','w') as out1:
      json.dump(database_ve, out1, indent = 4)


import json
import uuid
import random
with open('raw datafiles/electric_vehicles_data.json') as ve:
    vehicles = json.load(ve)

database_ve = {}
database_ve['cars'] = []
database_ve['actc'] = []
i=0
for v in vehicles['data']:
    vehicle = {}
    auto = {}
    vehicle['id']=v['id']
    vehicle['model']="ivasimas.VehicleModel"
    auto['id']=v['id']
    auto['model']="ivasimas.Vehicle"
    fil={}
    fil['engine_type'] = v['type']
    fil['release_year'] = v['release_year']
    fil['brand'] = v['brand']
    fil['variant'] = v['variant']
    fil['model'] = v['model']
    fil['ac_ports'] = v['ac_charger']['ports']
    fil['ac_usable_phases'] = v['ac_charger']['usable_phases']
    fil['ac_max_power'] = v['ac_charger']['max_power']
    fil['ac_charging_power'] = v['ac_charger']['power_per_charging_point']
    if v['dc_charger']==None:
        fil['dc_ports'] = 'none'
        fil['dc_max_power'] = 'none'
        fil['dc_charging_curve'] = 'none'
        fil['is_default_curve'] = 'none'
    else:
        fil['dc_ports'] = v['dc_charger']['ports']
        fil['dc_max_power'] = v['dc_charger']['max_power']
        fil['dc_charging_curve'] = v['dc_charger']['charging_curve']
        fil['is_default_curve'] = v['dc_charger']['is_default_charging_curve']
    fil['usable_battery_size'] = v['usable_battery_size']
    fil['average_energy_consumption'] = v['energy_consumption']['average_consumption']
    vehicle['fields']=fil
    filauto={}
    filauto['model']=v['id']
    filauto['owner']="u"+str(i+3)  
    auto['fields']=filauto      
    database_ve['cars'].append(vehicle)
    database_ve['actc'].append(auto)
    i+=1

with open('final data/VehicleModel.json','w') as out1:
      json.dump(database_ve['cars'], out1, indent = 4)

with open('final data/Vehicle.json','w') as out1:
      json.dump(database_ve['actc'], out1, indent = 4)

with open('final data/Provides.json','w') as out:
    providers={}
    providers['data']=[]
    for i in range(3):
        prov={"id":str(uuid.uuid4()),"model":"ivasimas.Provider","fields":{"provider_name":"prv"+str(i),"user":"u"+str(i)}}
        providers['data'].append(prov)
    json.dump(providers['data'],out,indent = 4)

with open('final data/Clusters.json','w') as out:
    clusters={}
    clusters['data']=[]
    for i in range(2):
        cl={"id":str(uuid.uuid4()),"model":"ivasimas.Provider","fields":{"provider_name":"cls"+str(i)}}
        clusters['data'].append(cl)
    json.dump(clusters['data'],out,indent = 4)

_PAYMENT_METHODS = [
    ("credit_card", "credit card"),
    ("cash", "cash"),
    ("paypal", "paypal"),
    ("coupon", "coupon"),
]

payments=[]
for i in range(500):
    pay={}
    pay['id']=str(uuid.uuid4())
    pay['model']="ivasimas.payments"
    filds={}
    filds['payment_req']=True
    filds['payment_method']=_PAYMENT_METHODS[int(random.uniform(0.0,4.0))][1]
    filds['cost']=random.uniform(8.0,13.0)
    filds['invoice']=""
    filds['user_id']='u'+str(int(random.uniform(3.0,148.0)))
    pay['fields']=filds
    payments.append(pay)

with open('final data/Payment.json','w') as out1:
    json.dump(payments,out1,indent = 4)

with open('raw datafiles/poi3.json') as po:
    points = json.load(po)

charging_stations=[]
for i in range(500):
    station={}
    station['id']=str(uuid.uuid4)
    

with open('final data/ChargingStations.json','w') as out1:
    json.dump(chs,out1,indent = 4)

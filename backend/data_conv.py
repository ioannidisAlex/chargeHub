import json
import random
import uuid

from django.db import connection

db_name = "default."


def randomint(fr, to):
    return int(random.uniform(fr, to))


with open("raw datafiles/electric_vehicles_data.json") as ve:
    vehicles = json.load(ve)

database_ve = {}
database_ve["cars"] = []
database_ve["actc"] = []
i = 0
for v in vehicles["data"]:
    vehicle = {}
    auto = {}
    vehicle["id"] = v["id"]
    vehicle["model"] = db_name + ".VehicleModel"
    auto["id"] = v["id"]
    auto["model"] = db_name + ".Vehicle"
    fil = {}
    fil["engine_type"] = v["type"]
    fil["release_year"] = v["release_year"]
    fil["brand"] = v["brand"]
    fil["variant"] = v["variant"]
    fil["model"] = v["model"]
    fil["ac_ports"] = v["ac_charger"]["ports"]
    fil["ac_usable_phases"] = v["ac_charger"]["usable_phases"]
    fil["ac_max_power"] = v["ac_charger"]["max_power"]
    fil["ac_charging_power"] = v["ac_charger"]["power_per_charging_point"]
    if v["dc_charger"] == None:
        fil["dc_ports"] = "none"
        fil["dc_max_power"] = "none"
        fil["dc_charging_curve"] = "none"
        fil["is_default_curve"] = "none"
    else:
        fil["dc_ports"] = v["dc_charger"]["ports"]
        fil["dc_max_power"] = v["dc_charger"]["max_power"]
        fil["dc_charging_curve"] = v["dc_charger"]["charging_curve"]
        fil["is_default_curve"] = v["dc_charger"]["is_default_charging_curve"]
    fil["usable_battery_size"] = v["usable_battery_size"]
    fil["average_energy_consumption"] = v["energy_consumption"]["average_consumption"]
    vehicle["fields"] = fil
    filauto = {}
    filauto["model"] = v["id"]
    filauto["owner"] = "u" + str(i + 3)
    auto["fields"] = filauto
    database_ve["cars"].append(vehicle)
    database_ve["actc"].append(auto)
    i += 1

with open("final data/VehicleModel.json", "w") as out1:
    json.dump(database_ve["cars"], out1, indent=4)

with open("final data/Vehicle.json", "w") as out1:
    json.dump(database_ve["actc"], out1, indent=4)

with open("final data/Provides.json", "w") as out:
    providers = {}
    providers["data"] = []
    for i in range(3):
        prov = {
            "id": str(uuid.uuid4()),
            "model": db_name + ".Provider",
            "fields": {"provider_name": "prv" + str(i), "user": "u" + str(i)},
        }
        providers["data"].append(prov)
    json.dump(providers["data"], out, indent=4)

with open("final data/Clusters.json", "w") as out:
    clusters = {}
    clusters["data"] = []
    for i in range(2):
        cl = {
            "id": str(uuid.uuid4()),
            "model": db_name + ".Provider",
            "fields": {"provider_name": "cls" + str(i)},
        }
        clusters["data"].append(cl)
    json.dump(clusters["data"], out, indent=4)

_PAYMENT_METHODS = [
    ("credit_card", "credit card"),
    ("cash", "cash"),
    ("paypal", "paypal"),
    ("coupon", "coupon"),
]

payments = []
for i in range(500):
    pay = {}
    pay["id"] = str(uuid.uuid4())
    pay["model"] = db_name + ".payments"
    filds = {}
    filds["payment_req"] = True
    filds["payment_method"] = _PAYMENT_METHODS[randomint(0, 4)][0]
    filds["cost"] = random.uniform(8.0, 13.0)
    filds["invoice"] = ""
    filds["user_id"] = "u" + str(randomint(3, 148))
    pay["fields"] = filds
    payments.append(pay)

with open("final data/Payment.json", "w") as out1:
    json.dump(payments, out1, indent=4)

CONNECTION_TYPE_CHOICES = [
    (7, "Avcon Connector"),
    (4, "Blue Commando (2P+E)"),
    (3, "BS1363 3 Pin 13 Amp"),
    (32, "CCS (Type 1)"),
    (33, "CCS (Type 2)"),
    (16, "CEE 3 Pin"),
    (17, "CEE 5 Pin"),
    (28, "CEE 7/4 - Schuko - Type F"),
    (23, "CEE 7/5"),
    (18, "CEE+ 7 Pin"),
    (2, "CHAdeMO"),
    (13, "Europlug 2-Pin (CEE 7/16)"),
    (1038, "GB-T AC - GB/T 20234.2 (Socket)"),
    (1039, "GB-T AC - GB/T 20234.2 (Tethered Cable)"),
    (1040, "GB-T DC - GB/T 20234.3"),
    (34, "IEC 60309 3-pin"),
    (35, "IEC 60309 5-pin"),
    (5, "LP Inductive"),
    (10, "NEMA 14-30"),
    (11, "NEMA 14-50"),
    (22, "NEMA 5-15R"),
    (9, "NEMA 5-20R"),
    (15, "NEMA 6-15"),
    (14, "NEMA 6-20"),
    (1042, "NEMA TT-30R"),
    (36, "SCAME Type 3A (Low Power)"),
    (26, "SCAME Type 3C (Schneider-Legrand)"),
    (6, "SP Inductive"),
    (1037, "T13 - SEC1011 ( Swiss domestic 3-pin ) - Type J"),
    (30, "Tesla (Model S/X)"),
    (8, "Tesla (Roadster)"),
    (31, "Tesla Battery Swap"),
    (27, "Tesla Supercharger"),
    (1041, "Three Phase 5-Pin (AS/NZ 3123)"),
    (1, "Type 1 (J1772)"),
    (25, "Type 2 (Socket Only)"),
    (1036, "Type 2 (Tethered Connector)"),
    (29, "Type I (AS 3112)"),
    (0, "Unknown"),
    (24, "Wireless Charging"),
    (21, "XLR Plug (4 pin)"),
]

CURRENT_TYPE_CHOICES = [
    (1, "AC - Single Phase"),
    (2, "AC - Three Phase"),
    (3, "DC"),
]

STATUS_TYPE_CHOICES = [
    (0, "Unknown"),
    (10, "Currently Available (Automated Status)"),
    (20, "Currently In Use (Automated Status)"),
    (30, "Temporarily Unavailable"),
    (50, "Operational"),
    (75, "Partly Operational (Mixed)"),
    (100, "Not Operational"),
    (150, "Planned For Future Date"),
    (200, "Removed (Decommissioned)"),
    (210, "Removed (Duplicate Listing)"),
]

USAGE_TYPE_CHOICES = [
    (0, "Unknown"),
    (6, "Private - For Staff"),
    (2, "Private - Restricted Access"),
    (3, "Privately Owned - Notice Required"),
    (1, "Public"),
    (4, "Public - Membership Required"),
    (7, "Public - Notice Required"),
    (5, "Public - Pay At Location"),
]

CHARGER_TYPE_CHOICES = [
    (1, "Low"),
    (2, "Medium"),
    (3, "High"),
]

KW_POWER_CHOICES = [
    (1, "Under 2 kW"),
    (2, "Over 2 kW"),
    (3, "Over 40 kW"),
]

with open("raw datafiles/poi3.json") as po:
    points = json.load(po)

charging_stations = []
charging_points = []
for i in points["data"]:
    station = {}
    # print(i)
    station["id"] = i["UUID"]
    station["model"] = db_name + ".ChargingStation"
    st = {}
    st["cluster"] = clusters["data"][randomint(0, len(clusters["data"]))]["id"]
    st["owner"] = str(uuid.uuid4())
    station["fields"] = st
    charging_stations.append(station)
    for co in i["Connections"]:
        c_points = {}
        c_points["id"] = str(uuid.uuid4())
        c_points["model"] = db_name + ".ChargingPoint"
        poi = {}
        poi["charging_station"] = station["id"]
        poi["connection_type"] = co["ConnectionType"]["ID"]
        poi["current_type"] = co["CurrentTypeID"]
        poi["status_type"] = co["StatusTypeID"]
        poi["location"] = str(uuid.uuid4())
        poi["charger_type"] = co["LevelID"]
        if i["UsageType"] != None:
            poi["usage_type_id"] = i["UsageType"]["ID"]
        poi["kw_power"] = co["PowerKW"]
        poi["usage_cost"] = random.uniform(0.06, 0.18)
        poi["volts_power"] = co["Voltage"]
        poi["amps_power"] = co["Amps"]
        c_points["fields"] = poi
        charging_points.append(c_points)

with open("final data/ChargingStations.json", "w") as out1:
    json.dump(charging_stations, out1, indent=4)
with open("final data/ChargingPoints.json", "w") as out1:
    json.dump(charging_points, out1, indent=4)

with open("raw datafiles/acn_data/caltech_acndata_sessions_12month.json") as se:
    sessions = json.load(se)

acn_data = []

cnt = 0
for s in sessions["_items"]:
    # print(s)
    if s["userInputs"] != None:
        session = {}
        session["id"] = str(uuid.uuid4())
        session["model"] = db_name + ".Session"
        se = {}
        se["payment"] = payments[cnt]["id"]
        # se['protocol']=""
        se["user_comments_ratings"] = str(randomint(1, 5)) + "stars"
        se["provider"] = providers["data"][randomint(0, len(providers))]["id"]
        se["kwh_delivered"] = s["kWhDelivered"]
        se["site_id"] = str(uuid.uuid4())
        se["connect_time"] = s["connectionTime"]
        se["disconnect_time"] = s["disconnectTime"]
        se["done_charging_time"] = s["doneChargingTime"]
        se["charging_point"] = charging_points[randomint(0, len(charging_points))]["id"]
        se["vehicle"] = database_ve["actc"][randomint(0, len(database_ve["actc"]))][
            "id"
        ]
        session["fields"] = se
        acn_data.append(session)
        cnt += 1
        if cnt == 500:
            break

with open("final data/Session.json", "w") as out1:
    json.dump(acn_data, out1, indent=4)

USER_TYPE_CHOICES = [
    (1, "Regular User"),
    (2, "Station Owner"),
    (3, "Energy Provider"),
]

users = []
for i in range(3):
    us = {}
    us["id"] = "u" + str(i)
    us["model"] = db_name + "User"
    u = {}
    u["username"] = "u" + str(i)
    u["passward"] = 3 * u["username"] + "123"
    u["email"] = u["username"] + "@tlMpa.gr"
    u["user_type"] = 3
    us["fields"] = u
    users.append(us)

for i in range(3, 148):
    us = {}
    us["id"] = "u" + str(i)
    us["model"] = db_name + "User"
    u = {}
    u["username"] = "u" + str(i)
    u["passward"] = 3 * u["username"] + "123"
    u["email"] = u["username"] + "@tlMpa.gr"
    u["user_type"] = 1
    us["fields"] = u
    users.append(us)

for i in range(148, 648):
    us = {}
    us["id"] = "u" + str(i)
    us["model"] = db_name + "User"
    u = {}
    u["username"] = "u" + str(i)
    u["passward"] = 3 * u["username"] + "123"
    u["email"] = u["username"] + "@tlMpa.gr"
    u["user_type"] = 2
    us["fields"] = u
    users.append(us)

with open("final data/Users.json", "w") as out1:
    json.dump(users, out1, indent=4)

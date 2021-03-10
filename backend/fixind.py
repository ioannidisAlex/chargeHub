import json

# with open("datafiles/charging_points_europe_json/poi2.json", 'r') as inn:
#     ses = json.load(inn)
#     for i in ses['data']:
#         print(i)
# with open("datafiles/charging_points_europe_json/poi.json", 'r') as inn:
#     data=inn.readlines()
#     with open("datafiles/charging_points_europe_json/poi2.json", 'w') as out:
#         for i in data:
#             out.write(i.strip('\n')+',\n')

with open("datafiles/charging_points_europe_json/poi2.json", "r") as inn:
    data = inn.readlines()
    with open("datafiles/charging_points_europe_json/poi3.json", "w") as out:
        j = 0
        for i in data:
            p = i
            # p=i.replace("{","\n{\n")
            # p=p.replace("}","\n}\n")
            out.write(p)
            j += 1
            if j > 500:
                break

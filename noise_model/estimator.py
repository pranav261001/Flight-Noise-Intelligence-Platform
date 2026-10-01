TYPE_CODE_CATEGORY = {
    "E55P" : "Light",
    "F2TH": "Light",
    "E190" : "Medium",
    "B737" : "Medium",
    "B789" : "Heavy",
    "A333" : "Heavy",
    "B752" : "Medium",
    "B77L" : "Heavy",
    "BCS3" : "Medium",
    "A321" : "Medium",
    "B788" : "Heavy",
    "B77W" : "Heavy",
    "A20N" : "Medium",
    "GLEX" : "Light",
    "B763" : "Heavy",
    "E145" : "Medium",
    "B38M" : "Medium",
    "B39M" : "Medium",
    "CL60" : "Light",
    "A332" : "Heavy",
    "A320" : "Medium",
    "A21N" : "Medium",
    "A319" : "Medium",
    "E35L" : "Light",
    "B738" : "Medium"
    }

ICAO_TYPE_TO_CATEGORY = {
        
    "L4J" : "Heavy",
    "H2T" : "Light",
    "L2T" : "Medium",
    "L1P" : "Light",
    "L1T" : "Medium",
}

CAT_DESC_TO_CATEGORY = {
    "Small (15500 to 75000 lbs)" : "Medium",
    "Heavy (> 300000 lbs)" : "Heavy",

}

REFERENCE_DISTANCE_M = 305
CATEGORY_REFERENCE_SEL = {"Heavy": 105, "Medium": 95, "Light": 80}

def classify_aircrafts(type_code, icao_type, cat_desc):
    if type_code in TYPE_CODE_CATEGORY:
        return TYPE_CODE_CATEGORY.get(type_code)
    elif icao_type in ICAO_TYPE_TO_CATEGORY:
        return ICAO_TYPE_TO_CATEGORY.get(icao_type)
    elif cat_desc in CAT_DESC_TO_CATEGORY:
        return CAT_DESC_TO_CATEGORY.get(cat_desc)
    else:
        return "Medium"

# print( classify_aircrafts("UNKNOWN123", "ZZ", "Heavy (> 300000 lbs)"))

AIRPORT_LAT = 53.4213
AIRPORT_LON = -6.2621
AIRPORT_ELEVATION_M = 74   #--(242ft -> 74m)

import math


# The function replicates the actual formula
def haversine_formula(lat1,lon1, lat2, lon2):
    # distance betwen lat n lon and converting degree to radians
    dlat = (lat2 - lat1)*math.pi/180
    dlon = (lon2 - lon1)*math.pi/180
    R = 6371000
    # convert lat n lat to radians
    lat1 = (lat1)* math.pi / 180
    lat2 = (lat2)* math.pi /180

    a = pow(math.sin(dlat/2),2)+math.cos(lat1)*math.cos(lat2)*pow(math.sin(dlon/2),2)
    c = 2*math.asin(math.sqrt(a))

    # distance
    d = R*c
    return d


def slant_distance(lat, lon, altitude_m):
    ground_distance = haversine_formula(lat, lon, AIRPORT_LAT, AIRPORT_LON)
    altitude_diff = altitude_m - AIRPORT_ELEVATION_M
    return math.sqrt(ground_distance**2 + altitude_diff**2)

# print(haversine_formula(AIRPORT_LAT, AIRPORT_LON, AIRPORT_LAT, AIRPORT_LON))
# print(haversine_formula(AIRPORT_LAT, AIRPORT_LON, AIRPORT_LAT+1, AIRPORT_LON))

# print(slant_distance(AIRPORT_LAT, AIRPORT_LON, AIRPORT_ELEVATION_M))
# print(slant_distance(AIRPORT_LAT, AIRPORT_LON, AIRPORT_ELEVATION_M+1000))

def sel_estimate(category, distance_m):
    reference_sel = CATEGORY_REFERENCE_SEL[category]
    distance_m = max(distance_m, 1)  # to log10 value werror if distance = 0
    sel = reference_sel - 20 * math.log10(distance_m/ REFERENCE_DISTANCE_M)
    return sel

# print( sel_estimate("Heavy", REFERENCE_DISTANCE_M * 2))
# print( sel_estimate("Heavy", REFERENCE_DISTANCE_M / 2))
# print( sel_estimate("Heavy", REFERENCE_DISTANCE_M))

# To build the Lden bucket function the UTC time has to be converted to irish local time

from zoneinfo import ZoneInfo
import datetime as dt
IRISH_TZ = ZoneInfo("Europe/Dublin")

def to_irish_tz(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    else:
        dt = dt

    return dt.astimezone(IRISH_TZ)


dt_time = dt.datetime(2026, 7, 1, 22, 00, 0)
# print(dt.tzinfo)

dt_1 = to_irish_tz(dt_time)
# print(dt_1.hour)

def time_bucket(timestamp):
    time = to_irish_tz(timestamp)
    hour = time.hour

    if hour >=7 and hour<19:
        return "Day"
    elif hour >=19 and hour <23:
        return "Evening"
    else: 
        return "Night"
# print(time_bucket(dt_time))

def period_leq(sel_list, period_in_secs):
    total_energy = sum(10**(sel/10) for sel in sel_list)
    total_energy = max(total_energy, 0.1)
    Leq = 10*math.log10(total_energy/period_in_secs)
    return Leq

# Day = 43,200 sec
# Eve = 14,400
# Night = 28,800

def lden(ld, le, ln):
    day = (12/24) * 10**(ld/10)
    eve = (4/24) * 10**((le + 5)/10)
    night = (8/24) * 10**((ln + 10)/10)

    lden_value = 10 * math.log10(day + eve + night)
    return lden_value

# print(period_leq([], 43200))
# print(period_leq([100,300], 43200))
# print(lden(60,60,60))
# print(lden(period_leq([], 14400), period_leq([], 14400), period_leq([], 14400)))
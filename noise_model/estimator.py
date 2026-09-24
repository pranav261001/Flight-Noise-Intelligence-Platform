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

print( classify_aircrafts("UNKNOWN123", "ZZ", "Heavy (> 300000 lbs)"))


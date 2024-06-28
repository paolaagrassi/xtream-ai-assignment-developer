from enum import Enum

class DiamondColorEnum(str,Enum):
    d = "D"
    e = "E"
    f = "F"
    g = "G"
    h = "H"
    i = "I"
    j = "J"

class DiamondClarityEnum(str, Enum):
    iF = "IF"
    vvs1 = "VVS1"
    vvs2 = "VVS2"
    vs1 = "VS1"
    vs2 = "VS2"
    si1 = "SI1"
    si2 = "SI2"
    i1 = "I1"

class DiamondCutEnum(str, Enum):
    fair = "Fair"
    good = "Good"
    very_good = "Very Good"
    ideal = "Ideal"
    premium = "Premium"

class DiamondColumnsEnum(str, Enum):
    CARAT = 'carat'
    COLOR = 'color'
    CLARITY = 'clarity'
    CUT = 'cut'
    PRICE = 'price'
    DEPTH = 'depth'
    TABLE = 'table'
    X = 'x'
    Y = 'y'
    Z = 'z'
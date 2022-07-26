from enum import IntEnum


class SpeedLimit(IntEnum):
    LIMIT_20 = 0
    LIMIT_30 = 1
    LIMIT_50 = 2
    LIMIT_60 = 3
    LIMIT_70 = 4
    LIMIT_80 = 5
    LIMIT_100 = 7
    LIMIT_120 = 8


class Instruction(IntEnum):
    NO_TRAFF_BOTH = 15
    NO_TRUCKS = 16
    NO_ENTRY = 17
    GO_RIGHT = 33
    GO_LEFT = 34
    GO_STRAIGHT = 35
    GO_R_OR_STR = 36
    GO_L_OR_STR = 37
    KEEP_RIGHT = 38
    KEEP_LEFT = 39


class EndRestrict(IntEnum):
    END_80 = 6
    END_OVERTAKING = 41
    END_OVERTAKING_T = 42


class DangerLong(IntEnum):
    GENERAL = 18
    UNEVEN = 22
    SLIPPERY = 23
    NARROWS = 24
    CONSTRUCTION = 25
    SNOW = 30
    ANIMALS = 31


class DangerShort(IntEnum):
    BEND_LEFT = 19
    BEND_RIGHT = 20
    BEND = 21
    TRAFFIC_SIGN = 26
    ROUNDABOUT = 40
    PED_CROSSING = 27
    SCHOOL_CROSSING = 28
    CYCLES_CROSSING = 29


class Overtaking(IntEnum):
    NO_OVERTAKING = 9
    NO_OVERTAKING_T = 10


class GiveWay(IntEnum):
    PRIO_AT_NEXT = 11
    PRIO_ROAD = 12
    GIVE_WAY = 13
    STOP = 14


class Parking(IntEnum):
    NO_STOPP = 43
    PARKING = 44
    NO_PARKING = 45


class Person(IntEnum):
    PEDESTRIAN = 46
    BIKE = 47


class Slot1(IntEnum):
    END_ALL_SPEED = 32
    LIMIT_20 = 0
    LIMIT_30 = 1
    LIMIT_50 = 2
    LIMIT_60 = 3
    LIMIT_70 = 4
    LIMIT_80 = 5
    LIMIT_100 = 7
    LIMIT_120 = 8


class Slot2(IntEnum):
    NO_OVERTAKING = 9
    NO_OVERTAKING_T = 10

    GENERAL = 18
    UNEVEN = 22
    SLIPPERY = 23
    NARROWS = 24
    CONSTRUCTION = 25
    SNOW = 30
    ANIMALS = 31

class Slot3(IntEnum):
    PRIO_AT_NEXT = 11
    PRIO_ROAD = 12
    GIVE_WAY = 13
    STOP = 14

class Slot4(IntEnum):
    NO_TRAFF_BOTH = 15
    NO_TRUCKS = 16
    NO_ENTRY = 17
    GO_RIGHT = 33
    GO_LEFT = 34
    GO_STRAIGHT = 35
    GO_R_OR_STR = 36
    GO_L_OR_STR = 37
    KEEP_RIGHT = 38
    KEEP_LEFT = 39

    BEND_LEFT = 19
    BEND_RIGHT = 20
    BEND = 21
    TRAFFIC_SIGN = 26
    ROUNDABOUT = 40
    PED_CROSSING = 27
    SCHOOL_CROSSING = 28
    CYCLES_CROSSING = 29

    NO_STOPP = 43
    PARKING = 44
    NO_PARKING = 45
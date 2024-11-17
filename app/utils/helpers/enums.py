import enum

class Status(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    PERSONAL_ASSISTANT = "PERSONAL_ASSISTANT"

class PlatformTypes(int, enum.Enum):
    DOCTOR = 1
    ENGINEER = 2
    TEACHER = 3
    PUBLIC_FIGURE = 4
    BUSINESS = 5
    LAWYER = 6


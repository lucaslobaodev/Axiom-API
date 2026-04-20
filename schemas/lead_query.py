from enum import Enum

class LeadOrderBy(str, Enum):
    id = "id"
    name = "name"
    email = "email"
    phone = "phone"

class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"

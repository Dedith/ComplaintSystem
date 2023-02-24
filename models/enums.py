import enum


class RoleType(str, enum.Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class State(str, enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

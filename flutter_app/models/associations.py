""" Associations
"""

from sqlalchemy import Column, ForeignKey, String, Table, DateTime, func, Enum
from flutter_app.db.database import Base


user_institution_association = Table(
    "user_institution",
    Base.metadata,
    Column(
        "user_id", String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "institution_id",
        String,
        ForeignKey("institutions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # ),
    # Column(
    #     "role",
    #     Enum("admin", "user", "guest", "owner", name="user_org_role"),
    #     nullable=False,
    #     default="user",
    # ),
    # Column(
    #     "status",
    #     Enum("member", "suspended", "left", name="user_org_status"),
    #     nullable=False,
    #     default="member",
    # ),
)

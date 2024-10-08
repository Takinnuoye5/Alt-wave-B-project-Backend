""" User data model
"""

from sqlalchemy import Column, String, text, Boolean
from sqlalchemy.orm import relationship
from flutter_app.models.oauth import OAuth
from flutter_app.models.associations import user_institution_association
from flutter_app.models.base_model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=text("true"))
    is_super_admin = Column(Boolean, server_default=text("false"))
    is_deleted = Column(Boolean, server_default=text("false"))
    is_verified = Column(Boolean, server_default=text("false"))

    profile = relationship(
        "Profile", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    institutions = relationship(
        "Institution", secondary=user_institution_association, back_populates="users"
    )
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    activity_logs = relationship(
        "ActivityLog", back_populates="user", cascade="all, delete-orphan"
    )
    token_login = relationship("TokenLogin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    oauth = relationship("OAuth", back_populates="user", uselist=False, cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan") 
    blogs = relationship("Blog", back_populates="author", cascade="all, delete-orphan") 
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="user", cascade="all, delete-orphan")
    blog_likes = relationship("BlogLike", back_populates="user", cascade="all, delete-orphan")
    blog_dislikes = relationship("BlogDislike", back_populates="user", cascade="all, delete-orphan")
    comment_likes = relationship("CommentLike", back_populates="user", cascade="all, delete-orphan")
    comment_dislikes = relationship("CommentDislike", back_populates="user", cascade="all, delete-orphan")
    notification_setting = relationship("NotificationSetting", back_populates="user",  cascade="all, delete-orphan", uselist=False)
    virtual_cards = relationship("VirtualCard", back_populates="user", cascade="all, delete-orphan")



    
    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict.pop("password")
        return obj_dict

    def __str__(self):
        return self.email

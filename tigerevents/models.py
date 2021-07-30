from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from datetime import datetime
from tigerevents import db, login_manager
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os

# get user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

###############################################################################
# Association Models/Tables                                                   #
###############################################################################
# 1. Events saved by user
class Saved(db.Model):
    __tablename__ = 'a_saved'
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('nice_user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('nice_event.id'), primary_key=True)

    # extra data
    going = db.Column(db.Boolean, unique=False, default=False)

    event = db.relationship("Event", back_populates="participants" )
    user = db.relationship("User", back_populates="events")

a_follow = db.Table("follow",
                    db.Column("user_id", db.Integer, db.ForeignKey('nice_user.id')),
                    db.Column("org_id", db.Integer, db.ForeignKey('nice_organization.id'))
                   )

a_org_tags = db.Table("org_tags",
                      db.Column("org_id", db.Integer, db.ForeignKey('nice_organization.id')),
                      db.Column("tag_id", db.Integer, db.ForeignKey('nice_tag.id'))
                     )

a_event_tags = db.Table("event_tags",
                        db.Column("event_id", db.Integer, db.ForeignKey('nice_event.id')),
                        db.Column("tag_id", db.Integer, db.ForeignKey('nice_tag.id'))
                       )

a_user_tags = db.Table("user_tags",
                        db.Column("user_id", db.Integer, db.ForeignKey('nice_user.id')),
                        db.Column("tag_id", db.Integer, db.ForeignKey('nice_tag.id'))
                      )

###############################################################################

###############################################################################
# Class Models                                                                #
###############################################################################
class User(db.Model, UserMixin):
    __tablename__ = 'nice_user'
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ical_uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    urole = db.Column(db.String(60), nullable=False)

    # relationships - all many to many
    # association object
    events = db.relationship("Saved", 
                             back_populates="user", 
                             cascade="all, delete-orphan")

    # association table
    following = db.relationship("Organization",
                                secondary=a_follow,
                                back_populates="followers",
                               )

    tags = db.relationship("Tag",
                           secondary=a_user_tags,
                           back_populates="users") 
                           
    # functions/methods
    def __repr__(self):
        return f"User('{self.email}')"
    
    # Follow an organization
    def follow(self, org):
        if not org in self.following:
            self.following.append(org)
            return self
    
    
    # Unfollow an organization.
    def unfollow(self, org):
        if org in self.following:
            self.following.remove(org)
            return self
    
    # Is user going to event?
    def is_going(self, event):
        if self.is_saved(event):
            return Saved.query.filter_by(event_id = event.id).filter_by(user_id = self.id)[0].going
        else:
            return False

    # return all events that the user is going to
    def going_to(self):
        return [assoc.event for assoc in Saved.query.filter_by(user_id = self.id).filter_by(going = True).all()]
    
    # Returns true if the user has saved the event
    def is_saved(self, event):
        return len(Saved.query.filter_by(event_id = event.id).filter_by(user_id = self.id).all()) > 0

    # Does the event clash with the user's calendar?
    def clash(self, event):
        events = [assoc.event for assoc in Saved.query.filter_by(user_id = self.id).filter_by(going = True).all()]

        for myevent in events:
            if myevent.event_clash(event):
                return True

        return False
    
    # Get iCal link for syncing with external calendar
    def get_link(self):
        return os.path.join("tigerevents.herokuapp.com", self.ical_uuid.hex + ".ics")

    # returns all events hosted by organizations followed by the user
    def org_events(self):
        events = []
        for org in self.following:
            events.extend(org.events)
        return events
    
    """
    Returns all events that the user has hosted
    """
    def host_of(self):
        if self.urole == "Host":
            return self.following[0]
        else:
            return None        
###############################################################################
###############################################################################
class EventQuery(BaseQuery, SearchQueryMixin):
    pass

class Event(db.Model):
    __tablename__='nice_event'
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_campaign.jpg")
    location = db.Column(db.String(120), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    search_vector = db.Column(TSVectorType('title','description','location'))
    
    # relationships
    # association object
    participants = db.relationship("Saved", 
                                   back_populates="event", 
                                   cascade="all, delete-orphan")

    tags = db.relationship("Tag",
                           secondary=a_event_tags,
                           back_populates="events")
    
    org_id = db.Column(db.Integer, db.ForeignKey("nice_organization.id"), nullable=False)

    # functions/methods
    def __repr__(self):
        return f"Event('{self.title}', '{self.date_posted}')"

    # do these events clash
    def event_clash(self, event):
        start1, end1 = self.start_date, self.end_date
        start2, end2 = event.start_date, event.end_date

        # start or end at the same time
        if ((start1 == start2) or (end1 == end2)):
            return True

        # does one event begin before the other ends
        if(start1 < start2):
            if (start2 < end1):
                return True
        else:
            if (start1 < end2):
                return True

        return False 
###############################################################################
###############################################################################
class Organization(db.Model):
    __tablename__='nice_organization'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_campaign.jpg")

    # relationships
    events = db.relationship("Event", backref="host", lazy=True)

    followers = db.relationship("User",
                                secondary=a_follow,
                                back_populates="following",
                                )
    
    tags = db.relationship("Tag",
                           secondary=a_org_tags,
                           back_populates="organizations")

    # functions/methods
    def __repr__(self):
        return f"Event('{self.name}', '{self.date_created}')"
###############################################################################
###############################################################################
class Tag(db.Model):
    __tablename__='nice_tag'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # relationship
    organizations = db.relationship("Organization",
                                    secondary=a_org_tags,
                                    back_populates="tags")

    events = db.relationship("Event",
                             secondary=a_event_tags,
                             back_populates="tags")
    
    users = db.relationship("User",
                             secondary=a_user_tags,
                             back_populates="tags")

    # functions/methods
    def __repr__(self):
        return f"Event('{self.name}')"

    # get all events with this tag
    def filter_events(self):
        return self.events
###############################################################################

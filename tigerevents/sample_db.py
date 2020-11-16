from tigerevents import db
from tigerevents.models import User, Event, Saved, Organization, Tag
from datetime import datetime

db.drop_all()
db.create_all()

# dummy users
user1 = User(name="Moin", email="moin@princeton.edu", password="moin_events")
user2 = User(name="Faisal", email="ffakhro@princeton.edu", password="faisal_events")
user3 = User(name="Michael", email="maf6@princeton.edu", password="michael_events")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

# dummy organizations
org1 = Organization(name="Career Center", description="We do career related events")
org2 = Organization(name="Robotics Club", description="We do cool robotics stuff")
org3 = Organization(name="Whitman", description="We basically give away free stuff")
org4 = Organization(name="SPIA", description="We changed our name recently we still the best")
db.session.add(org1)
db.session.add(org2)
db.session.add(org3)
db.session.add(org4)
db.session.commit()

# dummy events
event1 = Event(title="Microsoft Mixer", description="Meet engineers and hiring execs", 
               location="Jane Street Library", date=datetime(2020, 12, 25, 10), host=org1)
event2 = Event(title="Whit Study Break", description="Enjoy sushi with Insiya", 
               location="Whitman Common Room", date=datetime(2020, 11, 20, 18), host=org3)
event3 = Event(title="Robotics Club Meetup", description="Introduction to the robotics club", 
               location="Studio Lab, Fine Hall", date=datetime(2020, 11, 25, 16), host=org2)
event4 = Event(title="Discussing the 2020 Election", description="Discuss the elction with the panel", 
               location="A12, Clio Hall", date=datetime(2020, 11, 28, 14), host=org4)
event5 = Event(title="Free Stuff", description="T-Shirts and Ice Cream", 
               location="Whitman Common Room", date=datetime(2020, 11, 18, 20), host=org3)  
                 
db.session.add(event1)
db.session.add(event2)
db.session.add(event3)
db.session.add(event4)
db.session.add(event5)
db.session.commit()

# dummy tags
tag1 = Tag(name="Study Breaks")
tag2 = Tag(name="Residential Colleges")
tag3 = Tag(name="Technology")
tag4 = Tag(name="Panel Discussion")
tag5 = Tag(name="Politics")
tag6 = Tag(name="Career")
tag7 = Tag(name="Free Stuff")
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)
db.session.add(tag5)
db.session.add(tag6)
db.session.add(tag7)
db.session.commit()

# creating event-user relationships
# user1: S = [1,2,3] G = [2]
# user2: S = [1,3,4,5] G = [1,4]
# user3: S = [2,3,4] G = [2,3,4]

# user1
save11 = Saved(going=False)
save12 = Saved(going=True)
save13 = Saved(going=False)
save11.event = event1
save12.event = event2
save13.event = event3 
save11.user = user1
save12.user = user1
save13.user = user1

# user2 S = [1,3,4,5] G = [1,4]
save21 = Saved(going=True)
save23 = Saved(going=False)
save24 = Saved(going=True)
save25 = Saved(going=False)
save21.event = event1
save23.event = event3
save24.event = event4 
save25.event = event5 
save21.user = user2
save23.user = user2
save24.user = user2
save25.user = user2

# user3 S = [2,3,4] G = [2,3,4]
save32 = Saved(going=True)
save33 = Saved(going=True)
save34 = Saved(going=True)
save32.event = event2
save33.event = event3
save34.event = event4 
save32.user = user3
save33.user = user3
save34.user = user3

db.session.add(save11)
db.session.add(save12)
db.session.add(save13)
db.session.add(save21)
db.session.add(save23)
db.session.add(save24)
db.session.add(save25)
db.session.add(save32)
db.session.add(save33)
db.session.add(save34)
db.session.commit()

# create user-organization relationships
# user1: F = [2,3]
# user2: F = [1,4]
# user3: F = [1,2,3,4]
user1.following.extend((org2, org3))
user2.following.extend((org1, org4))
user3.following.extend((org1, org2, org3, org4))
db.session.commit()


# add tags to organizations
# org1 = [3,6]
# org2 = [3]
# org3 = [1,2,7]
# org4 = [4,5]
org1.tags.extend((tag3, tag6))
org2.tags.append(tag3)
org3.tags.extend((tag1, tag2, tag7))
org4.tags.extend((tag4, tag5))
db.session.commit()

# add tags to events
# event1 = [3,6,7], event2 = [1,2,7], event3 = [3]
# event4 = [4,5], event5 = [1,2,7]
event1.tags.extend((tag3, tag6, tag7))
event2.tags.extend((tag1, tag2, tag7))
event3.tags.append(tag3)
event4.tags.extend((tag4, tag5))
event5.tags.extend((tag1, tag2, tag7))
db.session.commit()

# add tags to users
# user1 = [3,4], user2 = [2,7], user3= [1,5,6]
user1.tags.extend((tag3, tag4))
user2.tags.extend((tag2, tag7))
user3.tags.extend((tag1, tag5, tag6))
db.session.commit()



    



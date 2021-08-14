from tigerevents import db, bcrypt
from tigerevents.models import User, Event, Saved, Organization, Tag
from datetime import datetime

db.drop_all()
db.configure_mappers()
db.create_all()
print("Step 1: Created tables.")

# dummy organizations
org1 = Organization(name="Career Center", description="We do career related events")
org2 = Organization(name="Robotics Club", description="We do cool robotics stuff")
org3 = Organization(name="Whitman", description="We basically give away free stuff")
org4 = Organization(name="SPIA", description="We changed our name recently we still the best")
org5 = Organization(name="COS", description="beep boop beep boop")
db.session.add(org1)
db.session.add(org2)
db.session.add(org3)
db.session.add(org4)
db.session.add(org5)
db.session.commit()
print("Step 2: Added organizations.")

# dummy users
pass1 = bcrypt.generate_password_hash("moin_events").decode("utf-8")
pass2 = bcrypt.generate_password_hash("faisal_events").decode("utf-8")
pass3 = bcrypt.generate_password_hash("michael_events").decode("utf-8")
pass4 = bcrypt.generate_password_hash("rick_events").decode("utf-8")
pass5 = bcrypt.generate_password_hash("marina_events").decode("utf-8")
pass6 = bcrypt.generate_password_hash("emma_events").decode("utf-8")
pass7 = bcrypt.generate_password_hash("jess_events").decode("utf-8")

user1 = User(name="Moin", email="moin@princeton.edu", password=pass1, urole='Host', org=org5)
user2 = User(name="Faisal", email="ffakhro@princeton.edu", password=pass2, urole='User')
user3 = User(name="Michael", email="maf6@princeton.edu", password=pass3, urole='User')
user4 = User(name="Rick", email="rick@princeton.edu", password=pass4, urole='Host', org=org3)
user5 = User(name="Marina", email="marina@princeton.edu", password=pass5, urole='Host', org=org2)
user6 = User(name="Emma", email="emma@princeton.edu", password=pass6, urole='Host', org=org4)
user7 = User(name="Jess", email="jess@princeton.edu", password=pass7, urole='Host', org=org1)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)
db.session.add(user6)
db.session.add(user7)
db.session.commit()
print("Step 3: Added users.")
print("Step 4: Assigned officers.")

""" 
Officers:
User      | Organization
1           5
4           3
5           2
6           4
7           1
"""

# dummy events
event1 = Event(title="Microsoft Mixer", description="Meet engineers and hiring execs", 
               location="Jane Street Library", 
               start_date=datetime(2020, 12, 25, 10), end_date = datetime(2020, 12, 25, 12), 
               host=org1, creator= user7)
event2 = Event(title="Whit Study Break", description="Enjoy sushi with Insiya", 
               location="Whitman Common Room",
               start_date=datetime(2020, 11, 20, 18), end_date = datetime(2020, 11, 20, 19),
               host=org3, creator=user4)
event3 = Event(title="Robotics Club Meetup", description="Introduction to the robotics club", 
               location="Studio Lab, Fine Hall",
               start_date=datetime(2020, 12, 25, 11), end_date = datetime(2020, 12, 25, 12),
               host=org2, creator= user5)
event4 = Event(title="Discussing the 2020 Election", description="Discuss the elction with the panel", 
               location="A12, Clio Hall",
               start_date=datetime(2020, 11, 28, 14), end_date = datetime(2020, 11, 28, 15),
               host=org4, creator=user6)
event5 = Event(title="Free Stuff", description="T-Shirts and Ice Cream", 
               location="Whitman Common Room",
               start_date=datetime(2020, 11, 28, 14, 30), end_date = datetime(2020, 11, 28, 16),
               host=org3, creator=user4) 
event6 = Event(title="COS Puzzle Hunt", description="Cryptic prizes", 
               location="Friend Center",
               start_date=datetime(2020, 11, 28, 14, 30), end_date = datetime(2020, 11, 28, 16),
               host=org5, creator=user1) 
 
                 
db.session.add(event1)
db.session.add(event2)
db.session.add(event3)
db.session.add(event4)
db.session.add(event5)
db.session.add(event6)
db.session.commit()
print("Step 5: Added events.")

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
print("Step 6: Added tags.")

# creating event-user relationships
# user2: S = [1,3,4,5] G = [1,4]
# user3: S = [2,3,4] G = [2,3,4]
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

db.session.add(save21)
db.session.add(save23)
db.session.add(save24)
db.session.add(save25)
db.session.add(save32)
db.session.add(save33)
db.session.add(save34)

db.session.commit()
print("Step 7: Created user-event (saved) relationships.")

# create user-organization relationships
# user1: F = [2,3]
# user2: F = [1,4]
# user3: F = [1,2,3,4]
user2.following.extend((org1, org4))
user3.following.extend((org1, org2, org3, org4))
db.session.commit()
print("Step 8: Added user following organizations.")

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
print("Step 9: Added tags to organizations.")

# add tags to events
# event1 = [3,6,7], event2 = [1,2,7], event3 = [3]
# event4 = [4,5], event5 = [1,2,7]
event1.tags.extend((tag3, tag6, tag7))
event2.tags.extend((tag1, tag2, tag7))
event3.tags.append(tag3)
event4.tags.extend((tag4, tag5))
event5.tags.extend((tag1, tag2, tag7))
db.session.commit()
print("Step 10: Added tags to events.")

# add tags to users
# user1 = [3,4], user2 = [2,7], user3= [1,5,6]
user2.tags.extend((tag2, tag7))
user3.tags.extend((tag1, tag5, tag6))
db.session.commit()
print("Step 11: Added tags to users.")



    



from tigerevents import db
from tigerevents.models import User, Event, Saved, Organization, Tag

db.drop_all()
db.create_all()

def create_sample_db():

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
    event1 = Event(title="Microsoft Mixer", description="Meet engineers and hiring execs", host=org1)
    event2 = Event(title="Whit Study Break", description="Enjoy sushi with Insiya", host=org3)
    event3 = Event(title="Robotics Club Meetup", description="Introduction to the robotics club", host=org2)
    event4 = Event(title="Discussing the 2020 Election", description="Discuss the elction with the panel", host=org4)
    event5 = Event(title="Free Stuff", description="T-Shirts and Ice Cream", host=org3)    
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
    user1.following.append(org2)
    user1.following.append(org3)
    user2.following.append(org1)
    user2.following.append(org4)
    user3.following.append(org1)
    user3.following.append(org2)
    user3.following.append(org3)
    user3.following.append(org4)

    # add tags to organizations
    # org1 = [3,6]
    # org2 = [3]
    # org3 = [1,2,7]
    # org4 = [4,5]
    org1.tags.append(tag3)
    org1.tags.append(tag6)
    org2.tags.append(tag3)
    org3.tags.append(tag1)
    org3.tags.append(tag2)
    org3.tags.append(tag7)
    org4.tags.append(tag4)
    org4.tags.append(tag5)

    # add tags to events
    # add tags to users

def user_event_test():

    create_sample_db()

    # getting all users
    users = User.query.all()

    def print_user_data():
        # all the events each user has saved and is going to
        user1_saved = [a.event.title for a in users[0].events if a.going is False]
        user1_going = [a.event.title for a in users[0].events if a.going]
        print("----------------------------------------------------------------")
        print(users[0].name, "is going to:")
        print(*user1_going, sep=', ')
        print(users[0].name, "is interested in:")
        print(*user1_saved, sep=', ')
        print("----------------------------------------------------------------")

        user2_saved = [a.event.title for a in users[1].events if a.going is False]
        user2_going = [a.event.title for a in users[1].events if a.going]
        print("----------------------------------------------------------------")
        print(users[1].name, "is going to:")
        print(*user2_going, sep=', ')
        print(users[1].name, "is interested in:")
        print(*user2_saved, sep=', ')
        print("----------------------------------------------------------------")

        user3_saved = [a.event.title for a in users[2].events if a.going is False]
        user3_going = [a.event.title for a in users[2].events if a.going]
        print("----------------------------------------------------------------")
        print(users[2].name, "is going to:")
        print(*user3_going, sep=', ')
        print(users[2].name, "is interested in:")
        print(*user3_saved, sep=', ')
        print("----------------------------------------------------------------")

    def change_user_data():
        # user1: S = [1,3]-->[1] G = [2]-->[2,3]
        Saved.query.filter_by(user=User.query.get(1), event=Event.query.get(3))[0].going = True
        # user2: S = [3,5]-->[1,3,5] G = [1,4]-->[4]
        Saved.query.filter_by(user=User.query.get(2), event=Event.query.get(1))[0].going = False
        # user3: S = []-->[4] G = [2,3,4]-->[2,3]
        Saved.query.filter_by(user=User.query.get(3), event=Event.query.get(4))[0].going = False

    print_user_data()
    change_user_data()
    print_user_data()

# tests the relationship between users and organization: Following, Unfollowing
def user_org_test():

    create_sample_db()

    # getting all users
    users = User.query.all()
    orgs = Organization.query.all()

    def print_user_data():
        # all the organizations each user has followed
        user1 = [org.name for org in users[0].following]
        print("----------------------------------------------------------------")
        print(users[0].name, "follows:")
        print(*user1, sep=', ')
        print("----------------------------------------------------------------")

        user2 = [org.name for org in users[1].following]
        print("----------------------------------------------------------------")
        print(users[1].name, "follows:")
        print(*user2, sep=', ')
        print("----------------------------------------------------------------")

        user3 = [org.name for org in users[2].following]
        print("----------------------------------------------------------------")
        print(users[2].name, "follows:")
        print(*user3, sep=', ')
        print("----------------------------------------------------------------")
    
    def print_org_data():
        # followers of each organization
        org1 = [u.name for u in orgs[0].followers]
        print("----------------------------------------------------------------")
        print(orgs[0].name, "followers:")
        print(*org1, sep=', ')
        print("----------------------------------------------------------------")

        org2 = [u.name for u in orgs[1].followers]
        print("----------------------------------------------------------------")
        print(orgs[1].name, "followers:")
        print(*org2, sep=', ')
        print("----------------------------------------------------------------")
    
    def change_user_data():
        # user1: F = [2,3]-->[3]
        User.query.get(1).following.remove(Organization.query.get(2))
        # user2: F = [1,4]-->[1,3,4]
        User.query.get(2).following.append(Organization.query.get(3))
        # user3: F = [1,2,3,4]-->[1,4]
        User.query.get(3).following.remove(Organization.query.get(2))
        User.query.get(3).following.remove(Organization.query.get(3))

    print_user_data()
    print_org_data()
    change_user_data()
    print_user_data()
        

def org_tag_test():

    create_sample_db()

    orgs = Organization.query.all()
    tags = Tag.query.all()

    def print_org_data():
        org1 = [tag.name for tag in orgs[0].tags]
        print("----------------------------------------------------------------")
        print(orgs[0].name, "tags:")
        print(*org1, sep=', ')
        print("----------------------------------------------------------------")

        org2 = [tag.name for tag in orgs[1].tags]
        print("----------------------------------------------------------------")
        print(orgs[1].name, "tags:")
        print(*org2, sep=', ')
        print("----------------------------------------------------------------")

        org3 = [tag.name for tag in orgs[2].tags]
        print("----------------------------------------------------------------")
        print(orgs[2].name, "tags:")
        print(*org3, sep=', ')
        print("----------------------------------------------------------------")

        org4 = [tag.name for tag in orgs[3].tags]
        print("----------------------------------------------------------------")
        print(orgs[3].name, "tags:")
        print(*org4, sep=', ')
        print("----------------------------------------------------------------")

    def print_tag_data():
        tag1 = [org.name for org in tags[0].organizations]
        print("----------------------------------------------------------------")
        print(tags[0].name, "Organizations:")
        print(*tag1, sep=', ')
        print("----------------------------------------------------------------")

        tag3 = [org.name for org in tags[2].organizations]
        print("----------------------------------------------------------------")
        print(tags[2].name, "Organizations:")
        print(*tag3, sep=', ')
        print("----------------------------------------------------------------")

        tag7 = [org.name for org in tags[6].organizations]
        print("----------------------------------------------------------------")
        print(tags[6].name, "Organizations:")
        print(*tag7, sep=', ')
        print("----------------------------------------------------------------")

    print_org_data()
    print_tag_data()




    



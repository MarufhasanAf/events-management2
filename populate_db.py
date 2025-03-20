import os
import django
from faker import Faker
import random
from events.models import Category, Event, Participant 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings') 


def populate_db():
    fake = Faker()

    # Define location choices
    LOCATION_CHOICES = ['DHAKA', 'CHITTAGONG', 'KHULNA', 'RAJSHAHI', 'BARISAL', 'SYLHET', 'RANGPUR', 'MYMENSINGH']

    # Create Categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.text()
    ) for _ in range(5)]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.sentence(nb_words=3),
            description=fake.text(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=random.choice(LOCATION_CHOICES),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        assigned_events = random.sample(events, random.randint(1, 5))
        participant.events.set(assigned_events)
        participants.append(participant)
    print(f"Created {len(participants)} participants and assigned them to events.")

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()

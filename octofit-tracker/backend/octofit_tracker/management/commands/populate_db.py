from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient, ASCENDING

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', ASCENDING)], unique=True)

        # Teams
        teams = [
            {'name': 'Team Marvel'},
            {'name': 'Team DC'}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'Team DC'}
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user': 'Spider-Man', 'activity': 'Web Swinging', 'duration': 30},
            {'user': 'Iron Man', 'activity': 'Flight Training', 'duration': 45},
            {'user': 'Wonder Woman', 'activity': 'Lasso Practice', 'duration': 40},
            {'user': 'Batman', 'activity': 'Martial Arts', 'duration': 50}
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'name': 'Super Strength', 'suggested_for': ['Wonder Woman', 'Spider-Man']},
            {'name': 'Tech Endurance', 'suggested_for': ['Iron Man', 'Batman']}
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'user': 'Spider-Man', 'points': 100},
            {'user': 'Iron Man', 'points': 90},
            {'user': 'Wonder Woman', 'points': 110},
            {'user': 'Batman', 'points': 95}
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

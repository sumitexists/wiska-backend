import random

import lorem
from django.core.management.base import BaseCommand

from accounts.models import User
from anonymous.models import Community, Post


def randomCommunityNameGenerator():
    community_names = [
        # Short Names
        "Nexus", "Haven", "Orbit", "Pulse", "Forge", "Drift", "Hive", "Nova", "Vertex", "Echo",

        # Startup Names
        "FounderCircle", "VentureVault", "StartupSyndicate", "HustleHub", "BuildScale", "InnovationNation", "GrowthLab", "TheFoundry", "CreatorEconomy", "MomentumClub",

        # AI / Future Names
        "NeuralNexus", "AIAssembly", "QuantumMinds", "FutureFoundry", "SyntheticSociety", "DeepThinkers", "PromptMasters", "NextGenHub", "BrainwaveCollective", "DataDynasty",

        # Gen Z / Modern Names
        "VibeSociety", "AfterHours", "NoContextClub", "ChaosCollective", "MidnightMinds", "DigitalNomads", "TheInnerCircle", "MainCharacterEnergy", "SocialLab", "OffbeatCrew",
    ]

    available_names = [
        candidate
        for candidate in community_names
        if not Community.objects.filter(name=candidate).exists()
    ]

    if available_names:
        return random.choice(available_names)

    while True:
        fallback_name = f"Community{random.randint(10000, 99999)}"
        if not Community.objects.filter(name=fallback_name).exists():
            return fallback_name


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=100,
            help="Indicates the number of communities to create",
        )
        parser.add_argument(
            "--app",
            type=str,
            help="Indicates the app to populate (e.g., 'anonymous')",
        )
    def handle(self, *args, **kwargs):
        app = kwargs["app"]
        total = kwargs["total"]
        self.stdout.write(f"Creating {total} communities...")

        if app == "anonymous_community":
            self.populate_anonymous(total)
        elif app == "users":
            self.populate_users(total)
        elif app == "posts":
            self.populate_posts(total)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} communities"))

    def populate_anonymous(self, total):
        self.stdout.write(f"Creating {total} communities...")

        for index in range(total):
            Community.objects.create(
                name=randomCommunityNameGenerator(),
                description=f"This is the description for Community {lorem.sentence()}.",
                owner_id=random.randint(1, 3),
            )
            self.stdout.write(f"Created community {index + 1}/{total}")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} communities"))
    
    def populate_users(self,total):
        self.stdout.write(f"Creating {total} users...")
        for i in range(total):
            User.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="test",
                first_name=f"User {i}",
                middle_name=f"middle {i}",
                last_name=f"Test {i}",
                phone_number=f"+123456789{i}",
            )
            self.stdout.write(f"Created user {i + 1}/{total}")
    def populate_posts(self, total):
        self.stdout.write(f"Creating {total} posts...")
        for i in range(total):
            Post.objects.create(
                author_id=random.randint(1, 3),
                title=f"Post Title {i}",
                content=f"This is the content of post {i}. {lorem.paragraph()}",
                community_id=random.randint(1, 100),
            )
            self.stdout.write(f"Created post {i + 1}/{total}")

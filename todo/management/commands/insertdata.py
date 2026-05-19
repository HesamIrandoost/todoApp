from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User
from todo.models import Task


class Command(BaseCommand):
    help = 'insert domy data'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()


    # def handle(self, *args, **options):
    #     user = User.objects.create_user(
    #         email=self.fake.email(), password="qwe123QWE@"
    #     )

    #     for _ in range(20):
    #         Task.objects.create(
    #             user=user,
    #             title=self.fake.paragraph(nb_sentences=1),
    #             description=self.fake.paragraph(nb_sentences=6),
    #         )


    def handle(self, *args, **options):
        user = User.objects.get(
            email="admin@gmail.com"
        )

        for _ in range(8):
            Task.objects.create(
                user=user,
                title=self.fake.paragraph(nb_sentences=1),
                description=self.fake.paragraph(nb_sentences=6),
                is_done=True
            )
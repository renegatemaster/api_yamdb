from csv import DictReader
from django.core.management import BaseCommand
from reviews.models import Review


db_model = Review
model_name = 'review'
file_name = 'review.csv'
filepath = 'static/data/' + file_name

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the {} data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables""".format(model_name)


class Command(BaseCommand):

    help = 'Loads data from {}'.format(file_name)

    def handle(self, *args, **options):

        if db_model.objects.exists():
            print(f'{model_name} data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print(f'Loading {model_name} data . . .')

        try:
            with open(filepath, mode="r", encoding="utf-8-sig") as csv_file:

                for row in DictReader(csv_file):
                    data = db_model(
                        # описание полей
                        id=row['id'],
                        title_id=row['title_id'],
                        text=row['text'],
                        author_id=row['author'],
                        score=row['score'],
                        pub_date=row['pub_date']
                    )
                    data.save()

            print(f'Saved {model_name} data')

        except Exception as e:
            print(e)

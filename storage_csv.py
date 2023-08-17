import csv
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, filename):
        self._filename = filename

    def add_movie(self, title, year, rating, poster_url):
        with open(self._filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, year, rating, poster_url])

    def list_movies(self):
        movies = {}
        try:
            with open(self._filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    title, year, rating, poster_url = row
                    movies[title] = {
                        'year': year,
                        'rating': float(rating),
                        'poster_url': poster_url
                    }
        except FileNotFoundError:
            pass  # Return an empty dictionary if the file doesn't exist
        return movies

    def movie_exists(self, title):
        movies = self.list_movies()
        return title in movies

    def delete_movie(self, title):
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, new_rating):
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = new_rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        with open(self._filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for title, info in movies.items():
                writer.writerow([title, info['year'], info['rating'], info['poster_url']])

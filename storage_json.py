from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.movie_list = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.movie_list, file)

    def list_movies(self):
        return self.movie_list

    def add_movie(self, title, year, rating, poster):
        if title in self.movie_list:
            return False

        self.movie_list[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }

        self._save_data()
        return True

    def delete_movie(self, title):
        if title in self.movie_list:
            del self.movie_list[title]
            self._save_data()
            return True
        return False

    def update_movie(self, title, rating):
        if title in self.movie_list:
            self.movie_list[title]["rating"] = rating
            self._save_data()
            return True
        return False

from main import generate_movie_website
from storage_json import StorageJson
import random


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def run(self):
        while True:
            print("My Movie Diary!")
            print("Please choose an option from the list below using 0-9:")
            print("0. Exit")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie Rating")
            print("5. Movie Statistics")
            print("6. Random Movie")
            print("7. Select Movie")
            print("8. Sort Movies by Rating")
            print("9. Generate Movie Website")

            command = input("Enter your choice: ")

            if command == "0":
                print("Bye!")
                break
            elif command == "1":
                self._command_list_movies()
            elif command == "2":
                self._command_add_movie()
            elif command == "3":
                self._command_delete_movie()
            elif command == "4":
                self._command_update_movie()
            elif command == "5":
                self._command_movie_stats()
            elif command == "6":
                self._command_random_movie()
            elif command == "7":
                self._command_select_movie()
            elif command == "8":
                self._command_sort_movies()
            elif command == "9":
                self._command_generate_website()
            else:
                print("Invalid command. Please try again.")

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies have been added yet.")
        else:
            print("List of movies:")
            for title, info in movies.items():
                print(f"{title} - Rating: {info['rating']} - Year: {info['year']}")

    def _command_add_movie(self):
        try:
            title = input("Enter new movie name: ")
            if self._storage.movie_exists(title):
                print(f"Movie '{title}' already exists.")
                return

            year = input("Enter the year of release: ")
            rating = float(input("Enter the rating: "))  # Validate user input
            poster_url = input("Enter the poster URL: ")

            self._storage.add_movie(title, year, rating, poster_url)
            print(f"Movie '{title}' added successfully.")
        except ValueError:
            print("Invalid input. Please enter valid data.")

    def _command_delete_movie(self):
        title = input("Enter the movie name to delete: ")
        if self._storage.movie_exists(title):
            self._storage.delete_movie(title)
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

    def _command_update_movie(self):
        title = input("Enter the movie name to update: ")
        if self._storage.movie_exists(title):
            try:
                new_rating = float(input("Enter the new rating: "))  # Validate user input
                self._storage.update_movie(title, new_rating)
                print(f"Movie '{title}' updated successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid rating.")
        else:
            print(f"Movie '{title}' not found.")

    def _command_movie_stats(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies have been added yet.")
        else:
            total_movies = len(movies)
            total_rating = sum(info['rating'] for info in movies.values())
            average_rating = total_rating / total_movies
            print(f"Total movies: {total_movies}")
            print(f"Average rating: {average_rating:.2f}")

    def _command_random_movie(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies have been added yet.")
        else:
            random_movie = random.choice(list(movies.keys()))
            print(f"Random movie: {random_movie}")

    def _command_select_movie(self):
        search_query = input("Enter a movie name to search: ")
        movies = self._storage.list_movies()
        found_movies = []

        for movie, info in movies.items():
            if search_query.lower() in movie.lower():
                found_movies.append(movie)

        if not found_movies:
            print(f"No movies found matching '{search_query}'")
        else:
            print(f"Found {len(found_movies)} movie(s) matching '{search_query}':")
            for movie in found_movies:
                print(movie)

    def _command_sort_movies(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies have been added yet.")
        else:
            sorted_movies = sorted(movies.keys(), key=lambda movie: movies[movie]['rating'], reverse=True)
            print("Movies sorted by rating:")
            for i, movie in enumerate(sorted_movies, start=1):
                print(f"{i}. {movie} - Rating: {movies[movie]['rating']}")

    def _command_generate_website(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies have been added yet. Can't generate website.")
        else:
            try:
                generate_movie_website(movies)  # Pass the movies data to the function
                print("Website was generated successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    storage = StorageJson('movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()

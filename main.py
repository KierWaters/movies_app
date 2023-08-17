import random
import json
import requests
from requests.exceptions import RequestException
from storage_json import StorageJson
from movie_app import MovieApp


def main():
    storage = StorageJson('movies.json')
    MovieApp(storage)
    movie_menu()
    movie_list = load_movie_data()  # Load movie data from storage

    while True:
        command = input("command: ")
        if command == "1":
            print_movies_list(movie_list)
        elif command == "2":
            add_movie(storage)
        elif command == "3":
            del_movie(movie_list)
        elif command == "4":
            update_movie(movie_list)
        elif command == "5":
            movie_stats(movie_list)
        elif command == "6":
            random_movie(movie_list)
        elif command == "7":
            select_movie(movie_list)
        elif command == "8":
            movies_sorted_by_rating(movie_list)
        elif command == "9":
            generate_movie_website(movie_list)
        elif command == "0":
            print("Bye!")
            save_movie_data(movie_list)  # Save movie data to storage
            break


def movie_menu():
    print("My Movie Diary!")
    print()
    print("Please choose an option from the list below using 0-9:")
    print()
    print("0. Exit")
    print("1. Movie list")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Select movie")
    print("8. Sorted by rating")
    print("9. Generate Website")
    print()


def save_movie_data(movie_list):
    with open("movies_data.json", "w") as file:
        json.dump(movie_list, file)


def load_movie_data():
    try:
        with open("movies_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def get_movies_list(storage):
    return storage.list_movies()


def print_movies_list(movies_data):
    if len(movies_data) == 0:
        print("No movies have been added to this list yet!\n")
    else:
        i = 1
        for movie, info in movies_data.items():
            rating = info["rating"]
            year_of_release = info["year"]
            print(f"{i}. {movie} - Rating: {rating} - Year: {year_of_release}")
            i += 1


def add_movie(storage):
    """ Adds a movie to the movies database """
    title = input("Enter new movie name: ")
    movie_data = storage.list_movies()

    if title in movie_data:
        print(f"Movie {title} already exists!")
        return

    url = f"http://www.omdbapi.com/?apikey=ba99a80f&t={title}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            movie_data = response.json()

            if not movie_data or "Error" in movie_data:
                print(f"No movie found with the title '{title}'")
                return

            year = movie_data.get("Year")
            rating = movie_data.get("imdbRating")
            poster_url = movie_data.get("Poster")

            if year is None or rating is None or poster_url is None:
                print(f"Incomplete movie data for '{title}'")
                return

            storage.add_movie(title, year, rating, poster_url)
            print(f"Movie {title} successfully added")
        else:
            print("Error occurred while fetching movie data from My_API")
    except RequestException:
        print("Connection error: Unable to access the API. Please check your internet connection.")


def del_movie(movie_list):
    """ Deletes a movie from the movies database """
    title = input("Enter the movie name to delete: ")
    if title not in movie_list:
        print(f"Movie {title} does not exist!")
        return

    # Delete the movie from the dictionary
    del movie_list[title]

    print(f"Movie {title} successfully deleted")


def update_movie(movie_list):
    """ Updates a movie in the movies database """
    title = input("Enter the movie name to update: ")
    if title not in movie_list:
        print(f"Movie {title} does not exist!")
        return

    new_rating = input("Enter the new rating: ")

    # Update the movie in the dictionary
    movie_list[title]["rating"] = float(new_rating)

    print(f"Movie {title} successfully updated")


def movie_stats(movies):
    """ provides the user with stats about the list of movies """
    num_movies = len(movies)

    if num_movies > 0:
        total_rating = sum(movie_info['rating'] for movie_info in movies.values())
        avg_rating = total_rating / num_movies
        max_rating = max(movie_info['rating'] for movie_info in movies.values())
        min_rating = min(movie_info['rating'] for movie_info in movies.values())
    else:
        avg_rating = 0
        max_rating = 0
        min_rating = 0

    print(f"Number of movies: {num_movies}")
    print(f"Average rating: {avg_rating:.2f}")
    print(f"Maximum rating: {max_rating}")
    print(f"Minimum rating: {min_rating}")


def random_movie(movies):
    """ Randomly selects a movie from the movie list """
    if len(movies) == 0:
        print("There are no movies in the list.")
        return

    random_choice = random.choice(list(movies.keys()))
    print(f"The random movie choice is {random_choice}")


def select_movie(movies):
    """allows the user to search for a movie on the movie list"""
    search_query = input("Enter a movie name: ")
    found_movies = []

    for movie_name, rating in movies.items():
        distance = levenshtein_distance(search_query.lower(), movie_name.lower())
        if distance <= 2:  # consider a match if distance is within 2
            found_movies.append((movie_name, rating))

    if not found_movies:
        print(f"No movies found matching '{search_query}'")
    else:
        print(f"Found {len(found_movies)} movie(s) matching '{search_query}':")
        for movie_name, rating in found_movies:
            print(f"{movie_name}, {rating}")


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# sorts the movies by rating
def movies_sorted_by_rating(movies):
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for i, (movie, info) in enumerate(sorted_movies):
        rating = info['rating']
        print(f"{i + 1}. {movie} - Rating: {rating}")


def generate_movie_website(movie_list):
    # Read the HTML template file
    with open("../_static/index_template.html", "r") as file:
        html_content = file.read()

    # Generate the movie grid
    movie_grid = ""
    for title, info in movie_list.items():
        movie_grid += f'<div class="movie">\n'
        movie_grid += f'<img class="movie-poster" src="{info["poster_url"]}"/>\n'
        movie_grid += f'<div class="movie-title">{title}</div>\n'
        movie_grid += f'<div class="movie-year">{info["year"]}</div>\n'
        movie_grid += f'</div>\n'

    # Replace the placeholder with the movie grid
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # Read the CSS file
    with open("../_static/style.css", "r") as file:
        css_content = file.read()

    # Insert the CSS content into the HTML
    html_content = html_content.replace("</head>", f"<style>{css_content}</style></head>")

    # Write the updated HTML content to the index.html file
    with open("movie_website.html", "w") as file:
        file.write(html_content)

    print("Website was generated successfully.")


if __name__ == "__main__":
    storage = StorageJson('movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()
    main()

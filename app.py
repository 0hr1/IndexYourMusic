# =====================================
# Imports
# =====================================

from flask import Flask, render_template, jsonify, request
from release import ReleaseDataSaver
import typing

# =====================================
# Classes
# =====================================

class DataSorter:
    """!
    @brief  class used to sort release data according to user requests
    """
    USER_RATING = "user-rating"
    RYM_RATING = "rym-rating"
    GENRE_SORT = "genre"
    DESCRIPTOR_SORT = "description"

    def __init__(self, release_data_path):
        with ReleaseDataSaver(release_data_path, "r") as f:
            self.release_data = f.read()

    def sort(self, sort_types: list[str], descriptors: list[str], genres: list[str]) -> list[str]:
        """!
        @param sort_types  types to sort
        @param descriptors  user requested descriptors 
        @param genres  user requested genres
        @return  releases sorted according to user requests as a list of strings "Artist - Release"
        """

        sorted_data = self.release_data.copy()

        if self.DESCRIPTOR_SORT in sort_types:
            sorted_data = self._descriptor_sort(sorted_data, descriptors)
        if self.GENRE_SORT in sort_types:
            sorted_data = self._genre_sort(sorted_data, genres)
        if self.USER_RATING in sort_types:
            sorted_data.sort(key=lambda x:x.user_rating, reverse=True)
        if self.RYM_RATING in sort_types:
            sorted_data.sort(key=lambda x:x.rym_rating, reverse=True)

        return [str(release) for release in sorted_data]

    @staticmethod
    def _descriptor_sort(release_data: list[ReleaseDataSaver], descriptors: list[str]) -> list[ReleaseDataSaver]:
        """
        @param release_data  list of releases
        @param descriptors  descriptors that should be included in returned list
        @return  list of releases in release data that contain ALL descriptors in descriptors
        """
        for descriptor in descriptors:
            release_data = [release for release in release_data if descriptor in release.descriptors]
        return release_data

    @staticmethod
    def _genre_sort(release_data, genres):
        """
        @param release_data  list of releases
        @param genres  genres that should be included in returned list
        @return  list of releases in release data that contain ALL genres in genres
        """
        for genre in genres:
            release_data = [release for release in release_data 
                            if genre in release.genres or genre in release.secondary_genres]
        return release_data
    
# =====================================
# Globals
# =====================================

app = Flask(__name__)
sorter = None

# =====================================
# Functions
# =====================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sort', methods=['POST'])
def sort_data():
    selected_options = request.json.get('sortTypes')
    description_value = request.json.get('descriptionValue')
    genre_value = request.json.get('genreValue')

    descriptors = [descriptor.strip() for descriptor in description_value.split(",")]
    genres = [genre.strip() for genre in genre_value.split(",")]
    
    sorted_data = sorter.sort(selected_options, descriptors, genres)
    return jsonify(sorted_data)

def run_app(data_path, port=5000):
    global sorter
    sorter = DataSorter(data_path)
    app.run(debug=True, host="0.0.0.0", port=port)

if __name__ == '__main__':
    run_app()

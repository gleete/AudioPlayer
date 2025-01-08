#!/usr/bin/python3

# Author: Gordon Leete

import json
from Library import Album, Song, Library

class LibraryController:
    """
    LibraryController is responsible for parsing and loading music libraries.

    This class provides methods to parse a music library from a JSON file and to load a music library from a given URL.
    """

    def parse_library(library: str) -> Library:
        """
        Parses a JSON file containing a music library and returns a Library object.

        Args:
            library (str): The file path to the JSON file containing the music library.

        Returns:
            Library: An object representing the parsed music library, containing albums and songs.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON.
        """
        with open(library, 'r') as f:
            data = json.load(f)

        albums = []
        for album in data:
            songs = []
            for song in album['songs']:
                songs.append(Song(song['name'], song['duration']))
            albums.append(Album(album['genre'], album['artist'], album['album'], songs))

        return Library(albums)

    def load_library(url: str) -> Library:
        """
        Loads a library from the given URL.

        Args:
            url (str): The URL from which to fetch the library.

        Returns:
            Library: An instance of the Library class containing the fetched data.
        """
        # TODO: Fetch library from URL through NetworkLayer abstraction
        return Library([])
#!/usr/bin/python3

# Author: Gordon Leete

from typing import List
from rich.table import Table

class Song:
    """
    A class to represent a song.

    Attributes
    ----------
    name : str
        The name of the song.
    duration : str
        The duration of the song in the format 'mm:ss'.
    """

    def __init__(self, name: str, duration: str):
        self.name = name
        self.duration = duration

class Album:
    def __init__(self, genre: str, artist: str, album: str, songs: List[Song]):
        self.genre = genre
        self.artist = artist
        self.album = album
        self.songs = songs

class Library:
    """
    Initialize the Library with a list of albums.
    Args:
        albums (List[Album]): A list of Album objects to be included in the library.

    Returns:
        Table: A rich Table object representing the music library.
    """
    def __init__(self, albums: List[Album]):
        self.albums = albums

    def to_table(self):
        table = Table(title="Music Library")
        table.add_column("Index", justify="right", style="cyan")
        table.add_column("Artist", style="magenta")
        table.add_column("Album", style="green")
        table.add_column("Genre", style="yellow")
        table.add_column("Songs", style="blue")
        
        for idx, album in enumerate(self.albums, 1):
            songs_list = "\n".join(f"  {i}. {song.name} ({song.duration})" 
                                 for i, song in enumerate(album.songs, 1))
            table.add_row(
                str(idx),
                album.artist,
                album.album,
                album.genre,
                songs_list,
            )
        
        return table
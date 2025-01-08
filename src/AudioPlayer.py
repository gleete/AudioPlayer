#!/usr/bin/python3

# Author: Gordon Leete
import argparse
from rich.console import Console
from LibraryController import LibraryController
from MusicPlayer import MusicPlayer

console = Console()


class AudioClient:

    def __init__(self, json_file: str):
        self.library = LibraryController.parse_library(json_file)
        self.player = MusicPlayer(self.library, console)

    def display_library(self):
        console.print(self.library.to_table())

    def run(self):
        """
        Runs the main loop of the audio client, handling user input and controlling playback.
        The loop continuously displays the music library and prompts the user for commands to control playback.
        Available commands include:
        - 'q': Quit the application
        - 'p': Pause or play the current song
        - 's': Stop the current song
        - 'n': Play the next song
        - 'r': Play the previous song
        - 'v': Make the player visible
        - 'b': Make the player invisible
        Users can also enter album and song numbers (e.g., '1 2' for the first album, second song) to play a specific song.
        The loop will terminate when the user enters the 'q' command.
        Raises:
            ValueError: If the user input for album and song numbers is invalid.
            IndexError: If the user input for album and song numbers is out of range.
        """
        try:
            while True:
                if not self.player.playing or not self.player.visible:
                    self.display_library()
                    console.print(
                        "\nEnter album and song numbers (e.g., '1 2' for first album, second song)"
                    )
                    console.print(
                        "Or enter a command: [P]ause/Play, [S]top, [N]ext, P[R]evious, [V]iew Playback, [Q]uit"
                    )

                    command = input("> ").strip().lower()

                    if command == "q":
                        break
                    elif command == "p":
                        self.player.pause()
                    elif command == "s":
                        self.player.stop()
                    elif command == "n":
                        self.player.next_song()
                    elif command == "r":
                        self.player.previous_song()
                    elif command == "v":
                        self.player.visible = True
                    else:
                        try:
                            album_idx, song_idx = map(
                                lambda x: int(x) - 1, command.split()
                            )
                            if 0 <= album_idx < len(self.library.albums):
                                album = self.library.albums[album_idx]
                                if 0 <= song_idx < len(album.songs):
                                    self.player.visible = True
                                    self.player.play(album, album.songs[song_idx])
                                else:
                                    console.print("Invalid song number")
                            else:
                                console.print("Invalid album number")
                        except (ValueError, IndexError):
                            console.print("Invalid input. Please try again.")
                else:
                    command = input("").strip().lower()
                    if command == "q":
                        break
                    elif command == "p":
                        self.player.pause()
                    elif command == "s":
                        self.player.stop()
                    elif command == "n":
                        self.player.next_song()
                    elif command == "b":
                        self.player.previous_song()
                    elif command == "l":
                        self.player.visible = False
        finally:
            self.player.stop()


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", type=str, required=True)

    args = parser.parse_args()
    client = AudioClient(args.library)
    client.run()


if __name__ == "__main__":
    start()

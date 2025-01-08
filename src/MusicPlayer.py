#!/usr/bin/python3

# Author: Gordon Leete
# pylint: disable=no-member
# pylint: disable=unsubscriptable-object

import time
import threading
from Library import Album, Song, Library
from typing import List, Optional
from rich.console import Console
from rich.align import Align
from rich.panel import Panel

class MusicPlayer:
    def __init__(self, library: Library, console: Console):
        self.console = console
        self.current_song: Optional[Song] = None
        self.current_album: Optional[Album] = None
        self.playing = False
        self.visible = False
        self.paused = False
        self.library = library
        self._playback_thread = None
        self.current_position = 0
        self.start_time = 0
        self.pause_time = 0

    def _duration_to_seconds(self, duration: str) -> int:
        """
        Convert a duration string in the format 'MM:SS' to total seconds.

        Args:
            duration (str): The duration string in the format 'MM:SS'.

        Returns:
            int: The total duration in seconds.
        """
        minutes, seconds = map(int, duration.split(':'))
        return minutes * 60 + seconds

    def update_playback(self):
        """
        Continuously updates the playback status of the current song.
        This method runs in a loop while the song is playing. It updates the 
        elapsed time and checks if the song has finished playing. If the song 
        has finished, it moves to the next song. It also updates the console 
        display with the current playback status, including the song name, 
        album, artist, and elapsed time.
        The method handles the following controls:
        - Pause/Play
        - Library
        - Stop
        - Next
        - Back
        - Quit
        The loop runs every second to update the playback status and console display.
        Returns:
            None
        """
        while self.playing:
            if not self.paused:
                elapsed = int(time.time() - self.start_time)
                total_seconds = self._duration_to_seconds(self.current_song.duration)
                
                if elapsed >= total_seconds:
                    self.next_song()
                    return
                
                self.current_position = elapsed

            if self.visible:
                self.console.clear()
                self.console.print(Panel(
                    Align.center(f"""
                    Now {self.playback_status()}: {self.current_song.name}
                    From: {self.current_album.album} by {self.current_album.artist}
                    Time: {self._format_duration(self.current_position)} / {self.current_song.duration}
                    
                    Controls:
                    [P]ause/Play | [L]ibrary | [S]top | [N]ext | [B]ack] | [Q]uit
                    """)
                ))
            time.sleep(1)
    
    def playback_status(self) -> str:
        """
        Returns the current playback status of the music player.
        Returns:
            str: The playback status, which can be "Stopped", "Playing", or "Paused".
        """
        if not self.playing:
            return "Stopped"
        
        if not self.paused:
            status = "Playing"
        else:
            status = "Paused"
        
        return status

    def _format_duration(self, seconds: int) -> str:
        """
        Converts a duration from seconds to a formatted string in the form of "MM:SS".

        Args:
            seconds (int): The duration in seconds.

        Returns:
            str: The formatted duration as a string in "MM:SS" format.
        """
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"

    def play(self, album: Album, song: Song):
        """
        Start playing the specified song from the given album.
        If a different song is currently playing, it will stop the current song
        and start playing the new one. Initializes playback status and starts
        a new thread to update the playback status.
        Args:
            album (Album): The album containing the song to be played.
            song (Song): The song to be played.
        Returns:
            None
        """
        # TODO: Actually start playing audio of the song
        if self.current_song != song:
            self.stop()
            self.current_song = song
            self.current_album = album
            self.playing = True
            self.paused = False
            self.current_position = 0
            self.start_time = time.time()
            
            if self._playback_thread is None or not self._playback_thread.is_alive():
                self._playback_thread = threading.Thread(target=self.update_playback)
                self._playback_thread.daemon = True
                self._playback_thread.start()

    def pause(self):
        """
        Pauses or resumes the music player.

        If the music is currently playing and not paused, this method will pause the music
        and record the current time as the pause time. If the music is currently playing and
        already paused, this method will resume the music and adjust the start time to account
        for the paused duration.

        Attributes:
            self.playing (bool): Indicates if the music is currently playing.
            self.paused (bool): Indicates if the music is currently paused.
            self.pause_time (float): The time at which the music was paused.
            self.start_time (float): The adjusted start time to account for the paused duration.
        """
        if self.playing and not self.paused:
            self.pause_time = time.time()
            self.paused = True
        elif self.playing and self.paused:
            self.start_time += time.time() - self.pause_time
            self.paused = False

    def stop(self):
        """
        Stops the currently playing music and resets the player state.

        This method stops the music if it is currently playing, resets the playing
        and paused states to False, clears the current song and album, and resets
        the current position, start time, and pause time to 0.
        """
        if self.playing:
            self.playing = False
            self.paused = False
            self.current_song = None
            self.current_album = None
            self.current_position = 0
            self.start_time = 0
            self.pause_time = 0

    def next_song(self):
        """
        Advances the music player to the next song in the current album. If the current song is the last song in the album,
        it moves to the first song of the next album in the list. If there is no current song or album, the method returns
        without doing anything.
        Returns:
            None
        """
        if not self.current_song or not self.current_album:
            return
        
        current_index = self.current_album.songs.index(self.current_song)
        if current_index < len(self.current_album.songs) - 1:
            self.play(self.current_album, self.current_album.songs[current_index + 1])
        else:
            # Move to next album
            current_album_index = self.library.albums.index(self.current_album)
            if current_album_index < len(self.library.albums) - 1:
                next_album = self.library.albums[current_album_index + 1]
                self.play(next_album, next_album.songs[0])

    def previous_song(self):
        """
        Plays the previous song in the current album. If the current song is the first song in the album,
        it moves to the last song of the previous album and plays it.
        Returns:
            None
        """
        if not self.current_song or not self.current_album:
            return
        
        current_index = self.current_album.songs.index(self.current_song)
        if current_index > 0:
            self.play(self.current_album, self.current_album.songs[current_index - 1])
        else:
            # Move to previous album
            
            current_album_index = self.library.albums.index(self.current_album)
            if current_album_index > 0:
                prev_album = self.library.albums[current_album_index - 1]
                self.play(prev_album, prev_album.songs[-1])

import os

import pygame

_SOUND_PATH = os.path.join(os.path.dirname(__file__), "can_sound.mp3")
_DEATH_SONG_PATH = os.path.join(os.path.dirname(__file__), "death_song.mp3")


def create_can_click_sound():
    """Load the can opening sound from file."""
    return pygame.mixer.Sound(_SOUND_PATH)


def create_death_song_sound():
    """Load the death screen song from file."""
    return pygame.mixer.Sound(_DEATH_SONG_PATH)

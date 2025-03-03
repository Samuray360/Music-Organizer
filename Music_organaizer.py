# The application should scan a specified directory on the user’s computer for supported music files (MP3, WAV).
# The user can view all available music files in the folder.
# Playlist Creation and Management:

# Users should be able to create new playlists by selecting songs from the available music files.
# Playlists should allow the user to add and remove songs, as well as reorder the songs within the playlist.
# Save and Load Playlists:

# The application should save playlists either in a file (e.g., .json, .txt) or use a database (e.g., SQLite) to store playlist data.
# Users should be able to load previously saved playlists and resume playlist management.

# Play Music:
# The application should allow users to play music directly from the playlist.
# Implement basic music control


import flet as ft
import os
import json

# Directory for songs and playlists
SONG_DIR = "songs"
PLAYLIST_FILE = "playlists.json"

# Load saved playlists
if os.path.exists(PLAYLIST_FILE):
    with open(PLAYLIST_FILE, "r") as f:
        playlists = json.load(f)
else:
    playlists = {}

# Function to configure the page settings
def configure_page(page: ft.Page):
    page.title = "Music Organizer"
    page.bgcolor = "00008B"
    page.window.height = 900
    page.window.width = 900
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

# Function to load songs from the songs folder
def load_songs():
    return [{"name": file, "url": os.path.join(SONG_DIR, file)} for file in os.listdir(SONG_DIR) if file.endswith(".mp3")]

# Function to handle song playback
def play_song(selected_playlist: ft.Dropdown, playlists: dict, audio: ft.Audio, current_song_index: int):
    selected_playlist_name = selected_playlist.value
    if selected_playlist_name in playlists and playlists[selected_playlist_name]:
        song = playlists[selected_playlist_name][current_song_index]  # Play song based on current index
        audio.src = song["url"]
        audio.update()
        audio.play()
    else:
        print(f"No songs found in playlist {selected_playlist_name}")

# Function to stop song playback
def stop_song(audio: ft.Audio):
    audio.pause()

# Function to create a new playlist
def create_playlist_ui(page: ft.Page, songs: list, playlists: dict, selected_playlist: ft.Dropdown):
    playlist_name = ft.TextField(label="Playlist Name", color="black")
    song_checkboxes = [ft.Checkbox(label=song["name"]) for song in songs]
    
    def save_playlist(e):
        selected_songs = [song for checkbox, song in zip(song_checkboxes, songs) if checkbox.value]
        if playlist_name.value and selected_songs:
            playlists[playlist_name.value] = selected_songs
            with open(PLAYLIST_FILE, "w") as f:
                json.dump(playlists, f)
            selected_playlist.options.append(ft.dropdown.Option(playlist_name.value))  # Update dropdown
            selected_playlist.update()
            page.snack_bar = ft.SnackBar(ft.Text(f"Playlist '{playlist_name.value}' saved!"))
            page.snack_bar.open = True
            page.update()
    
    create_button = ft.ElevatedButton("Save Playlist", on_click=save_playlist)
    playlist_window = ft.Container(content=ft.Column([playlist_name] + song_checkboxes + [create_button]), width=300, height=400, bgcolor="white")
    return playlist_window

# Function to create UI components
def create_song_player(playlists: dict, audio: ft.Audio):
    selected_playlist = ft.Dropdown(options=[ft.dropdown.Option(name) for name in playlists.keys()])
    play_btn = ft.ElevatedButton("▶ Play", on_click=lambda e: play_song(selected_playlist, playlists, audio, 0))
    stop_btn = ft.ElevatedButton("⏸ Stop", on_click=lambda e: stop_song(audio))
    next_btn = ft.ElevatedButton("Next ▶", on_click=lambda e: play_next_song(selected_playlist, playlists, audio, 1))
    previous_btn = ft.ElevatedButton("◀ Previous", on_click=lambda e: play_previous_song(selected_playlist, playlists, audio, -1))
    remove_btn = ft.ElevatedButton("Remove Song", on_click=lambda e: remove_song_from_playlist(selected_playlist, playlists))
    return selected_playlist, play_btn, stop_btn, next_btn, previous_btn, remove_btn

# Function to play the next song in the playlist
def play_next_song(selected_playlist, playlists, audio, current_song_index):
    playlist_name = selected_playlist.value
    if playlist_name in playlists:
        playlist = playlists[playlist_name]
        current_song_index += 1
        if current_song_index >= len(playlist):
            current_song_index = 0  # Loop back to the start
        song = playlist[current_song_index]
        audio.src = song["url"]
        audio.update()
        audio.play()

# Function to play the previous song in the playlist
def play_previous_song(selected_playlist, playlists, audio, current_song_index):
    playlist_name = selected_playlist.value
    if playlist_name in playlists:
        playlist = playlists[playlist_name]
        current_song_index -= 1
        if current_song_index < 0:
            current_song_index = len(playlist) - 1  # Loop to the last song
        song = playlist[current_song_index]
        audio.src = song["url"]
        audio.update()
        audio.play()

# Function to remove a song from the selected playlist
def remove_song_from_playlist(selected_playlist, playlists):
    playlist_name = selected_playlist.value
    if playlist_name in playlists:
        song_to_remove = selected_playlist.value  # Placeholder for song removal
        playlists[playlist_name] = [song for song in playlists[playlist_name] if song["name"] != song_to_remove]
        with open(PLAYLIST_FILE, "w") as f:
            json.dump(playlists, f)
        print(f"Removed song {song_to_remove} from playlist {playlist_name}")

# Function to display/hide songs in the selected playlist
def toggle_playlist_songs(selected_playlist: ft.Dropdown, playlists: dict, page: ft.Page, playlist_container: ft.Container):
    playlist_name = selected_playlist.value
    if playlist_name in playlists:
        playlist_songs = [ft.Text(song["name"]) for song in playlists[playlist_name]]
        playlist_container.content = ft.Column(controls=playlist_songs)
        playlist_container.visible = not playlist_container.visible
        page.update()

# Main function
def main(page: ft.Page):
    configure_page(page)
    songs = load_songs()
    audio = ft.Audio(autoplay=False)
    selected_playlist, play_btn, stop_btn, next_btn, previous_btn, remove_btn = create_song_player(playlists, audio)
    playlist_window = create_playlist_ui(page, songs, playlists, selected_playlist)
    playlist_container = ft.Container(visible=False)
    show_songs_btn = ft.ElevatedButton("Show/Hide Playlist Songs", on_click=lambda e: toggle_playlist_songs(selected_playlist, playlists, page, playlist_container))
    button_row = ft.Row(controls=[previous_btn, play_btn, stop_btn, next_btn, remove_btn], alignment=ft.MainAxisAlignment.CENTER)
    
    playlist_management = ft.Container(content=ft.Column([selected_playlist, show_songs_btn, playlist_window, playlist_container]))
    
    page.add( playlist_management,button_row, audio)
    page.update()

ft.app(target=main)

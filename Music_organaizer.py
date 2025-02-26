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

# Function to initialize and configure the page settings
def configure_page(page: ft.Page):
    page.title = "Music Organizer"
    page.bgcolor = "white"
    page.window.height = 600
    page.window.width = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

# Function to handle the file selection and display a snackbar
def on_file_selected(e: ft.FilePickerResultEvent, page: ft.Page):
    if e.files:
        file = e.files[0]  
        page.snack_bar = ft.SnackBar(ft.Text(f"Selected file: {file.name}"))
        page.snack_bar.open = True
        page.update()

# Function to initialize the file picker and button
def create_file_picker(page: ft.Page):
    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page))
    page.overlay.append(file_picker)
    pick_file_button = ft.ElevatedButton("Pick a file", on_click=lambda _: file_picker.pick_files())
    return pick_file_button

# Function to handle the song playing logic
def play_song(e, selected_playlist: ft.Dropdown, songs: list, audio: ft.Audio):
    selected_song = selected_playlist.value
    for song in songs:
        if song["name"] == selected_song:
            audio.src = song["url"]
            audio.play()

# Function to create the song player UI components
def create_song_player(songs: list, audio: ft.Audio):
    selected_playlist = ft.Dropdown(options=[ft.dropdown.Option(song["name"]) for song in songs])
    play_btn = ft.ElevatedButton("▶ Play", on_click=lambda e: play_song(e, selected_playlist, songs, audio))
    return selected_playlist, play_btn

# Main function to setup and run the app
def main(page: ft.Page):
    # Configure page layout and settings
    configure_page(page)
    
    # Define song list
    songs = [
        {"name": "Song 1", "url": "path_to_song_1.mp3"},
        {"name": "Song 2", "url": "path_to_song_2.mp3"}
    ]
    
    # Create audio player and file picker button
    audio = ft.Audio(autoplay=False)
    pick_file_button = create_file_picker(page)
    
    # Create the song player controls (dropdown, play button)
    selected_playlist, play_btn = create_song_player(songs, audio)
    
    # Add all components to the page
    page.add(selected_playlist, play_btn, audio, pick_file_button)

ft.app(target=main)

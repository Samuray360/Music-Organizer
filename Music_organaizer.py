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
    page.bgcolor = "00008B"
    page.window.height = 900
    page.window.width = 900
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


# Function to handle the file selection and display a snackbar
def on_file_selected(e: ft.FilePickerResultEvent, page: ft.Page, songs: list):
    if e.files:
        file = e.files[0]
        songs.append({"name": file.name, "url": file.path})  # Add song to playlist
        page.snack_bar = ft.SnackBar(ft.Text(f"Added {file.name} to playlist"))
        page.snack_bar.open = True
        page.update()


# Function to initialize the file picker and button for creating a playlist
def create_playlist(page: ft.Page, songs: list):
    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page, songs))
    page.overlay.append(file_picker)  # Adds the file picker to the page overlay
    pick_file_button = ft.ElevatedButton("Create a playlist", on_click=lambda _: file_picker.pick_files())
    return pick_file_button


# Function to handle the song playing logic
def play_song(selected_playlist: ft.Dropdown, songs: list, audio: ft.Audio):
    selected_song = selected_playlist.value 
    for song in songs:
        if song["name"] == selected_song:
            audio.src = song["url"]
            audio.play()


def stop_song(selected_playlist: ft.Dropdown, songs: list, audio: ft.Audio):
    audio.stop()


def next_song(selected_playlist: ft.Dropdown, songs: list, audio: ft.Audio):
    current_index = next((index for index, song in enumerate(songs) if song["name"] == selected_playlist.value), None)
    if current_index is not None:
        # Get next song, loop back to the first song if we're at the end
        next_index = (current_index + 1) % len(songs)
        next_song = songs[next_index]
        selected_playlist.value = next_song["name"]  # Update the dropdown to reflect the next song
        audio.src = next_song["url"]
        audio.play()


def previous_song(selected_playlist: ft.Dropdown, songs: list, audio: ft.Audio):
    current_index = next((index for index, song in enumerate(songs) if song["name"] == selected_playlist.value), None)
    if current_index is not None:
        # Get previous song, loop to the last song if we're at the beginning
        previous_index = (current_index - 1) % len(songs)
        previous_song = songs[previous_index]
        selected_playlist.value = previous_song["name"]  # Update the dropdown to reflect the previous song
        audio.src = previous_song["url"]
        audio.play()


# Function to create the song player UI components
def create_song_player(songs: list, audio: ft.Audio):
    selected_playlist = ft.Dropdown(options=[ft.dropdown.Option(song["name"]) for song in songs])
    play_btn = ft.ElevatedButton("▶", on_click=lambda e: play_song(selected_playlist, songs, audio))
    stop_btn = ft.ElevatedButton("⏸", on_click=lambda e: stop_song(selected_playlist, songs, audio))
    next_btn = ft.ElevatedButton("Next ▶", on_click=lambda e: next_song(selected_playlist, songs, audio))
    previous_btn = ft.ElevatedButton("◀ Previous", on_click=lambda e: previous_song(selected_playlist, songs, audio))
    return selected_playlist, play_btn, stop_btn, next_btn, previous_btn


# Function to create the playlist UI components (Display song names)
def create_playlist_ui(songs: list):
    playlist_items = [ft.Text(song["name"]) for song in songs]
    playlist = ft.Column(controls=playlist_items)
    return playlist


# Function to create a window for the playlist with a name field
def create_playlist_window(page: ft.Page, songs: list):
    playlist_name = ft.TextField(label="Playlist name",color="black")
    
    # Create the file picker button (and dynamically add songs to the playlist)
    pick_file_button = create_playlist(page, songs)

    # Container to hold playlist name and file picker button
    playlist_window = ft.Container(
        content=ft.Column([playlist_name, pick_file_button]),
        width=300,
        height=200,
        bgcolor="white",
        visible=False  # Initially hidden
    )
    return playlist_window


# Main function to setup and run the app
def main(page: ft.Page):
    # Configure page layout and settings
    configure_page(page)
    
    # Define song list (Empty initially)
    songs = []

    # Create audio player
    audio = ft.Audio(autoplay=False)

    # Create the song player controls (dropdown for song selection, play button)
    selected_playlist, play_btn, stop_btn, next_btn, previous_btn = create_song_player(songs, audio)

    # Create the playlist UI (Displays song names)
    playlist = create_playlist_ui(songs)
    
    # Add song control buttons in a row
    button_row = ft.Row(
        controls=[previous_btn, stop_btn, play_btn, next_btn],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Add all components to the page
    page.add(selected_playlist, button_row, audio)

    # Hardcoded songs (You can replace this with dynamically picked songs if needed)
    songs.append({"name": "Song 1", "url": "path_to_song_1.mp3"})
    songs.append({"name": "Song 2", "url": "path_to_song_2.mp3"})

    # Create playlist window (Initially hidden)
    playlist_window = create_playlist_window(page, songs)
    
    # Add the playlist window to the page
    page.add(playlist_window)
    
    # Create a button to toggle the visibility of the playlist window
    toggle_button = ft.ElevatedButton(
        "Play list creator",
        on_click=lambda e: toggle_window_visibility(playlist_window)
    )
    
    # Add the toggle button to the page
    page.add(toggle_button)

    # Update UI to reflect the new playlist
    page.update()


# Function to toggle the visibility of the playlist window
def toggle_window_visibility(playlist_window: ft.Container):
    # Toggle the visibility
    playlist_window.visible = not playlist_window.visible
    playlist_window.page.update()  # Refresh the page to apply changes

# Function to handle the file selection and add it to the playlist
def on_file_selected(e: ft.FilePickerResultEvent, page: ft.Page, songs: list):
    if e.files:
        file = e.files[0]
        songs.append({"name": file.name, "url": file.path})  # Add song to playlist
        page.snack_bar = ft.SnackBar(ft.Text(f"Added {file.name} to playlist"))
        page.snack_bar.open = True
        page.update()


# Function to initialize the file picker and button
def create_file_picker(page: ft.Page, songs: list):
    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page, songs))
    page.overlay.append(file_picker)
    pick_file_button = ft.ElevatedButton("Pick a file", on_click=lambda _: file_picker.pick_files())
    return pick_file_button


# Function to create the playlist UI components with remove functionality
def create_playlist_ui(songs: list, page: ft.Page, selected_playlist: ft.Dropdown):
    playlist_items = [ft.Text(song["name"]) for song in songs]
    playlist = ft.Column(controls=playlist_items)
   
    # Remove song functionality
    def remove_song():
        selected_song = selected_playlist.value
        songs[:] = [song for song in songs if song["name"] != selected_song]  # Remove song from playlist
        page.update()


    remove_btn = ft.ElevatedButton("Remove song", on_click=lambda e: remove_song())
    playlist.controls.append(remove_btn)  # Add the remove button to the playlist
    return playlist


ft.app(target=main)

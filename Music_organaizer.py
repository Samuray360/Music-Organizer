import flet as ft



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

def main(page: ft.Page):
    page.title = "MusicOrganaizer"
    page.bgcolor = "white"
    page.window.height = 600
    page.window.width = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER   
    



    def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file = e.files[0]  
                page.snack_bar = ft.SnackBar(ft.Text(f"Selected file: {file.name}"))
                page.snack_bar.open = True
                page.update()
        
    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    pick_file_button = ft.ElevatedButton("Pick a file", on_click=lambda _: file_picker.pick_files())




    songs = [
        {"name": "1", "url": ""},
        {"name": "2", "url": ""}
    ]

    
    audio = ft.Audio(autoplay=False)

 
    def play_song(e):
        selected_song = selected_playlist.value
        for song in songs:
            if song["name"] == selected_song:
                audio.src = song["url"]
                audio.play()

    selected_playlist = ft.Dropdown(
        options=[ft.dropdown.Option(song["name"]) for song in songs]
    )

    play_btn = ft.ElevatedButton("▶ Play", on_click=play_song)

    page.add(selected_playlist, play_btn, audio,pick_file_button)

ft.app(target=main)

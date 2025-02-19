import flet as ft

def main(page: ft.Page):
    page.title = "MusicOrganaizer"
    page.bgcolor = "white"
    page.window.height = 600
    page.window.width = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER   
    

   
    songs = [
        {"name": "1", "url": ""},
        {"name": "2", "url": ""}
    ]

    
    audio = ft.Audio(autoplay=False)

 
    def play_song(e):
        selected_song = dropdown.value
        for song in songs:
            if song["name"] == selected_song:
                audio.src = song["url"]
                audio.play()

    
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(song["name"]) for song in songs]
    )

    play_btn = ft.ElevatedButton("▶ Play", on_click=play_song)

    page.add(dropdown, play_btn, audio)

ft.app(target=main)

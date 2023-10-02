import pathlib
import pygame
from decouple import config

# Initialize Pygame
pygame.init()

# Define Pygame audio mixer settings (optional)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)


def load_config():
    music_path = config('MUSIC_PATH')
    # Add other configuration settings here
    return music_path


def main():
    music_path = load_config()
    files = pathlib.Path(music_path)

    filtered_data = list(files.rglob('*.mp3'))

    for file in filtered_data:
        file_str = str(file)

        # Extract singer and song from the filename
        clean_file = pathlib.Path(file).stem.split('.')[-1]
        singer, song = clean_file.split(' - ')

        print()
        print('*' * 69)
        print(f'Singer: {singer}\nSong: {song}')

        try:
            # Load and play the song using Pygame
            pygame.mixer.music.load(file_str)
            pygame.mixer.music.play()

            # Wait for the song to finish (optional)
            while pygame.mixer.music.get_busy():
                pygame.time.delay(1000)  # Delay in milliseconds
        except pygame.error as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
    pygame.mixer.quit()

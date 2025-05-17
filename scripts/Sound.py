import pygame

class MusicManager(object):
    def __init__(self):
        self.songs = {
            'main': 'Media/sound/Shop.wav',
            'battle': 'Media/sound/Battle.wav',
            'BattleTheme2': 'Media/sound/Shop.wav', 
            'BattleTheme3': 'Media/sound/Shop.wav',
            'BattleTheme4': 'Media/sound/Shop.wav',
            'BattleTheme5': 'Media/sound/Shop.wav',
            'BossTheme1': 'Media/sound/Shop.wav',
            'BossTheme2': 'Media/sound/Shop.wav',
            'roomSelect': 'Media/sound/Shop.wav',
            'roomRolling': 'Media/sound/Shop.wav',
            'gameOver': 'Media/sound/Shop.wav',
            'levelSelect': 'Media/sound/Shop.wav',
            'load': 'Media/sound/Shop.wav',
            'character': 'Media/sound/Shop.wav',
            'shop': 'Media/sound/Shop.wav'
        }
        self.songPlaying = None
        self.volume = 0.5
        self.loop = False
        self.songName = None

    def playTheme(self, songName, loop=False):
            if songName not in self.songs:
                print(f"Error: Song '{songName}' not found in song list.")
                return

            # Check if the requested song and loop status are already active
            if self.songName == songName and self.is_looping == loop and pygame.mixer.music.get_busy():
                print(f"Song '{songName}' is already playing with the same loop status.")
                return # Or restart if that's desired behavior for calling the same song

            try:
                # Stop currently playing music before loading a new one (load also does this)
                pygame.mixer.music.stop() 
                
                # Load the new song
                pygame.mixer.music.load(self.songs[songName])
                
                # Set loop status and play
                play_count = -1 if loop else 0 # -1 for infinite loop, 0 for play once
                pygame.mixer.music.play(loops=play_count)

             # Update state
                self.songName = songName
                self.loop = loop
                print(f"Playing '{songName}' (loop={loop})")

            except pygame.error as e:
                print(f"Error playing song '{songName}': {e}")
                self.songName = None
                self.loop = False
                

    def stop(self, songName):
        if self.songPlaying:
            self.songs[songName].stop()
            self.songPlaying = None
            self.loop = False
        
class SFXManager(object):
    def __init__(self):
        self.sfx = {
            'playerHurt': pygame.mixer.Sound('Media/sounds/playerhurt.wav'),
            'enemyHurt': pygame.mixer.Sound('Media/sounds/enemyhurt.wav'),
            'gameOver': pygame.mixer.Sound('Media/sounds/dang.wav'),
            'coinGot': pygame.mixer.Sound('Media/sounds/coingot.wav'),
            'heartGot': pygame.mixer.Sound('Media/sounds/heartGot.wav'),
            'enemyDeath': pygame.mixer.Sound('Media/sounds/enemydeath.wav'),
            'roomEnter': pygame.mixer.Sound('Media/sounds/roomenter.wav'),
            'menuClick': pygame.mixer.Sound('Media/sounds/menuclick.wav')
        }
        self.sfxPlaying = None
        self.volume = 0.5
        self.sfxName = None

    def playSFX(self, sfxName):
        if self.sfxPlaying and self.sfxPlaying != sfxName:
            self.sfxPlaying = sfxName
            self.sfx[sfxName].play()
        else:
            self.sfxPlaying = sfxName
            self.sfx[sfxName].play()
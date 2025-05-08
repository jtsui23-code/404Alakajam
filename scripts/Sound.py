import pygame

class MusicManager(object):
    def __init__(self):
        self.songs = {
            'TitleTheme': pygame.mixer.Sound('Media/sounds/title.wav'),
            'BattleTheme1': pygame.mixer.Sound('Media/sounds/battle.wav'),
            'BattleTheme2': pygame.mixer.Sound('Media/sounds/battle2.wav'),
            'BattleTheme3': pygame.mixer.Sound('Media/sounds/battle3.wav'),
            'BattleTheme4': pygame.mixer.Sound('Media/sounds/battle4.wav'),
            'BattleTheme5': pygame.mixer.Sound('Media/sounds/battle5.wav'),
            'BossTheme1': pygame.mixer.Sound('Media/sounds/boss.wav'),
            'BossTheme2': pygame.mixer.Sound('Media/sounds/boss2.wav'),
            'RoomSelectTheme': pygame.mixer.Sound('Media/sounds/roomselect.wav'),
            'ShopTheme': pygame.mixer.Sound('Media/sounds/shop.wav')
        }
        self.songPlaying = None
        self.volume = 0.5
        self.loop = False
        self.songName = None

    def playTheme(self, songName, loop=False):
        if self.songPlaying and self.songName != songName and loop == True:
            self.songPlaying = songName
            self.songs[songName].play(-1)
        elif self.songPlaying and self.songName != songName and loop == False:
            self.songPlaying = songName
            self.songs[songName].play()
        else:
            pass

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
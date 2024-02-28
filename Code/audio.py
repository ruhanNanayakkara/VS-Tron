import pyglet

# media player

class Audio(object):
    player = None
    
    music = None
    def __init__(self, file):
        self.player = pyglet.media.Player()

        self.music = pyglet.media.load(file)

    def play(self):
        self.player.queue(self.music)
        self.player.play()
import threading
import time

from synthesizer import Player, Synthesizer, Waveform

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

from dataclasses import dataclass

@dataclass
class Sound:
    volume: float
    note: str
    duration: float
    waveform: Waveform = Waveform.sine

class SoundMaster:
    player = None
    beat1 = None
    beat2 = None
    beat3 = None
    beat4 = None

    def __init__(self):
        self.player = Player()
        self.player.open_stream()

    def set_rhythm(self, beat1, beat2, beat3, beat4):
        self.beat1 = beat1
        self.beat2 = beat2
        self.beat3 = beat3
        self.beat4 = beat4

    def play_beat(self, n):
        if n == 1 and self.beat1:
            self.play_sound(self.beat1)
        elif n == 2 and self.beat2:
            self.play_sound(self.beat2)
        elif n == 3 and self.beat3:
            self.play_sound(self.beat3)
        elif n == 4 and self.beat4:
            self.play_sound(self.beat4)

    @threaded
    def play_sound(self, sound: Sound):
        synthesizer = Synthesizer(osc1_waveform=sound.waveform, osc1_volume=sound.volume, use_osc2=False)
        self.player.play_wave(synthesizer.generate_constant_wave(sound.note, sound.duration))

if __name__ == "__main__":
    sm = SoundMaster()

    sm.set_rhythm(
                Sound(1, "C4", 0.5),
                Sound(0.5, "G3", 0.5),
                Sound(1, "B3", 0.25),
                Sound(0.5, "C4", 0.5),
            )

    for i in range(5):
        for i in range(1,5):
            sm.play_beat(i)
            time.sleep(0.5)


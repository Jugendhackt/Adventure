import threading
import time
import numpy as np

from synthesizer import Player, Synthesizer, Waveform

# For debug
import sys
np.set_printoptions(threshold=sys.maxsize)



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

sounds = [
    Sound(1, "C4", 0.5),
    Sound(0.5, "G3", 0.5),
    Sound(1, "B3", 0.25),
    Sound(0.5, "C4", 0.5),
]

class SoundMaster:
    player = None
    beats: list[Sound] = [None, None, None, None]

    def __init__(self):
        self.player = Player()
        self.player.open_stream()

    beat_delta = 0.5
    collected_delta = 0.5
    current_beat = 0

    def update(self, delay: float):
        self.collected_delta += delay
        if self.collected_delta > self.beat_delta:
            self.current_beat += int(self.collected_delta/self.beat_delta)
            self.current_beat %= len(self.beats)
            self.play_beat(self.current_beat)
            self.collected_delta %= self.beat_delta


    def add_rhythm_beat(self, n):
        self.beats[n] = sounds[n]

    def set_rhythm_beat(self, n, sound):
        self.beats[n] = sound

    def play_beat(self, n):
        if n >= 0 and n <= 3 and self.beats[n]:
            self.play_sound(self.beats[n])

    @threaded
    def play_sound(self, sound: Sound):
        synthesizer = Synthesizer(osc1_waveform=sound.waveform, osc1_volume=sound.volume, use_osc2=False)
        sound_wave = synthesizer.generate_constant_wave(sound.note, sound.duration)
        envScale = np.array([float(1)]*len(sound_wave))
        startingpart = int(len(envScale)/20)
        for i in range(0,startingpart):
            envScale[i]*= float(i)/startingpart
            envScale[len(envScale)-startingpart+i]*= (startingpart-float(i))/startingpart

        sound_wave *= envScale
        print(sound_wave)
        self.player.play_wave(sound_wave)

if __name__ == "__main__":
    sm = SoundMaster()

    sm.set_rhythm_beat(0, sounds[0])
    sm.set_rhythm_beat(1, sounds[1])
    sm.set_rhythm_beat(2, sounds[2])
    sm.set_rhythm_beat(3, sounds[3])

    for t in range(5):
        for b in range(4):
            sm.play_beat(b)
            time.sleep(0.5)


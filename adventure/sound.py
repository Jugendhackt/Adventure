import threading

from synthesizer import Player, Synthesizer, Waveform

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class SoundMaster:
    def __init__(self):
        self.player = Player()
        self.player.open_stream()

    @threaded
    def play_sound(self, volume, note, dauer):
        print("beep")
        synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=volume, use_osc2=False)
        self.player.play_wave(synthesizer.generate_constant_wave(note, dauer))

if __name__ == "__main__":
    sm = SoundMaster()

    sm.play_sound(0.5, "E4", 0.5)
    sm.play_sound(0.5, "C4", 0.5)
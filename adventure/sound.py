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
    def play_sound(self):
        print("beep")
        synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
        self.player.play_wave(synthesizer.generate_constant_wave(440.0, 0.5))

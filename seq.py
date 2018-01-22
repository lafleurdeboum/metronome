
# Made this to try to have SOUND with the sequencer - doesn't work right now
# Keeps saying there's no preset 0 in bank 0 in SoundFont 1
# Whereas it used to say there's no preset found on channel 9 [bank=128 prog=0]
# when I use fluidsynth.play_Track direcly

from time import sleep
#from putch import Putch as putch
from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.containers.instrument import MidiInstrument
from mingus.core import value, chords
from mingus.midi import fluidsynth

SF2 = 'african.sf2'

class printer():
    def notify(self, msg_type, param_dict):
        #print msg_type
        print param_dict
        #putch(msg_type)
        #sleep(0.2)
        #putch('')


metronome_bar = Bar()
#metronome_bar.place_notes('D-4', value.dots(4))
metronome_bar.place_notes('D-5', 4)
metronome_bar.place_notes('D-4', 4)
metronome_bar.place_notes('D-4', 4)
metronome_bar.place_notes('D-4', 4)
# Use current_beat to check that the bar is full
if metronome_bar.current_beat != 1:
    raise SystemExit('metronome_bar is not full !')

drum = MidiInstrument()
#drum.name = "AFRICAN DRUM"
drum.name = drum.names[0]
#drum.instrument_nr = 1

metronome_track = Track(drum)

for i in range(2):
    # The mingus syntax is curious - this adds metronome_bar to metronome_track :
    metronome_track + metronome_bar

#if not fluidsynth.init(SF2):
seq = fluidsynth.FluidSynthSequencer()
seq.load_sound_font(SF2)
seq.init()
seq.start_audio_output(driver="alsa")


seq.set_instrument(1, 0)
seq.main_volume(0, 127)
a_printer = printer()
seq.attach(a_printer)

print "playing now"
seq.play_Track(metronome_track, bpm=80)
sleep(1)
print "done"


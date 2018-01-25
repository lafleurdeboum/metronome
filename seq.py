
# Made this to try to have SOUND with the sequencer - doesn't work right now
# when I use fluidsynth.play_Track direcly

from time import sleep
#from putch import Putch as putch
from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.containers.instrument import MidiInstrument
from mingus.core import value, chords
from mingus.midi import fluidsynth
from putch import Putch as putch

SF2 = 'african.sf2'


class printer():
    def notify(self, msg_type, notes_dict):
        if notes_dict.has_key('note'):
            putch(notes_dict['note'])


class player():
    def notify(self, msg_type, notes_dict):
        '''
        notes_dict is a dictionary that can have those items :
            - 'note' : 'C-4'
            - 'velocity' : 100
            - 'channel' : 1
        it could also have :
            - 'notes' : ['C-3']
            - 'channel' : 1
        '''
        if notes_dict.has_key('note'):
            if type(notes_dict['note']) == 'str':
                note = notes_dict['note']
                note.velocity = notes_dict['velocity']
                note.channel = notes_dict['channel']
                fluidsynth.play_Note(note)


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

metronome_track = Track(drum)

for i in range(2):
    # The mingus syntax is curious - this adds metronome_bar to metronome_track :
    metronome_track + metronome_bar

#if not fluidsynth.init(SF2):
seq = fluidsynth.FluidSynthSequencer()
seq.init()
seq.load_sound_font(SF2)
#seq.set_instrument(1, 1)
seq.start_audio_output(driver="alsa")
seq.main_volume(0, 127)
seq.fs.program_reset()


a_printer = printer()
a_player = player()
seq.attach(a_printer)
seq.attach(a_player)

print "playing now"
seq.play_Track(metronome_track, bpm=80)
sleep(1)
print
print "done"


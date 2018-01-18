#!/usr/bin/env python2
#-*- coding: utf-8 -*-
'''
metronome.py - play a tone at the desired rate

syntax : metronome.py [tempo]
    where tempo is expressed in bpm. In its absence metronome will play at 80bpm.
'''

from getch import getch
from sys import argv
from time import sleep, time
from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.containers.instrument import MidiInstrument
from mingus.core import value, chords
from mingus.midi import fluidsynth


SF2='african.sf2'
if len(argv) == 2:
    bpm = int(argv[1])
elif len(argv) == 1:
    bpm = 80
else:
    raise SystemExit(__doc__)



# Chords

basenote = 'C'
#basenote.channel = 0
i7 = NoteContainer(chords.I7(basenote))
iv7 = NoteContainer(chords.IV7(basenote))
v7 = NoteContainer(chords.V7(basenote))

# Bars

silence = Bar()
silence.place_rest(1)

metronome_bar = Bar()
#metronome_bar.place_notes('D-4', value.dots(4))
metronome_bar.place_notes('D-5', 4)
metronome_bar.place_notes('D-4', 4)
metronome_bar.place_notes('D-4', 4)
metronome_bar.place_notes('D-4', 4)
# Use current_beat to check that the bar is full
if metronome_bar.current_beat != 1:
    raise SystemExit('metronome_bar is not full !')
# Instruments

drum = MidiInstrument()
#drum.name = "AFRICAN DRUM"
drum.name = drum.names[0]
#drum.instrument_nr = 1

#piano = MidiInstrument()
#piano.name = piano.names[0] # Doesn't work without that. To hell with those.
#piano.instrument_nr = 0


# Tracks

metronome_track = Track(drum)
#intro_track = Track(drum)
#clave_track = Track(drum)

for i in range(10):
    metronome_track + metronome_bar

# Composition

#salsa = Composition()
#salsa.add_track(clave_track)

if not fluidsynth.init(SF2, driver='alsa'):
    raise SystemExit('Could not load ' + SF2)

fluidsynth.set_instrument(0, 0)
#fluidsynth.set_instrument(1, 1)
fluidsynth.main_volume(0, 127)
#fluidsynth.main_volume(1, 127)

# Breathe a second, toss it all
sleep(0.1)

print('press a key to start')
key = getch()
while True:
    try:
        starttime = int(time())
        while True:
            fluidsynth.play_Track(metronome_track, bpm=bpm)
    except KeyboardInterrupt:
        duration = int(time()) - starttime
        minutes = duration / 60 # integer division
        seconds = duration % 60
        sleep(0.3)
        if minutes == 0:
            msg = 'interrupted by user after ' + str(seconds) + ' seconds. '
        else:
            msg = 'interrupted by user after ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds. '
        msg += 'Press q to quit, any other key to resume.'
        print
        print(msg)
        key = getch()
        if key == 'q':
            raise SystemExit
        else:
            continue

#fluidsynth.play_Composition(salsa, channels=(0, 1))

#print('launching seq')
#seq = fluidsynth.FluidSynthSequencer()
#seq.init()
#seq.load_sound_font(SF2)
#seq.main_volume(0, 127)
#seq.main_volume(1, 127)
#seq.play_Composition(salsa)
#fluidsynth.play_Track(drum_track)



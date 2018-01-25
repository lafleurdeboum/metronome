#!/usr/bin/env python
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


default_bpm = 80
SF2='african.sf2'
instrument_bank_nr = 0


def tellduration(starttime):
    duration = int(time()) - int(starttime)
    minutes = duration / 60 # integer division - gives the lower integer in python2
    seconds = duration % 60
    sleep(0.3)
    if minutes == 0:
        msg = 'interrupted by user after ' + str(seconds) + ' seconds. '
    else:
        msg = 'interrupted by user after ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds. '
    print
    print(msg)


class metronome():
    def __init__(self):
        silence = Bar()
        silence.place_rest(1)

        metronome_bar = Bar()
        #metronome_bar.place_notes('D-4', value.dots(4))
        metronome_bar.place_notes('D-5', 4)
        metronome_bar.place_notes('D-4', 4)
        metronome_bar.place_notes('D-4', 4)
        metronome_bar.place_notes('D-4', 4)

        if metronome_bar.current_beat != 1:
            raise SystemExit('metronome_bar is not full !')

        drum = MidiInstrument()

        self.metronome_track = Track(drum)

        for i in range(10):
            # The mingus syntax is curious - this adds metronome_bar to metronome_track :
            self.metronome_track + metronome_bar

        #if not fluidsynth.init(SF2):
        if not fluidsynth.init(SF2, driver='alsa'):
            raise SystemExit('Could not load ' + SF2)

        fluidsynth.set_instrument(0, 0)
        fluidsynth.set_instrument(instrument_bank_nr, instrument_bank_nr)
        # MidiInstrument.names are purely standard tags, no incidence on instrument
        #drum.name = drum.names[instrument_bank_nr]
        fluidsynth.main_volume(0, 127)

        self.play = True
        # Breathe a (tenth of) second, toss it all
        sleep(0.1)

    def run(self, bpm):
        while self.play == True:
            fluidsynth.play_Track(self.metronome_track, bpm=bpm)
 
    def stop(self):
        self.play = False
        #fluidsynth.stop_everything()


if __name__ == '__main__':
    if len(argv) == 2:
        bpm = int(argv[1])
    elif len(argv) == 1:
        bpm = default_bpm
    else:
        raise SystemExit(__doc__)
    a_metronome = metronome()

    print('press a key to start')
    key = getch()
    while True:
        starttime = time()
        try:
            a_metronome.run(bpm)
        except KeyboardInterrupt:
            tellduration(starttime)
            print 'Press r to resume, any other key to quit.'
            key = getch()
            if key == 'r':
                continue
            else:
                a_metronome.stop()
                raise SystemExit



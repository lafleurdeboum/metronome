#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
metronome.py - play a tone at the desired rate

syntax : metronome.py [tempo]
    where tempo is expressed in bpm. In its absence metronome will play at 80bpm.
'''

from getch import getch
from putch import Putch as putch
from sys import argv
from time import sleep, time
from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.containers.instrument import MidiInstrument
from mingus.core import value, chords
from mingus.midi import fluidsynth

default_bpm = 80
SF2 = 'african.sf2'


def tellduration(starttime):
    duration = int(time()) - int(starttime)
    minutes = duration / 60 # integer division
    seconds = duration % 60
    sleep(0.3)
    if minutes == 0:
        msg = 'interrupted by user after ' + str(seconds) + ' seconds. '
    else:
        msg = 'interrupted by user after ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds. '
    print
    print(msg)


class printer():
    def notify(self, msg_type, param_dict):
        #print msg_type
        #print param_dict
        putch(msg_type)
        sleep(1)
        putch('')


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
        # Use current_beat to check that the bar is full
        if metronome_bar.current_beat != 1:
            raise SystemExit('metronome_bar is not full !')

        drum = MidiInstrument()
        #drum.name = "AFRICAN DRUM"
        drum.name = drum.names[0]
        #drum.instrument_nr = 1

        self.metronome_track = Track(drum)

        for i in range(10):
            # The mingus syntax is curious - this adds metronome_bar to metronome_track :
            self.metronome_track + metronome_bar

        #if not fluidsynth.init(SF2):
        self.seq = fluidsynth.FluidSynthSequencer()
        self.seq.load_sound_font(SF2)
        self.seq.start_audio_output(driver="alsa")

        self.seq.set_instrument(0, 0)
        self.seq.main_volume(0, 127)
        self.seq.init()
        self.printer = printer()
        self.seq.attach(self.printer)

        self.play = True
        # Breathe a (tenth of) second, toss it all
        sleep(0.1)

    def run(self, bpm):
        while self.play == True:
            self.seq.play_Track(self.metronome_track, bpm=bpm)
 
    def stop(self):
        self.play = False
        #seq.stop_everything()


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
            print 'Press q to quit, any other key to resume.'
            key = getch()
            if key == 'q':
                a_metronome.stop()
                raise SystemExit
            else:
                continue


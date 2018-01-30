#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
metronome.py - play a tone at the desired rate

syntax : metronome.py [tempo]
    where tempo is expressed in bpm. In its absence metronome will play at 80bpm.
'''

from putch import Putch as putch
from getch import getch
from sys import argv
from time import sleep, time
from mingus.containers import Note, NoteContainer, Bar, Track, Composition
from mingus.containers.instrument import MidiInstrument
from mingus.core import value, chords
from mingus.midi import fluidsynth
from threading import Thread


default_bpm = 80
SF2='african.sf2'
instrument_bank_nr = 0


def tellduration(starttime):
    duration = int(time()) - int(starttime)
    minutes = duration / 60 # integer division - gives the lower integer in python2
    seconds = duration % 60
    sleep(0.3)
    if minutes == 0:
        print 'interrupted by user after ' + str(seconds) + ' seconds.'
    else:
        print 'interrupted by user after ' + str(minutes) + ' minutes ' + str(seconds) + ' seconds.'


class Printer():
    def notify(self, msg_type, notes_dict):
        #if notes_dict.has_key('note'):
        if msg_type == 5:
            putch(notes_dict['note'])


class Player():
    def notify(self, msg_type, notes_dict):
        '''
        if msg_type is 5, notes_dict is a dictionary that can have those items :
            - 'note' : 'C-4'
            - 'velocity' : 100
            - 'channel' : 1
        '''
        #if notes_dict.has_key('note'):
        #    if isinstance(notes_dict['note'], str):
        if msg_type == 5:
            note = notes_dict['note']
            note.velocity = notes_dict['velocity']
            note.channel = notes_dict['channel']
            fluidsynth.play_Note(note)


class Metronome(Thread):
    def attach_notifier(self):
        printer = Printer()
        self.sequencer.attach(printer)

    def attach_player(self):
        player = Player()
        self.sequencer.attach(player)

    def __init__(self, bpm=80):
        super(Metronome, self).__init__()
        self.tempo = bpm
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

        for i in range(1):
            # The mingus syntax is curious - this adds metronome_bar to metronome_track :
            self.metronome_track + metronome_bar

        #if not fluidsynth.init(SF2):
        self.sequencer = fluidsynth.FluidSynthSequencer()
        self.sequencer.init()
        self.sequencer.load_sound_font(SF2)
        self.sequencer.start_audio_output(driver="alsa")

        self.sequencer.set_instrument(0, 0)
        self.sequencer.main_volume(0, 127)
        self.sequencer.fs.program_reset()
        #self.attach_notifier()
        self.attach_player()

    def run(self):
        self.starttime = time()
        self.running = True
        while self.running:
            # when we run stop, del(self.sequencer can occur after we get in the loop
            if hasattr(self, 'sequencer'): 
                self.sequencer.play_Track(self.metronome_track, bpm=self.tempo)
 
    def stop(self):
        if hasattr(self, 'starttime'):
            tellduration(self.starttime)
        self.running = False
        del(self.sequencer)
        #fluidsynth.stop_everything()


if __name__ == '__main__':
    if len(argv) == 2:
        bpm = int(argv[1])
    elif len(argv) == 1:
        bpm = default_bpm
    else:
        raise SystemExit(__doc__)

    while True:
        print 'Starting metronome. Press q to quit, any other key to pause.'
        a_metronome = Metronome()
        a_metronome.tempo = bpm
        a_metronome.start()
        key = getch()
        a_metronome.stop()
        del(a_metronome)
        if key == 'q':
            raise SystemExit()
        key = getch()
        if key == 'q':
            raise SystemExit()


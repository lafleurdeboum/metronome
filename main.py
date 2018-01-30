#!/usr/bin/env python
#-*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
from metronome import Metronome
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.event import EventDispatcher
from time import time

class Metrosignal(EventDispatcher):
    #buzz_label = StringProperty('off')
    def __init__(self):
        self.register_event_type('on_buzz')
        super(Metrosignal, self).__init__()

    def notify(self, msg_type, note_dict):
        if msg_type == 5:
            self.dispatch('on_buzz', (note_dict['note'], 'on'))
        if msg_type == 6:
            self.dispatch('on_buzz', (note_dict['note'], 'off'))

    def on_buzz(self, args):
        pass


class MetronomeGUI(BoxLayout):
    '''
    main widget defined in metronome.kv
    '''
    tempo_label = StringProperty(None)

    def __init__(self):
        self.launchtime = time()
        super(MetronomeGUI, self).__init__()
        self.metronome = Metronome()
        self.buzzer = Metrosignal()
        #self.buzzer.setDaemon(True)
        self.metronome.sequencer.attach(self.buzzer)
        self.buzzer.bind(on_buzz=self.lightbuzz)

    def lightbuzz(self, dispatcher, signal):
        print 'I was called with signal', signal, 'at date', time() - self.launchtime

    def set_tempo(self, tempo):
        print 'setting tempo to', tempo
        self.metronome.tempo = tempo
        self.ids.tempo_label.text = str(tempo)

    def set_tempo_label(self, object, tempo):
        self.ids.tempo_label.text = str(tempo)

    def switch_metronome(self):
        if self.ids.metronome_switch.active is True:
            print 'launching metronome'
            self.metronome.start()
        else:
            print 'stopping metronome'
            self.metronome.stop()
            del(self.metronome)
            self.__init__()


class MetronomeApp(App):
    '''
    links to metronome.kv
    '''
    def on_stop(self):
        print 'quitting'
        if hasattr(self.root, 'metronome'):
            self.root.metronome.stop()


if __name__ == '__main__':
    app = MetronomeApp()
    app.run()

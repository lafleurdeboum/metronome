# metronome.py

A light program that uses python, python-mingus and fluidsynth to reproduce a tone at any regular rate

## Installation

You will need `python`, `python-mingus` and `fluidsynth` to use this script. `python-mingus` is a wonderful python module dedicated to music ; if it isn't in your distribution's repo you can install it with
  `pip install mingus`

Then just download and run the script. Oh you will also need `getch.py`, `switch.py` and a soundfont file, called `african.sf2`, living in the same dir as the script. Courtesy of Thomas Hammer at hammersound : http://hammersound.net/hs_soundfonts.html . I must say that allthough his website does mention a copyright at the bottom of it, I was unable to locate any license involved in this copyright. The site just mentions that one _can_ download and use the soundfonts. TBC ...

## Usage

The syntax is :

  `python metronome.py [tempo]`

where tempo is an optional integer expressed in beats per minute (bpm). If it is ommited, the tempo will be 80. The script will run forever ; to quit press `q` ; to interrupt press any other key. Press a key again to resume.

Note that this script was written for python2. If you have other python versions installed, you should rather use :

  `python2 metronome.py [tempo]`

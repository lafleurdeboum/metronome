# metronome.py

A script that uses python, python-mingus and fluidsynth to reproduce a tone at any regular rate

## Installation

You will need `python`, `python-mingus` and `fluidsynth` to use this script. `python-mingus` is a wonderful python module dedicated to music ; if it isn't in your distribution's repo you can install it with
  `pip install mingus`

Then just download and run the script. Oh you will also need a soundfont file, called african.sf2, living in the same dir as the script. Courtesy of Thomas at hammersound : http://hammersound.net/hs_soundfonts.html .

## Usage

The syntax is :

  `metronome.py [tempo]`

where tempo is an optional integer expressed in beats per minute (bpm). If it is ommited, the tempo will be 80.

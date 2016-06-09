#! /usr/bin/python3

from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
import time
from getch import getch
from threading import Timer

handle = fluidhandle.FluidHandle()
settings = fluidsettings.FluidSettings(handle)
settings['synth.gain'] = 0.2
synth = fluidsynth.FluidSynth(handle, settings)
synth.load_soundfont('/usr/share/sounds/sf2/FluidR3_GM.sf2')

settings['audio.driver'] = 'alsa'
driver = fluidaudiodriver.FluidAudioDriver(handle, synth, settings)

c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
c_major_scale_intervals = dict(zip(c_major_scale, major_scale_intervals))

def abc2midi_note_number(abc_note_string):
    """"Convert an ABC note to a midi number"""
    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note_string.islower():
        midi_note_number += 12
        abc_note_string = abc_note_string.upper()
    midi_note_number += c_major_scale_intervals[abc_note_string]
    return midi_note_number

def demo_play_single_note():
    synth.noteon(0, 79, 1.0)
    time.sleep(1)
    synth.noteoff(0, 79)

def demo_play_scale():
    for note in c_major_scale + list(map(str.lower, c_major_scale)):
        midi_note_number = abc2midi_note_number(note)
        synth.noteon(0, midi_note_number, 1.0)
        time.sleep(0.5)
        synth.noteoff(0, midi_note_number)

def demo_play_interactive():
    print('Press a key for an ABC note from C to b... (Ctrl+C to finish)')
    two_octaves_c_major_scale = c_major_scale + list(map(str.lower, c_major_scale))
    while True:
        key = getch()
        if key is '\x03': # Ctrl+C
            break
        if key in two_octaves_c_major_scale:
            midi_note_number = abc2midi_note_number(key)
            synth.noteon(0, midi_note_number, 1.0)
            time.sleep(0.5)
            synth.noteoff(0, midi_note_number)
    # Limite de cette approche:
    #       il faut attendre la fin d'une note pour pouvoir en jouer une autre
    #       effet secondaire quand ça arrive: la note est affichée dans le terminal et pas traitée par getch()


# Version 2 de demo_play_interactive(): utilisation de timers
# Q: est-ce que libfluidsynth est réentrant? et pyfluidsynth3?

current_midi_note_number = None
current_midi_channel = 0
current_timer = None

def on_timeout():
    global current_midi_note_number
    global current_midi_channel

    # TODO: begin critical section
    # (sécuriser la sortie de section critique)
    synth.noteoff(current_midi_channel, current_midi_note_number)

    # TODO current_midi_note_number = None (after crit)

    # TODO: end critical section

def play_note(channel, note_number, velocity, delay_s):
    global current_midi_note_number
    global current_midi_channel
    global current_timer

    # TODO: begin critical section

    if current_midi_note_number is not None:
        synth.noteoff(current_midi_channel, current_midi_note_number)
        current_timer.cancel()

    current_midi_channel = channel
    current_midi_note_number = note_number
    synth.noteon(current_midi_channel, current_midi_note_number, velocity)
    current_timer = Timer(delay_s, on_timeout)
    current_timer.start()

    # TODO: end critical section

def demo_play_interactive_timer():
    print('Press a key for an ABC note from C to b... (Ctrl+C to finish)')
    two_octaves_c_major_scale = c_major_scale + list(map(str.lower, c_major_scale))
    while True:
        key = getch()
        if key is '\x03': # Ctrl+C
            break
        if key in two_octaves_c_major_scale:
            midi_note_number = abc2midi_note_number(key)
            play_note(0, midi_note_number, 1.0, 0.5)


demo_play_interactive_timer()
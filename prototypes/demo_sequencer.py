from pyfluidsynth3 import fluidaudiodriver, fluidevent, fluidhandle, fluidsettings, fluidsequencer, fluidsynth
from pyfluidsynth3.fluiderror import FluidError

import sys
import time
import traceback

''' Based on the examples from pyfluidsynth by MostAwesomeDude. '''
''' Based on sequencer.py from tea2code'''

soundfonts = [  # We will use the first sound font that can be found in that list:
    '/usr/share/sounds/sf2/FluidR3_GM.sf2',
    '/usr/share/sounds/sf2/default.sf2'  # Fedora: symlink to '/usr/share/soundfonts/FluidR3_GM.sf2'
]

try:
    HANDLE = fluidhandle.FluidHandle()
    settings = fluidsettings.FluidSettings(HANDLE)
    settings['synth.gain'] = 0.2
    SYNTH = fluidsynth.FluidSynth(HANDLE, settings)
    #load_soundfont()
    settings['audio.driver'] = 'alsa'
    driver = fluidaudiodriver.FluidAudioDriver(HANDLE, SYNTH, settings)
except FluidError as e:
    message = 'Failed to setup fluidsynth: ' + str(
        e) + '. Audio output will be disabled.'
    print(message)
    print(traceback.format_exc())
    sys.exit(1)

#if len( sys.argv ) < 3:
#    print( "Usage: {0} library soundfont.sf2".format(sys.argv[0]) )
#    sys.exit()


#handle = fluidhandle.FluidHandle( sys.argv[1] )
#settings = fluidsettings.FluidSettings( handle )
#synth = fluidsynth.FluidSynth( handle, settings )
#driver = fluidaudiodriver.FluidAudioDriver( handle, synth, settings )

SEQUENCER = fluidsequencer.FluidSequencer(HANDLE)

SYNTH.load_soundfont(soundfonts[0])

SEQUENCER.beats_per_minute = 90
beat_length = SEQUENCER.ticks_per_beat

print( "BPM: {0}".format(SEQUENCER.beats_per_minute))
print( "TPB: {0}".format(SEQUENCER.ticks_per_beat))
print( "TPS: {0}".format(SEQUENCER.ticks_per_second))

dest = SEQUENCER.add_synth(SYNTH)

c_scale = []

for note in range( 60, 72 ):
    event = fluidevent.FluidEvent(HANDLE)
    event.dest = dest[0]
    event.note( 0, note, 127, int(beat_length * 0.9) )
    c_scale.append( event )

ticks = SEQUENCER.ticks + 10

SEQUENCER.send(c_scale[0], ticks)
SEQUENCER.send(c_scale[4], ticks)
SEQUENCER.send(c_scale[7], ticks)

ticks += beat_length

SEQUENCER.send(c_scale[0], ticks)
SEQUENCER.send(c_scale[5], ticks)
SEQUENCER.send(c_scale[9], ticks)

ticks += beat_length

SEQUENCER.send(c_scale[0], ticks)
SEQUENCER.send(c_scale[4], ticks)
SEQUENCER.send(c_scale[7], ticks)

ticks += beat_length

SEQUENCER.send(c_scale[2], ticks)
SEQUENCER.send(c_scale[5], ticks)
SEQUENCER.send(c_scale[7], ticks)
SEQUENCER.send(c_scale[11], ticks)

ticks += beat_length

SEQUENCER.send(c_scale[0], ticks)
SEQUENCER.send(c_scale[4], ticks)
SEQUENCER.send(c_scale[7], ticks)

time.sleep( 16 )

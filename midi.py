# pip install python-rtmidi
# pip install mido
import rtmidi
import mido
import time

print("Midi output ports: ", mido.get_output_names())
midiOutput = mido.open_output("IAC Driver Bus 1")

def sendControlChange(control):
    message = mido.Message('control_change', control=control)
    midiOutput.send(message)


# sendControlChange(n) -> wenn der farbige Stift in Zone n ist
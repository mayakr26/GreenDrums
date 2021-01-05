# pip install python-rtmidi
# pip install mido
import mido

print("Midi output ports: ", mido.get_output_names())
midiOutput = mido.open_output("IAC-Treiber Bus 1")


def send_control_change(control):
    midiOutput.send(mido.Message('note_on', note=control, velocity=127))

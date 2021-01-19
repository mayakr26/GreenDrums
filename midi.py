# pip install python-rtmidi
# pip install mido
import mido
import platform

# print("Midi output ports: ", mido.get_output_names())

# MacOS und Windows haben unterschiedliche Midi-Synthesizer,
# die anders angesprochen werden.
# https://docs.python.org/3/library/platform.html

# Windows
if (platform.system() == "Windows"):
    midiOutput = mido.open_output("LoopBe Internal MIDI 1")

# MacOS
if (platform.system() == "Darwin"):
    midiOutput = mido.open_output("IAC-Treiber Bus 1")


def send_control_change(control):
    midiOutput.send(mido.Message('note_on', note=control, velocity=127))

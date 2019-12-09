import mido
from mido import Message
# import gpio
import os
import subprocess


def temperature_note_test():
    """
    Returns a midi note based on the decimal point of the temperature
    """
    # A hacky way of doing this, but eh.
    temp_str = subprocess.run(['/opt/vc/bin/vcgencmd', 'measure_temp'],
            stdout=subprocess.PIPE, text=True).stdout
    temp_decimal = temp_str.split('.')[1][0]
    return int(temp_decimal)


if __name__ == "__main__":
    
    sensor_list = [
            temperature_note_test
            ]  # A list of functions that return a value in sensor_list

    # We'll need to store channel state. Initialising to nonsense.
    frozen_msg = mido.Message('note_off')
    last_msgs_sent = [frozen_msg]*len(sensor_list)
    
    # Set up Midi outputs
    out = mido.open_output('UM-ONE:UM-ONE MIDI 1 20:0')

    # Now and forever more, do things.
    while 1==1:
        # Poll sensors
        for channel, sensor in enumerate(sensor_list):
            reading = sensor()
            
            print("Sensor {} reading = {}".format(sensor, reading))

            # Kill last note (for now, we're assuming that we only control note with sensor)
            print("Note off on channel {}".format(channel))
            last_note = last_msgs_sent[channel].note
            msg = Message('note_off', note = last_note, channel=channel)
            out.send(msg)
            
            # If reading is > some threshold (0 for now)
            if reading != 0:
                print("Note {} on channel {}".format(reading, channel))
                msg = Message('note_on', note=reading, channel=channel)
                out.send(msg)
            last_msgs_sent[channel] = msg

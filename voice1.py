import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np

FRAMES_PER_BUFFER=3200
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=16000

pa=pyaudio.PyAudio()

stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

print('start recording')

seconds=8
frames=[]
second_tracking=0
second_count=0
for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)
    second_tracking+=1
    if second_tracking == RATE/FRAMES_PER_BUFFER:
        second_count +=1
        second_tracking=0
        print(f'time left: {seconds-second_count}')

stream.stop_stream()
stream.close()
pa.terminate()

obj=wave.open('voice_msg1.wav','wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(pa.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b''.join(frames))
obj.close()

file=wave.open('voice_msg1.wav','rb')

sample_freq=file.getframerate()
frames=file.getnframes()
signal_wave=file.readframes(-1)

file.close()

time=frames/sample_freq

audio_arrav=np.frombuffer(signal_wave,dtype=np.int16)
times=np.linspace(0,time,num=frames)

plt.figure(figsize=(12,5))
plt.plot(times,audio_arrav)
plt.ylabel('Signal wave')
plt.xlabel('Times(s)')
plt.xlim(0,time)
plt.title('audio recording ')
plt.show()
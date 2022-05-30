# -*- coding: utf-8 -*-
import time
from six.moves import queue
import pyaudio

STREAMING_LIMIT = 10000

def get_current_time():
    """Return Current Time in MS."""

    return int(round(time.time() * 1000))

# function added
def duration_to_secs(duration):
    return duration.seconds + (duration.nanos /float(1e9))


""" Opens a recording stream as a generator yielding the audio chuncks."""
class ResumableMicrophoneStream:


    def __init__(self, rate, chunk_size):
        
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
    
        
        self._bytes_per_sample = 2 * self._num_channels
        self._bytes_per_second = self._rate * self._bytes_per_sample

        self._bytes_per_chunk = (self.chunk_size * self._bytes_per_sample)
        self._chunks_per_second = (self._bytes_per_second // self._bytes_per_chunk)
        
    
    def __enter__(self):

        self.closed = False
        
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )
        
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""

        while not self.closed:
            if get_current_time() - self.start_time > STREAMING_LIMIT:
                self.start_time = get_current_time()
                break
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.

            #comment this section so the api won't auto stop when bad connexion or nothing is provided 
            
            chunk = self._buff.get()

            if chunk is None:
                return

            
            data = []
            data.append(chunk)

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    
                    if chunk is None:
                        return
                    
                    data.append(chunk)
                    

                except queue.Empty:
                    break

            yield b"".join(data)
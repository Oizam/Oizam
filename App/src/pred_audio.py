import librosa
import librosa.display
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from PIL import Image

# On n'affiche pas les warnings de librosa dû au chargement de fichiers mp3
import warnings
warnings.filterwarnings("ignore", message="PySoundFile failed. Trying audioread instead.")

class AudioUtil():
  @staticmethod
  def load_audio(audio_completepath):
    samples, sample_rate = librosa.load(audio_completepath, sr=22050, mono=True)
    return (samples, sample_rate)

  @staticmethod
  def rechannel(audio, new_channel):
    samples, sample_rate = audio

    if new_channel not in [1, 2, 3]:
      raise Exception("Le nombre de channels doit être 1 ou 2 ou 3.")

    if (samples.shape[0] == new_channel):
      # Nothing to do
      return audio

    if (samples.shape[0] > 3) & (new_channel == 1):
      return audio

    if (samples.shape[0] > 3) & (new_channel != 1):
      if new_channel == 2:
        resamples = np.stack((samples, samples),axis=0)
      elif new_channel == 3:
        resamples = np.stack((samples, samples, samples),axis=0)
      return ((resamples, sample_rate))

    if (new_channel == 1):
      # Convert to mono by selecting only the first channel
      resamples = np.squeeze(samples[:1, :])
    elif (new_channel == 2):
      # Convert to stereo by duplicating the first channel
      samples = np.squeeze(samples[:1, :])
      resamples = np.stack((samples, samples),axis=0)
    else:
      # Convert to 3 channels by duplicating the first channel
      samples = np.squeeze(samples[:1, :])
      resamples = np.stack((samples, samples, samples),axis=0)     

    return ((resamples, sample_rate))

  @staticmethod
  def resample(audio, newsample_rate):
    samples, sample_rate = audio

    if (sample_rate == newsample_rate):
      # Nothing to do
      return audio

    resamples = librosa.resample(samples, sample_rate, newsample_rate)

    return ((resamples, newsample_rate))

  @staticmethod
  def padding_trunc_audio(audio, newduration):

    samples, sample_rate = audio
    if samples.shape[0] <= 3:
      num_channels, samples_len = samples.shape
    else:
      num_channels = 1
      samples_len = samples.shape[0]
    
    audio_duration = samples_len/sample_rate
    samples_newlen = round(newduration*sample_rate)

    if (samples_len > samples_newlen):
      # Truncate the signal to the given length
      if num_channels != 1:
        samples = samples[:,:samples_newlen]
      else:
        samples = samples[:samples_newlen]
    
    if (samples_len < samples_newlen):
      padding_len = samples_newlen - samples_len
      if num_channels != 1:
        padding = np.zeros((num_channels,padding_len))
        samples = np.concatenate([samples,padding],axis=1)
      else:
        padding = np.zeros((padding_len))
        samples = np.concatenate([samples,padding],axis=0)
      
    return ((samples, sample_rate))

  @staticmethod
  def audio_to_melspec(audio, n_mels=64, n_fft=2048, win_len=None, hop_len=None):

    samples, sample_rate = audio

    # sgram = librosa.stft(samples)
    # spec has shape [channel, n_mels, time], where channel is mono, stereo etc
    if samples.shape[0] <= 3:
      num_channels = samples.shape[0]
      spec = librosa.feature.melspectrogram(y=samples[0,:], n_fft=n_fft, win_length=win_len, hop_length=hop_len, n_mels=n_mels, fmax=sample_rate/2)
    else:
      num_channels = 1
      spec = librosa.feature.melspectrogram(y=samples, n_fft=n_fft, win_length=win_len, hop_length=hop_len, n_mels=n_mels, fmax=sample_rate/2)
      spec = np.expand_dims(spec,axis=2)
    
    if num_channels == 2:
      spec = np.stack([spec,spec],axis=2)
    elif num_channels == 3:
      spec = np.stack([spec,spec,spec],axis=2)
    # Convert to decibels
    spec = librosa.amplitude_to_db(spec, ref=np.min)
    return (spec)

  @staticmethod
  def plot_melspec(spec, sample_rate=44100, figsize=(14,5)):
    plt.figure(figsize=figsize)
    librosa.display.specshow(spec, sr=sample_rate, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')


def create_class_path_dataframe(classfilepath):
    classfilepath = classfilepath.replace(os.sep, '/')
    if classfilepath[-1] == "/":
        classfilepath = classfilepath[:-1]
    df_class_paths = pd.read_csv(classfilepath + '/' + 'classes_path.txt', header=None)
    return df_class_paths.rename(columns={0: 'SongID', 1: 'RelativePath', 2: 'ClassID'})

def wav_to_sgram(src_wav, num_channels=3, duration=10, newsample_rate=22050):

    audio_file = src_wav

    audio = AudioUtil.load_audio(audio_file)
    reaudio = AudioUtil.resample(audio, newsample_rate = newsample_rate)
    rechan = AudioUtil.rechannel(reaudio, num_channels)

    duration_audio = AudioUtil.padding_trunc_audio(rechan, duration)
    sgram = AudioUtil.audio_to_melspec(duration_audio, n_mels=300, n_fft=1024, win_len=1024, hop_len=512)
    sgram = np.rint(sgram).astype(np.uint8)

    return sgram

def save_sgram_to_image(sgram, dst_sgram):
    sgram_im = Image.fromarray(sgram)
    sgram_im = sgram_im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    sgram_im.save(dst_sgram)
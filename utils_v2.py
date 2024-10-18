import mne
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import pandas as pd
from scipy import signal

# Chemin du répertoire contenant les fichiers PSG et leurs annotations
directory_path = "./sleep-edf-database-expanded-1.0.0/sleep-cassette/"

# Utilisation de la méthode glob pour obtenir les chemins des fichiers PSG et d'annotations
PSG_files = glob.glob(os.path.join(directory_path, "*-PSG.edf"))
Hypno_files = glob.glob(os.path.join(directory_path, "*-Hypnogram.edf"))

ann2label = {
"Sleep stage W": 0,
"Sleep stage 1": 1,
"Sleep stage 2": 2,
"Sleep stage 3": 3,
"Sleep stage 4": 3,
"Sleep stage R": 4,
"Sleep stage ?": 5,
"Movement time": 5
}

# Définir le filtre Butterworth
nyquist = 0.5 * 100  # Fréquence de Nyquist, la moitié de la fréquence d'échantillonnage
low = 0.5 / nyquist
high = 35 / nyquist
b, a = signal.butter(4, [low, high], btype='band')


# Separating data into 30s epochs
epoch_duration = 30 

# Créer une liste pour stocker les dataframes de chaque PSG
all_dfs = [] 
 
# Boucle pour traiter chaque paire de fichiers PSG et d'annotations
for i in range(20):#(len(PSG_files)):
    PSG_path = PSG_files[i]
    Hypno_path = Hypno_files[i]

    # Reading files
    sleep_recording = mne.io.read_raw_edf(PSG_path)
    annotations = mne.read_annotations(Hypno_path)

    channel_name = ['EEG Pz-Oz']#['EEG Fpz-Cz']
    sleep_recording.pick(channel_name)
    shape = sleep_recording.get_data().shape

    epochs = []
    labels = []
    # Segmenter les données en époques de 30 secondes et affecter les labels correspondants
    for j in range(int(sleep_recording.n_times) // (epoch_duration * int(sleep_recording.info['sfreq']))):
        start_sec = j * epoch_duration
        data, times = sleep_recording[:,start_sec * sleep_recording.info['sfreq']:(start_sec + epoch_duration) * sleep_recording.info['sfreq']]
        data = data.flatten()

        # Appliquer le filtre passe-bande
        filtered_data = signal.filtfilt(b, a, data)
        epochs.append(filtered_data)

        for ann in annotations:
            if start_sec >= ann['onset'] and start_sec < ann['onset'] + ann['duration']:
                label = ann2label[ann['description']]
                break

        labels.append(label)

    # Convertir la liste en un tableau 2D
    all_data_array = np.array(epochs)
    all_labels_array = np.array(labels).reshape(-1, 1)

    # Normalisation so each epochs has zero mean and unit variance
    # Substracting each sampled point by sequence mean value and dividing this result by standard deviation calculated on whole sequence
    mean = np.expand_dims(all_data_array.mean(axis=1), axis=1)
    standard_deviation = np.expand_dims(all_data_array.std(axis=1), axis=1)
    normalized_data = (all_data_array - mean) / standard_deviation

    # Déballer les tableaux 2D et créer un DataFrame
    df = pd.DataFrame(np.concatenate([normalized_data, all_labels_array], axis=1), 
                      columns= [f'feature_{i+1}' for i in range(normalized_data.shape[1])] + ['label'])

    all_dfs.append(df)
    print(f'done for psg number {i+1}')



# Concaténer tous les DataFrames dans un seul DataFrame
final_df = pd.concat(all_dfs, ignore_index=False)

# Afficher le DataFrame
print(final_df.tail(1))

# Sauvegarder la DataFrame dans un fichier CSV 
final_df.to_csv('./dataframe_PremierPas_HP_PzOz_Normalized_20PSG.csv', index=False)

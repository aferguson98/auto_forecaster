from datetime import datetime
import os
import sys

from joblib import Parallel, delayed
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.callbacks import ModelCheckpoint, EarlyStopping

import auto_forecaster.core
from auto_forecaster.core import regions


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


regions = regions.get_regions_with_tokeniser()


"""def loss_function(y_true, y_pred):
    ""
    A custom loss function for the model
        * 60% of the score is the number of words that are incorrect
        * 40% of the score is the number of words in the incorrect order

    ""
    y_true_np = y_true
    y_pred_np = y_pred
    scores = []

    for i in range(len(y_true_np)):
        this_y_true = list(y_true_np[i])
        this_y_pred = list(y_pred_np[i])
        score = 0
        scores_j = []
        for j in range(len(this_y_true)):
            if this_y_true[j] != this_y_pred[j]:
                score += 0.4
                diff = abs(this_y_true.count(this_y_true[j]) -
                           this_y_pred.count(this_y_pred[j]))
                score += (0.6 * diff)
            tf.multiply(y_true[])
        scores.append(scores_j)
    scored = tf.multiply(y_true, scores)
    print(tf.reduce_mean(scored, axis=-1))
    tf.reduce_mean(scored, axis=-1)
    return tf.reduce_mean(scored, axis=-1)"""


def parallel_processing(region_idx):
    regions[region_idx].process_data()


def start_process(load_data=True, model_type="cnn"):
    """

    Parameters
    ----------
    load_data: bool
        Whether to load data or use the numpy save file
        * false - load data from numpy save file
        * true  - load data from NetCDF file

    model_type: str
        The type of model to create
        * cnn - generate a Convolutional Neural Network
        * dnn - generate a Deep Neural Network (Feed-forward network)

    Returns
    -------

    """
    """with open('../../logo_bbs.ans', 'r') as f:
        for line in f.readlines():
            print(line, end="")
            sleep(0.1)
    print("\n\tAutoCaster - a third year project by Alexander "
          "Ferguson at the University of East Anglia (UEA)"
          "\n\tData supplied by the Met Office "
          "© Crown copyright 2021, the Met Office\n\n\t"
          "NOTE: when loading file counts may decrease as file discovery "
          "traverses directories")"""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data")
    input_data_dir = os.path.join(data_dir, 'input_data.npy')
    output_data_dir = os.path.join(data_dir, 'output_data.npy')

    if load_data:
        # open a log file for session
        with open('../../log.log', 'w') as f:
            f.write("LOG FILE " + datetime.now().strftime("%Y/%m/%d:%H:%M"))

        loader = auto_forecaster.core.FileLoader(0, 0)
        for i in range(len(regions)):
            regions[i].calc_total_files(None)
            regions[i].set_loader(loader)
            regions[i].loader.adjust(total=regions[i].total_files)

        Parallel(n_jobs=16, require='sharedmem')(
            delayed(parallel_processing)(i) for i in range(len(regions)))

        input_data = np.array([region.data[data]['input']
                               for region in regions for data in region.data])

        output_data = np.asarray([region.data[data]['output']
                                 for region in regions for data in region.data]
                                )
        with open(input_data_dir, 'wb') as f:
            np.save(f, input_data)
        with open(output_data_dir, 'wb') as f:
            np.save(f, output_data)
    else:
        with open(input_data_dir, 'rb') as f:
            input_data = np.load(f)
        with open(output_data_dir, 'rb') as f:
            output_data = np.load(f)

    max_shape = max([output.shape for output in output_data])
    for o in range(len(output_data)):
        pad_width = max_shape[1] - output_data[o].shape[0]
        output_data[o] = np.pad(output_data[o], (0, pad_width), 'constant',
                                constant_values=-1)

    """input_data_concat = []
    for i in input_data:
        input_data_concat.append(i.flatten())
    input_data_concat = np.array(input_data_concat)"""
    inputs = keras.layers.Conv2D(8, 3, input_shape=input_data[0].shape,
                                 padding='same')

    normalizer = keras.layers.experimental.preprocessing.Normalization(
        input_shape=input_data.shape)
    normalizer.adapt(input_data)

    outputs = keras.layers.Dense(max_shape[1],
                                 name="forecast_text_vector", dtype=int32)

    es = EarlyStopping(monitor='accuracy', mode='max', patience=100)
    mc = ModelCheckpoint('../../models/model_a_dnn_best.h5',
                         monitor='accuracy', mode='max', save_best_only=True)
    model = keras.models.Sequential([inputs, keras.layers.Flatten(),
                                     outputs])
    model.summary()
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    model.fit(input_data,
              np.asarray([region.data[data]['output']
                          for region in regions for data in region.data]
                         ),
              batch_size=32, epochs=10000, validation_split=0.2, callbacks=[mc])
    model.save('../../models/model_a_dnn.h5')


if __name__ == '__main__':
    start_process()

"""
Test framework using data that the model would not have seen
"""
import glob
import os
import sys

import keras
import numpy as np
from joblib import Parallel, delayed

import auto_forecaster.core.regions

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

regions = auto_forecaster.core.regions.get_regions_with_tokeniser()


def parallel_processing(region_idx):
    regions[region_idx].process_data(mode="test")


if __name__ == '__main__':
    loader = auto_forecaster.core.FileLoader(0, 0)
    for i in range(len(regions)):
        regions[i].calc_total_files(None, mode="test")
        regions[i].set_loader(loader)
        regions[i].loader.adjust(total=regions[i].total_files)

    Parallel(n_jobs=4, require='sharedmem')(delayed(parallel_processing)(i)
                                            for i in range(len(regions)))

    input_data = np.array([region.data[data]['input'] for region in regions
                           for data in region.data])
    output_data = [region.data[data]['output'] for region in regions
                   for data in region.data]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "models")
    model_locations = os.path.join(model_dir, 'model_*')
    for models in glob.glob(model_locations):
        model = keras.models.load_model(models)
        predictions = model.predict(input_data)
        print(predictions)
        texts = regions[0].tokeniser.sequences_to_texts(predictions)
        print(texts)

        model_name = os.path.basename(models)
        text_folder = os.path.join(model_dir, "text")
        for i in range(len(predictions)):
            text_file = os.path.join(text_folder, model_name + str(i) + ".txt")
            with open(text_file, 'w') as f:
                f.write(texts[i] + "\n")
                f.write(output_data[i])

import pandas as pd
import os
import tifffile
import numpy as np

def get_panel(start_dir, panel_df):
    for file in os.listdir(start_dir):
        if '_full.csv' in file:
            seq_filename = os.path.join(start_dir, file)
            break
    seq = pd.read_csv(seq_filename, header=None)
    seq = seq.rename(columns={0: "Metal_Tag"})
    res = pd.merge(seq, panel_df, how="inner", on=["Metal_Tag"])
    panel = list(res["Target"])
    return panel
def measure(cell, image, mask, markers, sample):
    cell_y = mask == cell
    y = np.where(mask == cell)[0].mean()
    x = np.where(mask == cell)[1].mean()
    area = np.where(mask == cell)[0].shape[0]
    y_max = np.where(mask == cell)[0].max()
    x_max = np.where(mask == cell)[1].max()
    measuredvalue = image[:,cell_y].mean(1)
    cols = markers + ['sample', 'cell_id', 'x', 'y', 'x_max', 'y_max', 'area']
    values = list(measuredvalue)  + [sample, cell, x, y, x_max, y_max, area]
    df = pd.DataFrame(columns=cols)
    df.loc[len(df)] = values
    return df
def make_cell(mask_tiff, full_tiff, sample, panel):
    mtx = []
    mask = mask_tiff
    
    if len(mask.shape) == 3 and mask.shape[2] == 1:
        mask = mask[...,0]
    image = full_tiff
    assert mask.shape[0] == image.shape[1]
    assert mask.shape[1] == image.shape[2]
    cell_ids = np.unique(np.reshape(mask, -1))
    cell_ids = cell_ids[cell_ids != 0]
    for cell in cell_ids:
        mtx.append(
            measure(cell, image, mask, panel, sample)
        )
    return mtx

def df_measured(start_dir, sample_df, panel):
    mtxs = []
    excluded_images = []
     
    for file in os.listdir(start_dir):
        if '_full.tiff' in file:
            full_tiff = os.path.join(start_dir, file)
            # print(full_tiff)
            imc_tiff = tifffile.TiffFile(full_tiff)
            image = imc_tiff.asarray()
            mask_file_name=file.replace('_full', '_IA_mask')
            mask_tiff = os.path.join(start_dir, mask_file_name)
            if image.shape[1] < 50 or not os.path.isfile(mask_tiff):
                excluded_images.append(file)
                continue
            mask = tifffile.imread(mask_tiff)
            row = sample_df.loc[sample_df['TiffName'] == file]
            sample = row['SampleName'].iloc[0]
            cells = make_cell(mask, image, sample, panel)
            if len(cells) > 0:
                mtxs.append(pd.concat(cells))
    df_measured = pd.concat(mtxs)
    df_measured = df_measured.reset_index()
    df_measured = df_measured.drop(['index'], axis=1)
    return df_measured
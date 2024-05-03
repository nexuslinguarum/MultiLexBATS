import statsmodels
from statsmodels.stats.inter_rater import fleiss_kappa
import pandas as pd
import os
import numpy as np

PATH_DIR = 'data/mBATS_v1/'

def iaa_translations_per_language(main_dir):

    translations_per_lang = {}
    for folder in sorted(os.listdir(main_dir)):
        folder_dir = os.path.join(main_dir, folder)
        if folder[0] == '.':
            print('Ignoring:', folder)
            continue

        for f in os.listdir(folder_dir):
            rel_id = f.split(' ')[0]
            if rel_id != 'L11':
                #print('Ignoring:', f)
                continue

            lang = folder.upper()
            print('IAA file:', lang, folder_dir, f)
            translations = read_translations(os.path.join(folder_dir, f))

            if lang not in translations_per_lang:
                translations_per_lang[lang] = [translations]
            else:
                translations_per_lang[lang].append(translations)

    return translations_per_lang


def read_translations(file, ignore_extra=True, n_columns=1):
    df_file = pd.read_excel(file)
    #lang = df_file.columns[4].upper()

    translations = []
    for i, row in df_file.iterrows():

        if str(row[2]) != 'nan' or str(row[3]) != 'nan':
            translations.append(row[4])

        elif not ignore_extra:
            translations.append(row[4])

    return translations


def transpose_translations(translations):
    a = np.array(translations)
    at = a.transpose()
    return at

def compute_fleiss(translations):
    aggr_data = statsmodels.stats.inter_rater.aggregate_raters(translations)
    fleiss = statsmodels.stats.inter_rater.fleiss_kappa(aggr_data[0], method='fleiss')
    return fleiss


translations = iaa_translations_per_language(PATH_DIR)
for k, v in translations.items():
    vt = transpose_translations(v)
    #print(k, v)
    fleiss = compute_fleiss(vt)
    #print(k, fleiss)

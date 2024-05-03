import random

import pandas as pd
import os
import re

import iaa
import export_utils
from Entry import Entry, RelationEntries
from StatsObjects import StatsLang, StatsRelation

random.seed(3)

def find_groups(df):
    groups = []
    current_group = []

    for i, row in df.iterrows():
        # patch, cannot read everything as str ...
        for j in range(2, 5):
            row[j] = str(row[j])

        if len(row['Source words']) > 0 and row['Source words'] != 'nan': # TODO: use pd.isna() instead
            current_group = []
            curr_id = row[0]
            curr_source_en = row[2]

            if len(row[4]) > 0 and row[4] != 'nan':
                current_group.append((curr_id, curr_source_en, re.sub(r"\s+", '_', row[4].strip())))
                groups.append(current_group)
            else:
                current_group = None
                print('\tNo translation for source', curr_id, row[2])

        else:
            if current_group == None:
                # print('\tSomething wrong with', row[3])
                continue

            if len(row[4]) > 0 and row[4] != 'nan':  # isinstance(row[4], str) and len(row[4]) > 0:
                if len(row[3]) > 0 and row[3] != 'nan':
                    current_group.append((row[3].strip(), re.sub(r"\s+", '_', row[4].strip())))
                elif row[3] == 'nan':
                    words = row[4].split(',')
                    for w in words:
                        current_group.append(('EXTRA', re.sub(r"\s+", '_', w.strip())))

            elif row[3] != 'nan' and row[4] == 'nan':
                print('\tNo translation for target', row[3], row[4])
                current_group.append((row[3], 'EMPTY'))

    return groups




# working directory of MLBATS: one dir per language, one XLS file for relation (L01--L10)
PATH_DIR = 'data/mBATS_v1/'
all_dfs = []

#IGNORE_LANGUAGES = ['BM', 'MK']
IGNORE_LANGUAGES = []

iaa_translations_per_lang = {}

for dir in os.listdir(PATH_DIR):
    folder_dir = os.path.join(PATH_DIR, dir)

    if dir[0] == '.':
        print('Ignoring:', dir)
        continue

    for f in os.listdir(folder_dir):

        rel_id = f.split(' ')[0]
        if rel_id == 'L11': # IAA file, process and compute later
            iaa_translations = iaa.read_translations(os.path.join(folder_dir, f))
            if lang not in iaa_translations_per_lang:
                iaa_translations_per_lang[lang] = [iaa_translations]
            else:
                iaa_translations_per_lang[lang].append(iaa_translations)
            continue

        elif rel_id not in export_utils.REL_MAP: # unknown file
            print('Ignoring:', f)
            continue

        print('Processing', folder_dir, f)
        raw_df = pd.read_excel(os.path.join(folder_dir, f))  # cannot read everything as str...
        lang = raw_df.columns[4].upper()
        if len(lang) != 2:
            print('Language not an ISO code?', lang)

        if lang in IGNORE_LANGUAGES:
            print('Ignoring', lang)
            continue

        groups = find_groups(raw_df)
        rel_id = str(f).split(' ')[0]

        rel = re.split('\[(.*?)\]', str(f))[1]
        for g in groups:
            for i, r in enumerate(g):

                if i == 0:
                    continue

                row = pd.DataFrame({
                    'Source_id': g[0][0],
                    'Source_en': g[0][1],
                    'Source_trans': g[0][2],
                    'Target_en': r[0],
                    'Target_trans': r[1],
                    'lang': lang,
                    'rel': rel,
                    'rel_id': rel_id
                }, index=[str(g[0][0]) + '_' + str(i)])

                all_dfs.append(row)

df = pd.concat(all_dfs)

print(('Full_df:', len(df)))
print('Languages', df.groupby('lang').size())
# print(df.head())
# df.to_csv('data/all_mbats_for_stats.csv')

dataset = {}
languages = sorted(df['lang'].unique())
print('Languages', len(languages), sorted(languages))

for i, row in df.iterrows():
    rel = row['rel_id']
    if rel not in export_utils.REL_MAP:
        print('Unknown relation:', rel)
        continue

    if rel not in dataset:
        dataset[rel] = RelationEntries(rel)
    if row['Source_id'] not in dataset[rel].source_ids():
        dataset[rel].add_entry(row['Source_id'])

    lang = row['lang']
    dataset[rel].add_row(row['Source_id'], row['lang'], row['Source_en'], row['Target_en'], row['Source_trans'],
                         row['Target_trans'])

for k, re in dataset.items():
    re.mark_duplicates()

stats_all_relations = {l:{'Sources':0, 'Targets':0, 'NoTranslation':0, 'Duplicates':0, 'Extras':0, 'Empty':0} for l in languages}

for lang in languages:
    print(lang, '##########')
    stats_l = StatsLang(lang)
    rids = sorted(list(dataset.keys())) # natural order
    for rid in rids:
        stats_l.add_relation(dataset[rid])
    stats_l.report()
    if lang in iaa_translations_per_lang:
        vt = iaa.transpose_translations(iaa_translations_per_lang[lang])
        # print(k, v)
        fleiss = iaa.compute_fleiss(vt)
        print('Fleiss Kappa:', fleiss)


export_utils.generate_all_languages_files(languages, dataset, "all")
export_utils.all_files_to_single_csv("all", "all_in_one.csv")

#export_utils.generate_in_original_bats_format(languages, dataset, "original")

#export_utils.generate_in_split_bats_format(languages, dataset, "split")
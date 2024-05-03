import os
import pandas as pd
import random

REL_MAP = {
    'L01': 'hypernyms - animals',
    'L02': 'hypernyms - misc',
    'L03': 'hyponyms - misc',
    'L04': 'meronyms - substance',
    'L05': 'meronyms - member',
    'L06': 'meronyms - part',
    'L07': 'synonyms - intensity',
    'L08': 'synonyms - exact',
    'L09': 'antonyms - gradable',
    'L10': 'antonyms - binary'
}

def generate_all_languages_files(languages, dataset, output_dir):
    print('Generating all languages files ...')
    cols = ['ID', 'Relation', 'Source', 'Target']
    cols.extend(languages)

    for rid, re in dataset.items():
        print('\tGenerating', rid)
        df_all_languages = pd.DataFrame(columns=cols)
        dict = {}
        for eid, e in re.entries.items():
            en = e.source_trans['EN']
            dict = {'ID': eid, 'Relation': REL_MAP[rid], 'Source': en}
            for lang in languages:
                if lang == 'EN': continue
                dict[lang] = e.source_trans[lang] if lang in e.source_trans else ''
                # else 'EMPTY'
                # print(lang, e.source_trans[lang] if lang in e.source_trans else 'EMPTY?', end='\t')
            df_all_languages.loc[len(df_all_languages)] = dict

            for w in e.target_trans:
                dict = {'Target': w}
                for lang in languages:
                    if lang == 'EN': continue
                    dict[lang] = e.target_trans[w][lang] if lang in e.target_trans[w] and 'EMPTY' not in e.target_trans[w][lang] else ''
                    # else 'EMPTY'
                    # print('\t', lang, e.target_trans[w][lang] if lang in e.target_trans[w] else 'EMPTY?', end='\t')
                df_all_languages.loc[len(df_all_languages)] = dict

            dict = {}
            for lang, extras in e.extras.items():
                dict[lang] = ','.join(extras)
            df_all_languages.loc[len(df_all_languages)] = dict

            df_all_languages.to_excel(output_dir+"/all_" + rid + ".xlsx", index=False)

def generate_in_original_bats_format(languages, dataset, output_dir):
    print('Generating in original BATS format...')
    dict_rel_lang = {} # rel -> lang -> source -> targets
    for rid, re in dataset.items():
        dict_rel_lang[rid] = {}
        for eid, e in re.entries.items():
            for lang in languages:
                if lang not in dict_rel_lang[rid]:
                    dict_rel_lang[rid][lang] = {}

                if lang in e.source_trans and len(e.source_trans[lang]) > 0 and 'NO_TRANSLATION' not in e.source_trans[lang] and 'EMPTY' not in e.source_trans[lang]:
                    source = e.source_trans[lang]
                    dict_rel_lang[rid][lang][source] = []
                    #print('*', dict_rel_lang[rid][lang])
                    for w in e.target_trans:
                        if lang in e.target_trans[w] and len(e.target_trans[w][lang]) > 0 and ('NO_TRANSLATION' not in e.target_trans[w][lang]) and ('DUPLICATE' not in e.target_trans[w][lang]) and ('EMPTY' not in e.target_trans[w][lang]):
                            dict_rel_lang[rid][lang][source].append(e.target_trans[w][lang])
                    if lang in e.extras:
                        dict_rel_lang[rid][lang][source].extend(e.extras[lang])

    # create the files
    write_bats_file(dict_rel_lang, output_dir)

def generate_in_split_bats_format(languages, dataset, output_dir, to_predict=30):
    random.seed(3)
    print('Languages:', len(languages))
    dict_rel_use = {}
    for rid, re in dataset.items():
        dict_rel_use[rid] = []

        for eid, e in re.entries.items():
            # source has translation for every language (+1 for en) and at least one target in every language (en is the index)
            if len(e.source_trans) == len(languages)+1 and len(e.languages_with_targets()) == len(languages):
                dict_rel_use[rid].append(e)

        random.shuffle(dict_rel_use[rid])

    dict_rel_lang_cd = {}
    dict_rel_lang_ab = {}
    for rel, entries in dict_rel_use.items():
        dict_rel_lang_cd[rel] = {}
        dict_rel_lang_ab[rel] = {}

        dict_rel_lang_cd[rel]['EN'] = {}
        dict_rel_lang_ab[rel]['EN'] = {}
        for e in entries:
            source = e.source_trans['EN']
            dict_to_add = dict_rel_lang_cd[rel]['EN'] if len(dict_rel_lang_cd[rel]['EN']) < to_predict else dict_rel_lang_ab[rel]['EN']
            dict_to_add[source] = list(e.target_trans.keys())
            #if source == 'pony':
            #    print('+', dict_to_add[source])

        for lang in languages:
            dict_rel_lang_cd[rel][lang] = {}
            dict_rel_lang_ab[rel][lang] = {}

            for e in entries:
                source = e.source_trans[lang]

                dict_to_add = dict_rel_lang_cd[rel][lang] if len(dict_rel_lang_cd[rel][lang]) < to_predict else dict_rel_lang_ab[rel][lang]
                dict_to_add[source] = []

                for w in e.target_trans:
                    if lang in e.target_trans[w] and len(e.target_trans[w][lang]) > 0 and (
                            'NO_TRANSLATION' not in e.target_trans[w][lang]) and (
                            'DUPLICATE' not in e.target_trans[w][lang]) and ('EMPTY' not in e.target_trans[w][lang]):
                        dict_to_add[source].append(e.target_trans[w][lang])
                    if lang in e.extras:
                        dict_to_add[source].extend(e.extras[lang])

        # create the files
        write_bats_file(dict_rel_lang_cd, output_dir, suffix='cd')
        write_bats_file(dict_rel_lang_ab, output_dir, suffix='ab')

def write_bats_file(dict_rel_lang, output_dir, suffix=None):
    for rel, langs in dict_rel_lang.items():
        for lang, row in langs.items():
            path = output_dir + '/' + lang.lower() + '/4_Lexicographic_semantics/'
            print('Exporting', suffix, path)
            if not os.path.exists(path):
                os.makedirs(path)
            name = path + rel + ('_' + suffix if suffix else '') +'.txt'
            with open(name, 'w') as f:
                for k, v in row.items():
                    if len(v) > 0:
                        f.write(k + '\t' + '/'.join(v) + '\n')


def all_files_to_single_csv(input_dir, output_file):
    print('All languages files to single CSV ...')
    rows = []
    for file in os.listdir(input_dir):
        rel_id = file.split('_')[1].split('.')[0]
        df_rel = pd.read_excel(os.path.join(input_dir, file))
        languages = [c for c in df_rel.columns if c != 'ID' and c != 'Relation' and c != 'Source' and c != 'Target']
        #print(rel_id, languages)

        sources = {}
        for index, row in df_rel.iterrows():
            #print(rel_id, index)

            if not pd.isna(row['ID']) and not pd.isna(row['Source']) and pd.isna(row['Target']): # source word
                source_id = row['ID']
                relation = row['Relation']

                # English
                sources['EN'] = row['Source']
                for lang in languages:
                    if not pd.isna(row[lang]) and 'NO_TRANSLATION' not in row[lang] and 'DUPLICATE' not in row[lang]:
                        sources[lang] = row[lang]

            elif pd.isna(row['Source']) and not pd.isna(row['Target']):  # target word
                # English
                line_en = {'Source': sources['EN'], 'Source_id': source_id, 'Target': row['Target'], 'Target_id': index,
                           'lang': 'EN', 'rel': relation, 'rel_id': rel_id}
                rows.append(line_en)
                for lang in languages:
                    if not pd.isna(row[lang]) and lang in sources and 'NO_TRANSLATION' not in row[lang] and 'DUPLICATE' not in row[lang]:
                        line = {'Source': sources[lang], 'Source_id': source_id, 'Target': row[lang], 'Target_id': index,
                                'lang': lang.upper(), 'rel': relation, 'rel_id': rel_id}
                        rows.append(line)


    df_all = pd.DataFrame(rows)
    df_all.to_csv(output_file)


def all_languages_files_to_original_bats(input_dir, output_dir):
    print('All languages files to original BATS format ...')
    dict_rel_lang = {} # rel -> lang -> source -> targets

    for file in os.listdir(input_dir):
        rel_id = file.split('_')[1].split('.')[0]
        dict_rel_lang[rel_id] = {}

        print(rel_id)
        df_rel = pd.read_excel(os.path.join(input_dir, file))
        languages = [c for c in df_rel.columns if c != 'ID' and c != 'Relation' and c != 'Source' and c != 'Target']

        dict_lang_sources_targets = {l : {} for l in languages} # lang -> source -> targets .. if a source is duplicated in a language, only one makes it to the file ...
        dict_lang_sources_targets['EN'] = {}

        current_source = {l : None for l in languages}
        current_source['EN'] = None

        for index, row in df_rel.iterrows():
            #print(rel_id, index)

            if not pd.isna(row['ID']) and not pd.isna(row['Source']) and pd.isna(row['Target']): # source word

                # English
                dict_lang_sources_targets['EN'][row['Source']] = []
                current_source['EN'] = row['Source']
                for lang in languages:
                    if not pd.isna(row[lang]) and 'NO_TRANSLATION' not in row[lang] and 'DUPLICATE' not in row[lang]:
                        dict_lang_sources_targets[lang][row[lang]] = []
                        current_source[lang] = row[lang]

            elif pd.isna(row['Source']) and not pd.isna(row['Target']):  # target word
                # English
                dict_lang_sources_targets['EN'][current_source['EN']].append(row['Target'])

                for lang in languages:
                    if not pd.isna(row[lang]) and 'NO_TRANSLATION' not in row[lang] and 'DUPLICATE' not in row[lang]:
                        if not pd.isna(current_source[lang]):
                            dict_lang_sources_targets[lang][current_source[lang]].append(row[lang])

            elif pd.isna(row['Source']) and pd.isna(row['Target']): # extras
                for lang in languages:
                    if not pd.isna(row[lang]) and not pd.isna(current_source[lang]):
                        for w in row[lang].split(','):
                            dict_lang_sources_targets[lang][current_source[lang]].append(w.strip())

            dict_rel_lang[rel_id] = dict_lang_sources_targets


        #for rid, lang_entries in dict_rel_lang.items():
        #    print(rid)
        #    for l, e, in lang_entries.items():
        #        print(l, '->', e)

        write_bats_file(dict_rel_lang, output_dir=output_dir)


#all_files_to_single_csv('all', 'all_in_one.csv')
#all_languages_files_to_original_bats('all', 'original')
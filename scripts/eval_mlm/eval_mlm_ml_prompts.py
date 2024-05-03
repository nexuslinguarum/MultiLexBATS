import pathlib
import pandas as pd
import tqdm
import random

from transformers import pipeline

from templates import PROMPT_TEMPLATES

MATS = {"name": "mats", "path": pathlib.Path('../dataset/')}
MLBATS = {"name": "mbats", "path": pathlib.Path('../mbats/')}

# converted from dataset directory with export_utils.all_files_to_single_csv
ALL_MBATS = '../all_in_one.csv'

DATASET = MLBATS
N_SHOTS = [0, 5]
USE_QUOTES = True

MBERT = {"name": "bert-base-multilingual-uncased", "mask": "[MASK]", "sub_prefix": "##"}
XLMR = {"name": "xlm-roberta-base", "mask": "<mask>", "sub_prefix": "_"}
MODELS = [MBERT, XLMR]

LANGUAGES_USE = [
	('en', 'de'),
#	('de', 'it'),
#	('de', 'sl'),
#	('sk', 'sl'),
#	('sk', 'hr'),
#	('en', 'es'),
#	('en', 'pt'),
#	('en', 'fr'),
#	('en', 'bm'),
#	('en', 'al'),
#	('en', 'el'),
#	('en', 'he'),
#	('en', 'lt'),
#	('en', 'hr'),
#	('fr', 'bm'),
#	('fr', 'en'),
#	('fr', 'ro'),
#	('es', 'it'),
#	('es', 'pt'),
#	('es', 'ro'),

#	('it', 'pt'),
#	('it', 'ro'),
#	('it', 'el'),

#	('hr', 'sl'),
#	('hr', 'sk'),
#	('sl', 'sk'),
]

def expand_prompt(prompt, template, n_shots, tuples, remove, quotes):
	valid = [t for t in tuples if t not in remove]
	valid = random.sample(valid, n_shots)
	examples = [get_complete_analogy(template, a, b, c, d, quotes=quotes) for a, b, c, d in valid]

	return ' '.join(examples) + ' ' + prompt

def get_complete_analogy(template, a, b, c, d, quotes=False):
	return template.format("\"" + a + "\"", "\"" + b + "\"", "\"" + c + "\"", "\"" + d + "\"") if quotes else template.format(a, b, c, d)

def get_multilingual_templates(lang_1, lang_2):
	if lang_1 in PROMPT_TEMPLATES and lang_2 in PROMPT_TEMPLATES:
		if isinstance(PROMPT_TEMPLATES[lang_1][0], list) and isinstance(PROMPT_TEMPLATES[lang_2][0], list):
			prompt = [PROMPT_TEMPLATES[lang_1][i][0] + ' ' + PROMPT_TEMPLATES[lang_2][i][1] for i in range(len(PROMPT_TEMPLATES[lang_1]))]

		elif isinstance(PROMPT_TEMPLATES[lang_1][0], list):
			prompt = [p + ' ' + PROMPT_TEMPLATES[lang_2][1] for p in PROMPT_TEMPLATES[lang_1][0]]

		elif isinstance(PROMPT_TEMPLATES[lang_2][0], list):
			prompt = [PROMPT_TEMPLATES[lang_1][0] + ' ' + p for p in PROMPT_TEMPLATES[lang_2][1]]
		else:
			prompt = [PROMPT_TEMPLATES[lang_1][0] + ' ' + PROMPT_TEMPLATES[lang_2][1]]
		return prompt
	else:
		print('ERROR: No prompts for language', lang_1, lang_2)
		return None

	if lang in PROMPT_TEMPLATES:
		if isinstance(PROMPT_TEMPLATES[lang], str):
			return [PROMPT_TEMPLATES[lang]] if isinstance(PROMPT_TEMPLATES[lang], str) else \
			PROMPT_TEMPLATES[lang]
	else:
		print('ERROR: No prompts for language', lang)
		return None

def fill_template(template, a, b, c, len_d, quotes=False):
	mask = " ".join([pipe.tokenizer.mask_token] * len_d)
	return template.format("\"" + a + "\"", "\"" + b + "\"", "\"" + c + "\"",
						   "\"" + mask + "\"") if quotes else template.format(a, b, c, mask)

def unmask_with_length(prompt, length_b2):
	preds = pipe(prompt)
	if length_b2 == 1: preds = [preds]
	token_ids = [t[0]['token'] for t in preds]
	token_strs = pipe.tokenizer.convert_ids_to_tokens(token_ids)
	token_strs = pipe.tokenizer.convert_tokens_to_string(token_strs)
	token_strs = token_strs.replace(' -', '-').replace('- ', '-').lower()
	return token_strs


for model in MODELS:
	pipe = pipeline(task='fill-mask', model=model['name'], top_k=1)

	def get_lens(bs):
		return {len(pipe.tokenizer.encode(b, add_special_tokens=False)) for b in bs}

	for shots in N_SHOTS:

		all_results = []
		df_all = pd.read_csv(ALL_MBATS)
		rels = df_all['rel_id'].unique()
		rels.sort()

		for lang_pair in tqdm.tqdm(LANGUAGES_USE):

			for rel_id in rels:
				lang_1 = lang_pair[0]
				lang_2 = lang_pair[1]

				df_1 = df_all.query("lang == '" + lang_1.upper() + "' & rel_id == '" + rel_id + "'")
				df_2 = df_all.query("lang == '" + lang_2.upper() + "' & rel_id == '" + rel_id + "'")

				tuples = []
				for i, e1 in df_1.iterrows():
					aligned = df_2.query(
						"Source_id == '" + str(e1['Source_id']) + "' & Target_id == " + str(e1['Target_id']))

					if len(aligned) > 0:
						s1 = e1['Source'].replace('_', ' ').lower()
						t1 = e1['Target'].replace('_', ' ').lower()
						s2 = aligned.iloc[0]['Source'].replace('_', ' ').lower()
						t2 = aligned.iloc[0]['Target'].replace('_', ' ').lower()
						tuples.append((s1, t1, s2, t2))
					# print(s2, t2)
					else:
						# print('No '+lang_1+'->'+lang_2+' translation for:', e1['Source'], e1['Target'])
						continue

				print(f'PROCESSING {len(tuples)} tuples...')
				tuples = [t for t in tuples if 'NO_TRANSLATION' not in t[1] and 'NO_TRANSLATION' not in t[3] and 'DUPLICATE_' not in t[1] and 'DUPLICATE_' not in t[3]]

				res_subcat = []
				for a, b, c, d in tqdm.tqdm(tuples, desc=lang_1+'->'+lang_2+', '+rel_id, leave=False, miniters=30):

					#print(rel_id, ':', a, b, c, d)

					ok = False
					for length in get_lens({d}):
						templates = get_multilingual_templates(lang_1, lang_2) # avoids testing every template: if one is ok, move to next source

						if not templates:
							break

						#print('*** TEMPLATES:', templates, a, b, c, d, length)
						for template in templates:
							prompt = fill_template(template, a, b, c, length, quotes=USE_QUOTES)

							if shots > 0:
								prompt = expand_prompt(prompt, template, shots, tuples, [(a, b), (c, d)],
													   quotes=USE_QUOTES)

							prediction = unmask_with_length(prompt, length)
							#print('*** PROMPT:', prompt, '->', prediction)
							ok = ok or (prediction == d)
							if ok: break  # early stop
						if ok: break  # early stop

					res_subcat.append(int(ok))

				all_results.append({
					'lang_1': lang_1,
					'lang_2': lang_2,
					'relation': rel_id,
					'accuracy': (sum(res_subcat) / len(res_subcat)) if len(res_subcat) > 0 else 0,
					'n_correct': sum(res_subcat),
					'n_items': len(res_subcat)
				})
				print('Results so far:')
				for row in all_results:
					print(row)

	pd.DataFrame.from_records(all_results).to_csv(f'../results/mbats-{model["name"]}-{shots}shots-quotes{USE_QUOTES}-trans.csv')

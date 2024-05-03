import os
import pathlib
import pandas as pd
import tqdm

import random
import re

from transformers import pipeline

from templates import PROMPT_TEMPLATES

MATS = {"name": "mats", "path": pathlib.Path('../dataset/')}
MBATS = {"name": "mbats", "path": pathlib.Path('../mbats/')}
MBERT = {"name": "bert-base-multilingual-uncased", "mask": "[MASK]", "sub_prefix": "##"}
XLMR = {"name": "xlm-roberta-base", "mask": "<mask>", "sub_prefix": "_"}

#PAIRS_PATH = pathlib.Path('../analogy_pairs/')
PAIRS_PATH = pathlib.Path('../random_samples_BLOOM/')
N_SHOTS = [0, 5]
USE_QUOTES = True

MODELS = [MBERT, XLMR]

LANGUAGES_USE = ['hr']
TEMPLATES_USE = {l : ' '.join(PROMPT_TEMPLATES[l]) for l in LANGUAGES_USE}

random.seed(3)

def expand_prompt(prompt, template, n_shots, tuples, remove, quotes):
	valid = [t for t in tuples if t not in remove] # p2 was probably removed earlier anyway
	valid = random.sample(valid, n_shots)

	examples = []
	for a, b, c, ds in valid:
		examples.append(get_complete_analogy(template, a, b, c, ds[0], quotes=quotes))

	return ' '.join(examples) + ' ' + prompt


for model in MODELS:
	pipe = pipeline(task='fill-mask', model=model['name'], top_k=1)

	def get_lens(bs, max=8):
		lengths = {len(pipe.tokenizer.encode(b, add_special_tokens=False)) for b in bs}
		lengths = {l for l in lengths if l <= max}
		return lengths

	# for few-shot learning
	def get_complete_analogy(template, a, b, c, d, quotes=False):
		return template.format("\"" + a + "\"", "\"" + b + "\"", "\"" + c + "\"", "\"" + d + "\"") if quotes else template.format(a, b, c, d)

	def get_templates(lang):
		if lang in TEMPLATES_USE:
			return [TEMPLATES_USE[lang]] if isinstance(TEMPLATES_USE[lang], str) else TEMPLATES_USE[lang]
		else:
			print('ERROR: No prompts for language', lang)
			return None

	def fill_template(template, a, b, c, len_d, quotes=False):
		mask = " ".join([pipe.tokenizer.mask_token] * len_d)
		if quotes:
			return template.format("\"" + a + "\"", "\"" + b + "\"", "\"" + c + "\"", "\"" + mask + "\"")
		else:
			return template.format(a, b, c, mask)

	def unmask_with_length(prompt, length_b2):
		preds = pipe(prompt)
		if length_b2 == 1: preds = [preds]
		token_ids = [t[0]['token'] for t in preds]
		token_strs = pipe.tokenizer.convert_ids_to_tokens(token_ids)
		token_strs = pipe.tokenizer.convert_tokens_to_string(token_strs)
		token_strs = token_strs.replace(' -', '-').replace('- ', '-').lower()
		return token_strs

	def read_analogy_tuples(file):
		pairs_lang = {}
		df_tuples = pd.read_csv(file)
		#df_tuples = pd.read_excel(file)

		for i, row in df_tuples.iterrows():
			lang = row['Language']
			if lang not in pairs_lang:
				pairs_lang[lang] = []

			ds = eval(row['d'])
			nt = (row['a'], row['b'], row['c'], ds)
			pairs_lang[lang].append((row['a'], row['b'], row['c'], ds))

		return pairs_lang

	for shots in N_SHOTS:
		all_results = []
		for file in tqdm.tqdm(sorted(PAIRS_PATH.glob('*')), desc=f'Running for {shots} shots...'):

			if not file.name.endswith('.csv'):
				continue

			rel_id = file.name.split('_')[1]

			tuples_lang = read_analogy_tuples(PAIRS_PATH / file)
			#print(file, tuples)

			for lang in tuples_lang:

				if lang.lower() not in LANGUAGES_USE:
					continue

				res_subcat = []
				for a, b, c, ds in tuples_lang[lang]:
					ok = False
					for length in get_lens(ds):
						template = get_templates(lang.lower())[0]
						prompt = fill_template(template, a, b, c, length, quotes=USE_QUOTES)

						if shots > 0:
							prompt = expand_prompt(prompt, template, shots, tuples_lang[lang], (a, b, c, ds),
												   quotes=USE_QUOTES)

						prediction = unmask_with_length(prompt, length)
						print(prompt, '->', prediction, prediction in ds)
						ok = ok or (prediction in ds)
						if ok: break

					res_subcat.append(int(ok))

				all_results.append({
					'lang': lang,
					'subcategory': rel_id,
					'category': file.parent.name,
					'accuracy': (sum(res_subcat) / len(res_subcat)) if len(res_subcat) > 0 else 0,
					'n_correct': sum(res_subcat),
					'n_items': len(res_subcat)
				})
				print('Results so far:')
				for row in all_results: print(row)

		pd.DataFrame.from_records(all_results).to_csv(
			f'../results/from-file-mbats-{model["name"]}-{shots}shot-quotes{USE_QUOTES}.csv')


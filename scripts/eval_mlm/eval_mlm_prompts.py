import pathlib
import pandas as pd
import tqdm

import random
import re

from transformers import pipeline

from templates import PROMPT_TEMPLATES

# Datasets must be in the original BATS format
MATS = {"name": "mats", "path": pathlib.Path('../dataset/')}
MLBATS = {"name": "mbats", "path": pathlib.Path('../mbats/')}
DATASET = MLBATS

# number of source words per relation: full relation file = 50
SOURCES_PER_RELATION = 50
# number of analogies to compute for each source word: all = 49
ANALOGIES_PER_SOURCE = 3
# maximum number target words for considering in the first pair
MAX_TARGETS_ANALOGY = 10

N_SHOTS = [0, 5]
USE_QUOTES = True

MBERT = {"name": "bert-base-multilingual-uncased", "mask": "[MASK]", "sub_prefix": "##"}
XLMR = {"name": "xlm-roberta-base", "mask": "<mask>", "sub_prefix": "_"}
MODELS = [MBERT, XLMR]

LANGUAGES_USE = ['bm']
TEMPLATES_USE = {l : ' '.join(PROMPT_TEMPLATES[l]) for l in LANGUAGES_USE}

random.seed(3)

def expand_prompt(prompt, template, n_shots, pairs, remove, quotes):
	valid = [p for p in pairs if p not in remove] # p2 was probably removed earlier anyway
	valid = random.sample(valid, n_shots*2)

	examples = []
	for n in range(n_shots):
		a, b = valid[n]
		c, d = valid[n_shots + n]
		examples.append(get_complete_analogy(template, a, list(b)[0], c, list(d)[0], quotes=quotes))

	return ' '.join(examples) + ' ' +prompt


for model in MODELS:
	pipe = pipeline(task='fill-mask', model=model['name'], top_k=1)

	def get_lens(bs, max=10):
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

	for shots in N_SHOTS:

		all_results = []
		for lang in sorted(list(TEMPLATES_USE.keys())):
			mats_dir = DATASET["path"] / lang
			for file in tqdm.tqdm(sorted(mats_dir.glob('**/*.txt')), desc=lang):

				if '4_Lexicographic_semantics' not in str(file):
					print('IGNORE:', file)
					continue

				print('PROCESSING', file)

				with open(file) as fh:
					pairs = map(str.split, filter(None, map(str.strip, fh)))
					pairs = [(a, set(filter(None, b.split('/')))) for a, b in pairs]
					pairs = [(a.replace('_', ' ').lower(), {bn.replace('_', ' ').lower() for bn in b}) for a, b in
							 pairs]

				#print(len(pairs), ' entries: ', pairs)

				sources_test = pairs if len(pairs) <= SOURCES_PER_RELATION else random.sample(pairs, SOURCES_PER_RELATION)

				res_subcat = []
				for i1, (a1, b1s) in tqdm.tqdm(list(enumerate(sources_test)), desc=lang+'/'+file.name, leave=False):

					use_as_first = pairs.copy()
					del use_as_first[i1]

					if len(use_as_first) > ANALOGIES_PER_SOURCE:
						use_as_first = random.sample(use_as_first, ANALOGIES_PER_SOURCE)

					#print('# results = ', len(res_subcat), '+', len(use_as_first))
					for i2, (a2, b2s) in list(enumerate(use_as_first)):
						ok = False

						# tests for each b1 in b1s and for each number of masks in bs2
						# one correct answer out of the previous is enough!
						# for length in get_lens(b2s):
						#	ok = ok or any(map(lambda b1: unmask_with_length(lang, a1, b1, a2, length) in b2s, b1s))

						if len(b2s) > MAX_TARGETS_ANALOGY:
							b2s = list(b2s)[:MAX_TARGETS_ANALOGY]

						# inverted (a1,b1s) <-> (a2,b2s) for easier selection of sample for first pair
						for length in get_lens(b1s):
							for b2 in b2s:
								templates = get_templates(lang) # avoids testing every template: if one is ok, move to next source
								for template in templates:
									prompt = fill_template(template, a2, b2, a1, length, quotes=USE_QUOTES)

									if shots > 0:
										prompt = expand_prompt(prompt, template, shots, pairs, [(a2, b2s), (a1, b1s)], quotes=USE_QUOTES)
									#print('** EXPANDED PROMPT:', prompt)

									prediction = unmask_with_length(prompt, length)
									ok = ok or (prediction in b1s)
									if ok: break  # early stop: correct prediction for one template
								if ok: break # early stop: correct prediction for one first target b2
							if ok: break  # early stop: correct prediction for one length of masks

						res_subcat.append(int(ok))

				all_results.append({
					'lang': lang,
					'subcategory': file.name,
					'category': file.parent.name,
					'accuracy': (sum(res_subcat) / len(res_subcat)) if len(res_subcat) > 0 else 0,
					'n_correct': sum(res_subcat),
					'n_items': len(res_subcat)
				})
				print('Results so far:')
				for row in all_results:
					print(row)

		pd.DataFrame.from_records(all_results).to_csv(f'../results/{DATASET["name"]}-{model["name"]}-{shots}shot-perSource{ANALOGIES_PER_SOURCE}-sourcesRel{SOURCES_PER_RELATION}-maxTargets{MAX_TARGETS_ANALOGY}-quotes{USE_QUOTES}.csv')

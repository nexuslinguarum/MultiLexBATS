class Entry:

    def __init__(self, eid):
        self.eid = str(eid)
        self.target_trans = {} # target_en -> lang -> target_trans
        self.source_trans = {} # lang -> source_trans
        self.extras = {} # lang -> extra_targets

    def add_row(self, lang, source_en, target_en, source, target):

        if isinstance(target_en, str) and len(target_en) > 0:
            if target_en == 'EXTRA':
                if lang not in self.extras:
                    self.extras[lang] = [target.replace(' ', '_')]
                else:
                    self.extras[lang].append(target.replace(' ', '_'))

            else:
                if 'EN' not in self.source_trans:
                    self.source_trans['EN'] = source_en

                if lang not in self.source_trans:
                    self.source_trans[lang] = source.replace(' ', '_')

                if target_en not in self.target_trans:
                    self.target_trans[target_en] = {}

                if lang not in self.target_trans[target_en]: # to avoid replacement by English DUPLICATES
                    self.target_trans[target_en][lang] = target.replace(' ', '_')

    def source_in(self, lang):
        return self.source_trans[lang] if lang in self.source_trans else None

    def targets_in(self, lang):
        targets = [v[lang] for k, v in self.target_trans.items() if lang in v if not v[lang].startswith('DUPLICATE') and v[lang] != 'EMPTY']
        return targets

    def no_translations_in(self, lang):
        no_trans = []
        for k, v in self.target_trans.items():
            if lang in v:
                if v[lang] == 'NO_TRANSLATION':
                    no_trans.append(k)
        return no_trans

    def duplicates_in(self, lang):
        dups = []
        for k, v in self.target_trans.items():
            if lang in v:
                if v[lang].startswith('DUPLICATE_'):
                    dups.append((k, v[lang]))
        return dups

    def extras_in(self, lang):
        return self.extras[lang] if lang in self.extras else []

    def empty_in(self, lang):
        empty = []
        for k, v in self.target_trans.items():
            if lang in v:
                if v[lang] == 'EMPTY':
                    empty.append((k, v[lang]))
        return empty

    def mark_duplicates(self):
        targets_lang = {}
        for tar_en, l_w in self.target_trans.items():
            for lang, w in l_w.items():
                if lang not in targets_lang:
                    targets_lang[lang] = set()

                if w != 'EMPTY':
                    if w in targets_lang[lang]:
                        self.target_trans[tar_en][lang] = 'DUPLICATE_' +  w
                    elif not w.startswith('DUPLICATE_'):
                        targets_lang[lang].add(w)

    def languages_with_targets(self):
        unique_langs = set()
        for ten, trans in self.target_trans.items():
            for lang, tar in trans.items():
                if 'EMPTY' not in tar and 'NO_TRANSLATION' not in tar:
                    unique_langs.add(lang)
        return unique_langs

    def __str__(self):
        entry_str = self.eid
        entry_str = entry_str + '\n\tSources:' + str(self.source_trans)
        entry_str = entry_str + '\n\tTargets:' + str(self.target_trans)
        entry_str = entry_str + '\n\tExtras:' + str(self.extras)
        return entry_str


class RelationEntries:

    def __init__(self, rid):
        self.rel_id = rid
        self.entries = {}

    def source_ids(self):
        return self.entries.keys()

    def add_entry(self, sid):
        self.entries[sid] = Entry(sid)

    def get_entry(self, sid):
        return self.entries[sid]

    def add_row(self, eid, lang, source_en, target_en, source, target):
        self.entries[eid].add_row(lang, source_en, target_en, source, target)

    def mark_duplicates(self):
        for k, e in self.entries.items():
            e.mark_duplicates()
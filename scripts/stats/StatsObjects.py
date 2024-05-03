class StatsLang:

    def __init__(self, lang):
        self.lang = lang
        self.relations = {}

    def add_relation(self, rel_entries):
        self.relations[rel_entries.rel_id] = StatsRelation(rel_entries, self.lang)

    def report(self):
        for rid, s in self.relations.items():
            print(rid, ':', s.stats)
        self.report_all_relations()

    def report_all_relations(self):
        tab = {'Sources': 0, 'Targets': 0, 'NoTranslation': 0, 'Duplicates': 0, 'Extras': 0, 'Empty': 0}
        for rid, s in self.relations.items():
            tab['Sources'] = tab['Sources'] + s.stats['Sources']
            tab['Targets'] = tab['Targets'] + s.stats['Targets']
            tab['NoTranslation'] = tab['NoTranslation'] + s.stats['NoTranslation']
            tab['Duplicates'] = tab['Duplicates'] + s.stats['Duplicates']
            tab['Extras'] = tab['Extras'] + s.stats['Extras']
            tab['Empty'] = tab['Empty'] + s.stats['Empty']
        print('ALL:', tab['Sources'], '&', tab['Targets'], '&', tab['NoTranslation'], '&', tab['Duplicates'], '&', tab['Extras'], '&', tab['Empty'])

class StatsRelation:

    def __init__(self, rel_entries, lang):
        self.lang = lang
        self.stats = {'Sources':0, 'Targets':0, 'NoTranslation':0, 'Duplicates':0, 'Extras':0, 'Empty':0}

        for sid, e in rel_entries.entries.items():
            if e.source_in(lang) != None:
                self.stats['Sources'] = self.stats['Sources'] + 1

            self.stats['Targets'] = self.stats['Targets'] + len(e.targets_in(self.lang))
            self.stats['NoTranslation'] = self.stats['NoTranslation'] + len(e.no_translations_in(self.lang))
            self.stats['Duplicates'] = self.stats['Duplicates'] + len(e.duplicates_in(self.lang))
            self.stats['Extras'] = self.stats['Extras'] + len(e.extras_in(self.lang))
            self.stats['Empty'] = self.stats['Empty'] + len(e.empty_in(self.lang))
import re


necromancer = re.compile('necro(mancer)?', re.IGNORECASE)
guardian = re.compile('guard(ian)?', re.IGNORECASE)
ranger = re.compile('range(r)?', re.IGNORECASE)
thief = re.compile('thief', re.IGNORECASE)
warrior = re.compile('warr(ior)?', re.IGNORECASE)
revenant = re.compile('rev(enant)?', re.IGNORECASE)
elementalist = re.compile('ele(mentalist)?', re.IGNORECASE)
mesmer = re.compile('mes(mer)?', re.IGNORECASE)
engineer = re.compile('engi(neer)?', re.IGNORECASE)



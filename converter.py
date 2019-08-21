#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue August 6 09:45:08 2019
 @author: Sina Ahmadi (ahmadi.sina@outlook.com)
"""

import codecs
import string
import json
import os
import sys
import shortuuid
shortuuid.set_alphabet(string.digits)

class template:
	def __init__(self, configuration): #source_language, target_language, source_script="", target_script=""):
		self.source_language = configuration["source_language"]
		self.source_language_code = configuration["source_language_code"]
		self.source_script = configuration["source_language_script"]
		self.source_lang_script = self.source_language
		if configuration["source_language_script"] and configuration["source_language_code"]:
			self.source_lang_script = configuration["source_language_code"] + "-" + configuration["source_language_script"]
		self.source_language_url = configuration["source_language_url"]
		self.target_language = configuration["target_language"]
		self.target_language_code = configuration["target_language_code"]
		self.target_script = configuration["target_language_script"]
		self.target_language_url = configuration["target_language_url"]
		self.pos_map = configuration["pos_map"]
		self.gender_map = configuration["gender_map"]
		self.number_map = configuration["number_map"]
		self.affixes_pos = configuration["affixes_pos"]
		self.prefixes = """
@prefix : <http://example.org/owlim/> .
@prefix lexicog: <http://www.w3.org/ns/lemon/lexicog#> .
@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
@prefix vartrans: <http://www.w3.org/ns/lemon/vartrans#> .
@prefix synsem: <http://www.w3.org/ns/lemon/synsem#> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .
@prefix lime: <http://www.w3.org/ns/lemon/lime#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix contact: <http://www.w3.org/2000/10/swap/pim/contact#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
		"""
		#----------------------
		 # LEXICOGRAPHIC RESOURCE
		self.lexicographic_template_header = """
:|-G-|_Dictionary a lexicog:LexicographicResource ;
    dct:title ""@en ;
    dct:description "" ;
    rdfs:label ""@en ;
    dct:created "2019-08-21"^^xsd:date ;
    dct:modified "2019-08-21"^^xsd:date ;
    owl:versionInfo "0.1" ;
    cc:license "" ;
    dct:creator "" ;
	dc:contributer "" ;
	dct:language |-B-| ;
""".replace("|-G-|", self.source_language).replace("|-B-|", self.source_language_url)

		self.lexicographic_entry = """	lexicog:entry :HEAD_entry ;""" 

		self.lexicographic_entry_comp = """
:HEAD_entry a lexicog:Entry ;
	rdfs:member :HEAD_comp ."""

		self.lexicographic_entry_sense = """ rdf:_X :sense ;
"""

		self.lexicographic_tail = """:HEAD a lexicog:LexicographicComponent .
"""
		
		self.lexicographic_entry_comp_cf = """
:HEAD_entry a lexicog:Entry ;
	rdfs:member :CF_comp ;
	owl:sameAs :CF_entry ."""
		#----------------------

		self.lexicon_metadata = """
:|-G-|_lexicon a lime:Lexicon ;
	lime:language "|-A-|" ;
	dct:language |-B-| ;
	lime:lexicalEntries "X-X|-X-|X-X"^^xsd:integer ;
	dct:description ""@en ;
	dct:creator "" ;
""".replace("|-A-|", self.source_language_code).replace("|-B-|", self.source_language_url).replace("|-G-|", self.source_language)

		self.entry_meta = "	lime:entry :lex_HEAD ;"

		self.entry_body = """
:lex_HEAD a ontolex:LexicalEntry, ontolex:ENTRYTYPE ;
	ontolex:canonicalForm :form_HEAD ;
	rdfs:label "HDWORD"@|-C-| ;
	lexinfo:partOfSpeech lexinfo:POS ;
	lexinfo:gender lexinfo:GENDER ;
	ontolex:sense SENSES .

:form_HEAD a ontolex:Form ;
	dct:language |-B-| ;
	ontolex:writtenRep "HDWORD"@|-C-| ;
	lexinfo:number lexinfo:NUMBER ;
""".replace("|-C-|", self.source_lang_script).replace("|-B-|", self.source_language_url)

		self.entry_translation = """:TRANS a ontolex:LexicalEntry ;
	dct:language |-F-| ;
	rdfs:label "LABEL"@|-E-| ;
	ontolex:sense :TRANS_sense ;

:trans_HEAD_sense a vartrans:Translation ;
	vartrans:source :HEAD_sense ;
	vartrans:target :TRANS_sense ;
""".replace("|-E-|", self.target_language_code).replace("|-F-|", self.target_language_url)

		self.entry_example = """:HEAD_sense a lexicog:UsageExample ;
	rdf:value "EX1"@|-C-| ;
	rdf:value "EX2"@|-E-| .
""".replace("|-C-|", self.source_lang_script).replace("|-E-|", self.target_language_code)
		
		self.entry_body_cf = """
:lex_HEAD a ontolex:LexicalEntry, ontolex:ENTRYTYPE ;
	ontolex:canonicalForm :form_HEAD ;
	rdfs:label "HDWORD"@|-C-| ;

:form_HEAD owl:sameAs :form_CF .

""".replace("|-C-|", self.source_lang_script)

		self.lexicog_lexicon_relation = ":lexicog_subj lexicog:describes :lexicon_subj ."

	def create_triple_subject(self, lang, ALL_SUBJECTS):
		search = True
		while search:
			entry_ID = lang + "_" + shortuuid.uuid()[0:10]
			if entry_ID not in ALL_SUBJECTS.keys():
				return entry_ID

	def create_lexicog(self, entry_ID, senses_origin_ID):
		lexico_header = self.lexicographic_entry.replace("HEAD", entry_ID)
		lexico_comp = self.lexicographic_entry_comp.replace("HEAD", entry_ID)
		lexico_sense = ":" + entry_ID + "_comp" 
		lexico_tail = self.lexicographic_tail.replace("HEAD", entry_ID+"_comp")

		for s_ind in range(len(senses_origin_ID)):
			lexico_sense += self.lexicographic_entry_sense.replace("X", str(s_ind)).replace("sense", list(senses_origin_ID)[s_ind]+"_sense_X_comp".replace("X", str(s_ind)))
			lexico_tail += self.lexicographic_tail.replace("HEAD", list(senses_origin_ID)[s_ind]+"_sense_X_comp".replace("X", str(s_ind)))
		
		return lexico_header, lexico_comp, lexico_sense, lexico_tail

	def find_frames(self, word_list):
		frame_boundaries = list()
		for id in range(len(word_list)-1):
			if True not in [True if i != "" else False for i in word_list[id]]:
				pass
			else:
				step = id +1
				while word_list[step][0] == "" and word_list[step][1] == "" and True in [True if i != "" else False for i in word_list[step]]:
					frame_boundaries.append((id, step))
					step = step + 1
				id = step
		return frame_boundaries
# ================================================
# Main
# ================================================
input_file_name, configuration_file_name = "", ""
if len(sys.argv) == 5:
	for i in [1, 3]:
		if sys.argv[i] == "-input":
			input_file_name = sys.argv[i+1]
		elif sys.argv[i] == "-config":
			configuration_file_name = sys.argv[i+1]
if not len(input_file_name) and not len(configuration_file_name):
	raise ValueError('Arguments not identifiable.')

lex = codecs.open(input_file_name, "r", "utf-8").read().replace("\r", "").split("\n")
lex = [e.split("\t") for e in lex]
with open(configuration_file_name) as f:
    configuration = json.load(f)

if not os.path.exists(configuration["source_language"]):
	os.mkdir(configuration["source_language"])

tmplt = template(configuration)

invalids = list()
ALL_SUBJECTS_origin = dict() # entry, 
ALL_SUBJECTS_en = dict()
entry_senses_ID = dict()
final_resource = ""
lexicog_header, lexicog_comp, lexico_sense, lexicog_tail = "", "", "", ""
LEXICON_meta, LEXICON_RESOURCE = "", ""
lexicog_lexicon_triples,lexicog_lexicon_triples_cf = "", ""

lex_frames = tmplt.find_frames(lex)

for ind in range(len(lex)):
	entry = lex[ind]
	entry_type = ""
	is_cf = False
	lexicon_body = ""
	headword = entry[0].strip()
	print(headword)

	# Check if the entry is in a frame. If yes, skip (for this version of the code)
	if ind in [i[1] for i in lex_frames]:
		pass
	# Find entry type (Word, Affix, MultiwordExpression, cf)
	elif headword != "":
		if True in [True if d in headword else False for d in string.digits]:
			pass
		else:
			if entry[1] in tmplt.affixes_pos:
				entry_type = "Affix"
			elif entry[1] == "" and entry[5] != "":
				is_cf = True
			elif "-" not in headword:
				if entry[1] == "":
					if entry[2] != "":
						entry_type = "Word"
						
				elif "," not in headword and entry[1] in tmplt.pos_map.keys(): 
					entry_type = "Word"
			else:
				if " " not in headword and len(headword) > 1:
					entry_type = "MultiwordExpression"
				else:
					entry_type = "Word"

	if entry_type:
		# create subject for triples of the entry
		entry_ID = tmplt.create_triple_subject(tmplt.source_language_code, ALL_SUBJECTS_origin) # entry ID
		ALL_SUBJECTS_origin[entry_ID] = headword

		senses = [s.strip().replace("\"", "") for s in entry[2].split(";")]
		sense_IDs = dict()
		for s in senses:
			if s:
				sense_ID_en = tmplt.create_triple_subject(tmplt.target_language_code, ALL_SUBJECTS_en)
				sense_ID_origin = tmplt.create_triple_subject(tmplt.source_language_code, ALL_SUBJECTS_origin)
				ALL_SUBJECTS_en[sense_ID_en] = s
				sense_IDs[sense_ID_origin]= sense_ID_en

		entry_senses_ID[entry_ID] = sense_IDs

		# LEXICON-LEXICOG RELATION -----
		lexicog_lexicon_triples += tmplt.lexicog_lexicon_relation.replace("lexicog_subj", entry_ID+"_comp").replace("lexicon_subj", "lex_"+entry_ID) + "\n"

		# LEXICOGRAPHIC RESOURCE
		lexicog_entry_output = tmplt.create_lexicog(entry_ID, sense_IDs.keys())
		lexicog_header += lexicog_entry_output[0] + "\n"
		lexicog_comp += lexicog_entry_output[1] + "\n"
		if sense_IDs:
			lexico_sense += lexicog_entry_output[2] + "\n"
		lexicog_tail += lexicog_entry_output[3]

		# LEXICON ----------------------
		LEXICON_meta += tmplt.entry_meta.replace("HEAD", entry_ID)+ "\n"

		# Gender
		gender = "GENDER"
		if entry[1] in tmplt.gender_map.keys():
			gender = tmplt.gender_map[entry[1]]

		# Number
		number = "NUMBER"
		if entry[1] in tmplt.number_map.keys():
			number = tmplt.number_map[entry[1]]

		# Example
		# Examples of idioms and headwords were originally separated by ;
		# This was temporarily ignored. A better conversion of such cases will be needed. 
		examples = dict()
		if entry[3] != "":
			example = entry[3].replace("\"; \"", "|").replace("\", \"", "|").replace("\",\"", "|").replace(", \"", "|")
			for ex in example.split("|"):
				ex = ex.replace("\"", "")
				ex_1, ex_2 = ex.split(":")[0], ex.split(":")[1]
				examples[ex_1.strip()] = ex_2.strip()

		# Idioms should be placed as new entries but in the same lexicographic component of the headword
		lexicon_body = tmplt.entry_body.replace("ENTRYTYPE", entry_type).replace("HEAD", entry_ID).replace("HDWORD", headword).replace("POS", tmplt.pos_map[entry[1]]).replace("GENDER", gender).replace("NUMBER", number).replace("SENSES", ", ".join(":"+s+"_sense" for s in sense_IDs.keys()))
		lexicon_body = lexicon_body.replace("\n	lexinfo:gender lexinfo:GENDER ;", "").replace("\n	lexinfo:number lexinfo:NUMBER ;", "")
		
		translations = ""
		for origin_sense_ID in sense_IDs:
			translations += tmplt.entry_translation.replace("TRANS", sense_IDs[origin_sense_ID]).replace("LABEL", ALL_SUBJECTS_en[sense_IDs[origin_sense_ID]]).replace("HEAD_sense", origin_sense_ID+"_sense") + "\n"

			lexicog_lexicon_triples += tmplt.lexicog_lexicon_relation.replace("lexicog_subj", origin_sense_ID+"_comp").replace("lexicon_subj", origin_sense_ID+"_sense") + "\n"

		examples_content = ""
		for ex in examples:
			examples_content += tmplt.entry_example.replace("HEAD_sense", origin_sense_ID+"_sense").replace("EX1", ex).replace("EX2", examples[ex]) + "\n"

		lexicon_body += "\n" + translations + examples_content
		lexicon_body = lexicon_body.replace("\n\tlexinfo:partOfSpeech lexinfo:POS ;", "").replace("\n\tontolex:sense  .", "")
	
	else:
		# Cf. entries
		if is_cf:
			# print(headword)
			entry_ID = tmplt.create_triple_subject(tmplt.source_language_code, ALL_SUBJECTS_origin) # entry ID
			ALL_SUBJECTS_origin[entry_ID] = headword
			if entry[5].strip() in list(ALL_SUBJECTS_origin.values()):
				CF_id = list(ALL_SUBJECTS_origin.keys())[list(ALL_SUBJECTS_origin.values()).index(entry[5])]
				# Lexicography
				lexicog_header += tmplt.lexicographic_entry.replace("HEAD", entry_ID)+ "\n"
				lexicog_comp += tmplt.lexicographic_entry_comp_cf.replace("HEAD", entry_ID).replace("CF", CF_id) + "\n"
				lexicog_lexicon_triples_cf += tmplt.lexicog_lexicon_relation.replace("lexicog_subj", entry_ID+"_entry").replace("lexicon_subj", "lex_"+entry_ID) + "\n"
				# Lexicon
				LEXICON_meta += tmplt.entry_meta.replace("HEAD", entry_ID)+ "\n"
				lexicon_body = tmplt.entry_body_cf.replace("ENTRYTYPE", "Word").replace("HDWORD", headword).replace("HEAD", entry_ID).replace("CF", CF_id)

			else:
				invalids.append("\t".join(entry))
				
	if lexicon_body:
		LEXICON_RESOURCE += lexicon_body + "\n"


LEXICOGRAPHIC_RESOURCE = (tmplt.lexicographic_template_header + lexicog_header + lexicog_comp + "\n" + lexico_sense + lexicog_tail).replace(" ;\n\n", " .\n\n")
LEXICON_RESOURCE = (tmplt.lexicon_metadata.replace("X-X|-X-|X-X", str(len(lex)-len(invalids))) + LEXICON_meta + LEXICON_RESOURCE).replace(" ;\n\n", " .\n\n")
final_resource = tmplt.prefixes + "\n\n# LEXICOGRAPHIC RESOURCE -------------------------------------------\n " + \
				LEXICOGRAPHIC_RESOURCE + "\n\n# LEXICON ----------------------------------------------------------\n" + \
				LEXICON_RESOURCE + "# LEXICOGRAPHIC RESOURCE - LEXICON RELATIONS -------------------\n\n" + \
				lexicog_lexicon_triples + "\n" + lexicog_lexicon_triples_cf

if True:
	# write invalides
	codecs.open(configuration["source_language"]+"/invalids.txt", "w", "utf-8").write("\n".join(invalids))
	# write triples subject
	with open(configuration["source_language"]+"/entries_ID.json", 'w', encoding='utf-8') as f:
		json.dump(ALL_SUBJECTS_origin, f)

	with open(configuration["source_language"]+"/entry_senses.json", 'w', encoding='utf-8') as f:
		json.dump(entry_senses_ID, f)

	with open(configuration["source_language"]+"/|-E-|_senses_IDs.json".replace("|-E-|", configuration["target_language_code"]), 'w', encoding='utf-8') as f:
		json.dump(ALL_SUBJECTS_en, f)

	# codecs.open("Kurmanji/final.txt", "w", "utf-8").write(final_resource)
	codecs.open(configuration["source_language"]+"/Dictionary.ttl", "w", "utf-8").write(final_resource)



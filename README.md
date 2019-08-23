# Converting tabular data to Ontolex-Lexicog

## Ontolex-Lemon and Lexicog

Lexicography is the science of words and their semantic relationships. Wouldn't it be beneficial to take advantage of linked data for lexicography too? Well, this is the motivation behind Ontolex-Lemon. 

[Lemon](https://lemon-model.net/) stands for the lexicon model for ontologies (*lemon*) which provides rich linguistic grounding for ontologies. By rich, the creators theoretically aim at all types of information related to words in dictionaries, such as morphological and syntactic properties. The [Ontolex-Lemon](https://www.w3.org/2016/05/ontolex/) is the result of the [W3C Ontology-Lexica Community Group](https://www.w3.org/community/ontolex/).

One of the useful modules in Ontolex-Lemon is the [Ontolex-Lemon lexicography module (lexicog)](https://jogracia.github.io/ontolex-lexicog/).

## Conversion to Ontolex-Lexicog

This tool gets as input the lexicographic data in a tabular format, such as [comma-separated values (CSV)](https://en.wikipedia.org/wiki/Comma-separated_values) and tab-separated values (TSV). In the current version of the tool, the conversion can be done for the followings:

- headwords
- part-of-speech tags
- senses
- examples
- idioms
- and `see also`. 

The conversion can be configured using a configuration file called `configuration.json`. In this file, you can set various information such as source and target languages with their codes, PoS tags according to the [Lexinfo module](https://www.lexinfo.net/ontology/2.0/lexinfo). 

To run the code, clone or download [this repository](https://github.com/sinaahmadi/Tabular2Lexicog) and pass the input file and the configuration files respectively following `-input` and `-config` arguments in the command line:

```
python -input Sample_dictionary.tsv -config configuration.json 
```

**Please note that this script can deal with relatively simple structures for the moment**. 

## A working example

These are a few entries in a Kurdish dictionary in tabular format ([original data in `tsv`](https://raw.githubusercontent.com/sinaahmadi/Tabular2Lexicog/master/Sample_dictionary.tsv)):

<table align="center" class="table table-bordered table-hover table-condensed">
	<thead>
		<tr>
			<th>Headword</th>
			<th>POS</th>
			<th>Sense (translation)</th>
			<th>Example</th>
			<th>Expression</th>
			<th>Cf.</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>aferîde</td>
			<td>m</td>
			<td>creature</td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>aferîn</td>
			<td>excl</td>
			<td>bravo</td>
			<td>bravo ji ... re: good for ...</td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>afirandin </td>
			<td>v.t. </td>
			<td>to create</td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>afîş</td>
			<td>f</td>
			<td>poster</td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>aga</td>
			<td>adj</td>
			<td>aware</td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>agadarî</td>
			<td>f</td>
			<td>information</td>
			<td> announcement; awareness</td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>agah</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td>aga</td>
		</tr>
		<tr>
			<td>agahdarî</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td>agadarî</td>
		</tr>
		<tr>
			<td>agir</td>
			<td>m</td>
			<td>fire</td>
			<td></td>
			<td>agir danîn bi: to set fire to</td>
			<td></td>
		</tr>
	</tbody>
</table>

In order to carry out the conversion correctly, we set a few conventions:

- Senses are separated using `;` or `,`. 
- Any part-of-speech tag can be used, as long as the correct mappings are provided in the configuration file. This regards `Word`, `MultiwordExpression` and `Affix` classes in Ontolex-Lemon. 

The results is created in a folder with the source language name, as in [Kurmanji](https://github.com/sinaahmadi/Tabular2Lexicog/tree/master/Kurmanji).

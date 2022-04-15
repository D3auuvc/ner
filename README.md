# EstBERT_NER

## Model description 

EstBERT_NER is a fine-tuned EstBERT model that can be used for Named Entity Recognition (NER). This model was trained on the Estonian NER dataset created by ([Tkachenko, 2010](https://core.ac.uk/download/pdf/16270382.pdf); [Tkachenko et al., 2013](https://aclanthology.org/W13-2412.pdf)). Originally, the Estonian NER dataset was annotated with three types of entities: locations **(LOC)**, organizations **(ORG)** and persons **(PER)**. The reannotated version is annotated with the following entities:
- PER - person names
- GPE - geopolitical entities
- LOC - geographical locations
- ORG - organizations
- PROD - products, things, works of art
- EVENT - events
- DATE - dates
- TIME - times
- TITLE - titles and professions
- MONEY - monetary expressions
- PERCENT - percentages

## How to use 

You can use this model with Transformers pipeline for NER. Post-processing of results may be necessary as the model occasionally tags subword tokens as entities. 

```
from transformers import BertTokenizer, BertForTokenClassification
from transformers import pipeline

tokenizer = BertTokenizer.from_pretrained('tartuNLP/EstBERT_NER')
bertner = BertForTokenClassification.from_pretrained('tartuNLP/EstBERT_NER')

nlp = pipeline("ner", model=bertner, tokenizer=tokenizer)

text = "Kaia Kanepi (WTA 57.) langes USA-s Charlestonis toimuval WTA 500 kategooria tenniseturniiril konkurentsist kaheksandikfinaalis, kaotades poolatarile Magda Linette'ile (WTA 64.) 3 : 6, 6 : 4, 2 : 6."

ner_results = new_nlp(text)

tokens=tokenizer(text)
tokens=tokenizer.convert_ids_to_tokens(tokens['input_ids'])


print(f'tokens: {tokens}')
print(f'NER model:{ner_results}')

```
```
tokens: ['[CLS]', 'kai', '##a', 'kanepi', '(', 'w', '##ta', '57', '.', ')', 'langes', 'usa', '-', 's', 'cha', '##rl', '##est', '##onis', 'toimuval', 'w', '##ta', '500', 'kategooria', 'tennise', '##turniiril', 'konkurentsist', 'kaheksandik', '##finaalis', ',', 'kaotades', 'poola', '##tari', '##le', 'ma', '##gda', 'line', '##tte', "'", 'ile', '(', 'w', '##ta', '64', '.', ')', '3', ':', '6', ',', '6', ':', '4', ',', '2', ':', '6', '.', '[SEP]']

```
```
NER model: [{'entity': 'B-PER', 'score': 0.99999887, 'index': 1, 'word': 'kai', 'start': None, 'end': None}, {'entity': 'B-PER', 'score': 0.97371966, 'index': 2, 'word': '##a', 'start': None, 'end': None}, {'entity': 'I-PER', 'score': 0.99999815, 'index': 3, 'word': 'kanepi', 'start': None, 'end': None}, {'entity': 'B-ORG', 'score': 0.63085276, 'index': 5, 'word': 'w', 'start': None, 'end': None}, {'entity': 'B-GPE', 'score': 0.99999934, 'index': 11, 'word': 'usa', 'start': None, 'end': None}, {'entity': 'B-GPE', 'score': 0.9999685, 'index': 14, 'word': 'cha', 'start': None, 'end': None}, {'entity': 'I-GPE', 'score': 0.8875574, 'index': 15, 'word': '##rl', 'start': None, 'end': None}, {'entity': 'I-GPE', 'score': 0.9996168, 'index': 16, 'word': '##est', 'start': None, 'end': None}, {'entity': 'I-GPE', 'score': 0.9992657, 'index': 17, 'word': '##onis', 'start': None, 'end': None}, {'entity': 'B-EVENT', 'score': 0.99999064, 'index': 19, 'word': 'w', 'start': None, 'end': None}, {'entity': 'I-EVENT', 'score': 0.9772493, 'index': 20, 'word': '##ta', 'start': None, 'end': None}, {'entity': 'I-EVENT', 'score': 0.99999076, 'index': 21, 'word': '500', 'start': None, 'end': None}, {'entity': 'I-EVENT', 'score': 0.99955636, 'index': 22, 'word': 'kategooria', 'start': None, 'end': None}, {'entity': 'B-TITLE', 'score': 0.8771319, 'index': 30, 'word': 'poola', 'start': None, 'end': None}, {'entity': 'B-PER', 'score': 0.99999785, 'index': 33, 'word': 'ma', 'start': None, 'end': None}, {'entity': 'B-PER', 'score': 0.9998398, 'index': 34, 'word': '##gda', 'start': None, 'end': None}, {'entity': 'I-PER', 'score': 0.9999987, 'index': 35, 'word': 'line', 'start': None, 'end': None}, {'entity': 'I-PER', 'score': 0.9999976, 'index': 36, 'word': '##tte', 'start': None, 'end': None}, {'entity': 'I-PER', 'score': 0.99999285, 'index': 37, 'word': "'", 'start': None, 'end': None}, {'entity': 'I-PER', 'score': 0.9999794, 'index': 38, 'word': 'ile', 'start': None, 'end': None}, {'entity': 'B-ORG', 'score': 0.7664479, 'index': 40, 'word': 'w', 'start': None, 'end': None}]
```



## BibTeX entry and citation info

```
@misc{tanvir2020estbert,
      title={EstBERT: A Pretrained Language-Specific BERT for Estonian}, 
      author={Kairit Sirts and ChengHan Chung},
      year={2022},
      eprint={2011.04784},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

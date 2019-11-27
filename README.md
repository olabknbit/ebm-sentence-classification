# ebm-sentence-classification
It is an unsuccessful attempt to reconstruct findings of Kim, Su & Martinez, David & Cavedon, Lawrence & Yencken, Lars. (2011). Automatic classification of sentences to support Evidence Based Medicine. BMC bioinformatics. 12 Suppl 2. S5. 10.1186/1471-2105-12-S2-S5. 
A link for you convenience: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-S2-S5

This project uses dataset from ALTA 2012 competition. https://www.alta.asn.au/events/sharedtask2012/description.html
Please contact the contact author of the article for the dataset yourself.

## Need to know before running
1. You need a dataset from ALTA 2012 Shared Task competition. It is not available online, but the before-mentioned paper has a contact author (David Martinez) to whom you can reach out for the dataset. This is how I got the dataset. 
2. You need to prep the data before you can run the mallet package on them - they are in a wrong format.
This actually entails something TODO for you - the generated training data is in a slightly wrong format.
3. Install mallet: http://mallet.cs.umass.edu/

## TODO
The training data for mallet should be in a form where each document is separated by a blank space.
If we have two documents that we want to train on:
```text
ref_id1 1 This is the first sentence of an abstract
ref_id1 2 And this is the second sentence of the same abstract
ref_id1 3 And here goes third
ref_id2 1 This is the first sentence of an yet ANOTHER abstract
ref_id2 2 And how I hope you guessed, this is a second sentence of a second abstract
``` 
Right now it has a form: 
```text
feature feature class
feature feature feature class
feature feature feature feature class
feature feature class
feature class
```

but in fact it the two documents should be separated by a blank line like:
```text
feature feature class
feature feature feature class
feature feature feature feature class

feature feature class
feature class
```

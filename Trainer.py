#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import re
import json

TRAIN_DATA = []

jsfile = json.load(open(r"C:\Users\926AJ\Desktop\NLP\IO\master_data.data", "r", encoding='utf-8'))
if 'error' in jsfile:
    print("error")
else:
    rowCount = len(jsfile['rows'])
    index = 1
    for row in jsfile['rows']:
        print('training ', index, 'of', rowCount)
        index += 1
        cleanedLabel = re.sub(r'([\s]?[\d]+)', '', row['label'])
        if cleanedLabel != '':
            print(cleanedLabel)
            if cleanedLabel == "verdachte" or cleanedLabel == "slachtoffer" or cleanedLabel == "betrokkene" or cleanedLabel == "appellant" or cleanedLabel == "appellante" or cleanedLabel == "naam" or cleanedLabel == "eiser" or cleanedLabel == "eiseres" or cleanedLabel == "verbalisant" or cleanedLabel == "belanghebbende" or cleanedLabel == "de man" or cleanedLabel == "de vader" or cleanedLabel == "de vrouw" or cleanedLabel == "de moeder" or cleanedLabel == "het kind" or cleanedLabel == "kind 1" or cleanedLabel == "de zoon" or cleanedLabel == "de dochter" or cleanedLabel == "gedaagde" or cleanedLabel == "geintimeerde" or cleanedLabel == "gerekwireerde" or cleanedLabel == "gerequireerde" or cleanedLabel == "rekwirant" or cleanedLabel == "requirant" or cleanedLabel == "rekwirante" or cleanedLabel == "requirante" or cleanedLabel == "slachtoffer" or cleanedLabel == "verzoeker" or cleanedLabel == "verzoekster" or cleanedLabel == "verweerder" or cleanedLabel == "verweerster" or cleanedLabel == "gemachtigde" or cleanedLabel == "vertegenwoordiger" or cleanedLabel == "directeur" or cleanedLabel == "werknemer" or cleanedLabel == "werkgever" or cleanedLabel == "leidinggevende" or cleanedLabel == "arts" or cleanedLabel == "psycholoog" or cleanedLabel == "psychiater" or cleanedLabel == "veroordeelde" or cleanedLabel == "getuige":
                TRAIN_DATA.append((row['line'], {'entities': [(row['start'], row['end'], 'Person')]}))
        # if index > 200:
        # 	break


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=(r"C:\Users\zl0\Desktop\Training Model\nl_model\123", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(
        model=r"C:\Users\926AJ\Desktop\NLP\T_Model\nl_model-0.0.0\nl_model\nl_model-0.0.0",
        output_dir=r"C:\Users\926AJ\Desktop\NLP\Model",
        n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('nl')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    if model is None:
        optimizer = nlp.begin_training()
    else:
        # Note that 'begin_training' initializes the models, so it'll zero out
        # existing entity types.
        optimizer = nlp.entity.create_optimizer()

    print('TRAINING STARTED')

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # optimizer = nlp.begin_training()

        for itn in range(n_iter):
            print('ITERATION {} STARTED'.format(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            # batches = minibatch(TRAIN_DATA, size=compounding(1., 3., 1.001))
            for batch in batches:
                # print('iter', itn, 'batch', batch)
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.35,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)

            print(itn, 'Losses', losses, )

    print('TESTING STARTED')

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    print('SAVING MODEL')

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == '__main__':
    plac.call(main)

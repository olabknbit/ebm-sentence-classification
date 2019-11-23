# Features
# Lexical information:
#   bag-of-words (BOW),
#   unigrams
#   bigrams,
#   POS (Part-of-Speech) information of the tokens in the BOW and bigram representations—used the CPAN module
#       Lingua::EN::Tagger as POStagger.
#
# Semantic information
#   Metathesaurus from the Unified Medical Language System (UMLS)
#       we use this resource in two ways:
#       (i) directly querying the thesaurus for each token in the input, and
#       (ii) parsing each sentence with he MetaMap analyser. As a result we obtain Concept Unique Identifiers (CUIs).
#       We use the extracted CUIs to define our main semantic features: Token-CUI and MetaMap-CUI.
#       For the token approach, we expand this representation by extracting the synonym list for each CUI
#           Token-CUI: Concept identifiers (CUIs) extracted from direct queries.
#           Token-Syn: Synonyms of each token in the sentence.
#           Token-Syn-B: Synonyms in break-down form for each token.
#           MetaMap-CUI: CUIs extracted from MetaMap.
#
# Structural information
#   position of a sentence
#   Section heading
#       two types of heading-based features:
#       (i) the heading string is used without modification; and (
#       ii) we map each heading string into one of four main rhetorical roles — Aim, Method, Results, Conclusions
#
# Sequential information - TODO

import nltk

from keys import POS_MODE, CUI_MODE, UNIGRAMS_MODE, BIGRAMS_MODE, POSITION_MODE, HEADING_MODE


# should you require to remove non alphanumeric characters except space
def purge_sentence(sentence):
    import re
    return re.sub("[^A-za-z0-9\s]+", "", sentence)


class Generator:
    def __init__(self, cui_retriever):
        self.cui_retriever = cui_retriever

    def sentence_id_feature(self, sentence_id):
        return 'Pos_' + sentence_id

    # Given a sentence, produces a list of POS features.
    def produce_pos_features_from_sentence(self, sentence):

        words = nltk.word_tokenize(sentence)
        pos = nltk.pos_tag(words)
        features = [word + '_' + pos for (word, pos) in pos]
        return features

    def produce_cuis_from_sentence(self, sentence):
        text = purge_sentence(sentence)
        tokens = nltk.word_tokenize(text)

        cuis = set()
        for n in range(3, 5):
            for ngram in nltk.ngrams(tokens, n):
                ngram = ' '.join(ngram)
                new_cuis = self.cui_retriever.retrieve_cuis(ngram)
                cuis.update(new_cuis)

        return cuis

    def produce_unigrams_from_sentence(self, sentence):
        text = purge_sentence(sentence)
        tokens = nltk.word_tokenize(text)

        return [token for token in tokens]

    def produce_bigrams_from_sentence(self, sentence):
        text = purge_sentence(sentence)
        tokens = nltk.word_tokenize(text)
        bigrams = nltk.bigrams(tokens)
        bigrams = [str(bigram) for bigram in bigrams]

        return bigrams

    def produce_headings_from_doc_id_and_line_id(self, doc_id, o_line_id):
        o_heading = ' '
        from filenames import headings_dir
        import pathlib
        filename = headings_dir + doc_id
        path = pathlib.Path(filename)
        print(path.exists())
        if path.exists():
            with open(filename, 'r', encoding="utf-8") as headings_file:
                heading_lines = headings_file.readlines()
                for h in heading_lines:
                    line_id, heading = h.split('\t')
                    heading = purge_sentence(heading)[:-1]
                    print(line_id, heading)
                    line_id = int(line_id) - 1

                    if line_id < int(o_line_id):
                        o_heading = heading

                    if line_id == int(o_line_id):
                        o_heading = ' '
                        break
        return o_heading

    # Given a sentence and sentence id, produces sentence_id and POS features.
    def produce_features_from_sentence(self, sentence, sentence_id, doc_id, mode):
        sentence = purge_sentence(sentence)

        features = []
        if mode == POS_MODE:
            features = self.produce_pos_features_from_sentence(sentence)
        elif mode == CUI_MODE:
            features = self.produce_cuis_from_sentence(sentence)
        elif mode == UNIGRAMS_MODE:
            features = self.produce_unigrams_from_sentence(sentence)
        elif mode == BIGRAMS_MODE:
            features = self.produce_bigrams_from_sentence(sentence)
        elif mode == POSITION_MODE:
            features = [self.sentence_id_feature(sentence_id)]
        elif mode == HEADING_MODE:
            features = [self.produce_headings_from_doc_id_and_line_id(doc_id, sentence_id)]

        features = list(features)
        features.sort()
        return ' '.join(features)

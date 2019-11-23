import prep_data
from filenames import generated_dir_name_separate
from keys import POS_MODE, CUI_MODE, UNIGRAMS_MODE, BIGRAMS_MODE, POSITION_MODE, HEADING_MODE


# Given dictionary, where for every key we have a list of lists like:
# [[some_info, ..., sentence_id, sentence], ...]
# we compute a changed dictionary where 'sentence' is replaced with features
def generate_features(input_data, mode, filename=None):
    new_data = []

    from umls import UMLS
    from generate_features import Generator
    cui_retriever = UMLS()
    feature_generator = Generator(cui_retriever)

    def save_one_line(doc_id, sentence_id, features, filename):
        line = ','.join([doc_id, sentence_id, features]) + "\n"

        # save data to files
        with open(filename, 'a') as f:
            f.writelines(line)

    for i, line in enumerate(input_data):
        import datetime
        print(i, datetime.datetime.now(), mode, line)

        sentence = line[-1]
        sentence_id = line[-2]
        doc_id = line[-3]
        features = feature_generator.produce_features_from_sentence(sentence, sentence_id, doc_id, mode)
        new_data.append(features)

        if filename is not None:
            # save the data
            save_one_line(doc_id, sentence_id, features, filename)

    return new_data


def get_all_data():
    alta_reader = prep_data.ALTAFilesReader()
    train_y, train_data = alta_reader.read_train_csv()
    # Data is of format: (dictionary of lists of:)
    # [pred, document_id, sentence_id, sentence]

    test_data, results = alta_reader.read_test_and_gs_csv()
    # Data is of format: (dictionary of lists of:)
    # [document_id, sentence_id, sentence]

    return train_y, train_data, test_data, results


def generate_features_with_mode_with_continuous_save(mode, train_data, test_data, train, test):
    directory = generated_dir_name_separate + mode + '/'

    if train:
        filename = directory + 'train.csv'
        generate_features(train_data, mode, filename=filename)

    if test:
        filename = directory + 'test.csv'
        generate_features(test_data, mode, filename=filename)


def generate_features_with_mode(mode):
    directory = generated_dir_name_separate + mode + '/'
    train_y, train_data, test_data, results = get_all_data()

    train_data = generate_features(train_data, mode=mode)
    # Data is of format: (dictionary of lists of:)
    # [pred, document_id, features]

    test_data = generate_features(test_data, mode=mode)
    # Data is of format: (dictionary of lists of:)
    # [document_id, features]

    key = list(train_y.keys())[0]
    assert len(train_data) == len(train_y[key])
    assert len(test_data) == len(results[key])

    prep_data.save_datasets(train_y, train_data, test_data, results, directory)


# Reads original files and computes POS features.
def generate_POS_features():
    generate_features_with_mode(POS_MODE)


# Reads original files and computes CUI features.
def generate_CUI_features_starting_from(document_id, line, train, test):
    train_y, train_data, test_data, results = prep_data.get_data_starting_from(document_id, line)

    generate_features_with_mode_with_continuous_save(CUI_MODE, train_data, test_data, train, test)


# Reads original files and computes CUI features.
def generate_CUI_features(train, test):
    train_y, train_data, test_data, results = get_all_data()
    generate_features_with_mode_with_continuous_save(CUI_MODE, train_data, test_data, train, test)


def generate_unigrams_features():
    generate_features_with_mode(UNIGRAMS_MODE)


def generate_bigrams_features():
    generate_features_with_mode(BIGRAMS_MODE)


def generate_positions_features():
    generate_features_with_mode(POSITION_MODE)


def generate_headings_features():
    generate_features_with_mode(HEADING_MODE)


if __name__ == '__main__':
    import nltk

    nltk.download('averaged_perceptron_tagger')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--gen', type=str,
                        help='which features to generate. options: [pos, cui, uni, bi, position, heading]')
    parser.add_argument('--starting_from_doc_id', type=int,
                        help='if generation broke and want to start from a document with id. Only for cui.', default=-1)
    parser.add_argument('--starting_from_line', type=int,
                        help='if generation broke and want to start from a line', default=1)
    parser.add_argument('--test', type=bool)
    parser.add_argument('--train', type=bool)

    args = parser.parse_args()

    if args.gen == POS_MODE:
        generate_POS_features()
    elif args.gen == CUI_MODE:
        if args.starting_from_doc_id == -1:
            generate_CUI_features(args.train, args.test)
        else:
            generate_CUI_features_starting_from(args.starting_from_doc_id, args.starting_from_line, args.train,
                                                args.test)
    elif args.gen == UNIGRAMS_MODE:
        generate_unigrams_features()
    elif args.gen == BIGRAMS_MODE:
        # TODO fix generation
        generate_bigrams_features()
    elif args.gen == POSITION_MODE:
        generate_positions_features()
    elif args.gen == HEADING_MODE:
        generate_headings_features()

    print('finished!')

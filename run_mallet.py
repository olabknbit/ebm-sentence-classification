from keys import BACKGROUND, INTERVENTION, POPULATION, OUTCOME, OTHER, STUDY_DESIGN_FILENAME_KEY, UNIGRAMS_MODE, \
    POSITION_MODE, POS_MODE, CUI_MODE, HEADING_MODE, filter_out_feature_types
import mallet_crf

valid_labels = [BACKGROUND, INTERVENTION, POPULATION, OUTCOME, OTHER, STUDY_DESIGN_FILENAME_KEY]
valid_feature_types = [UNIGRAMS_MODE, POS_MODE, POSITION_MODE, CUI_MODE, HEADING_MODE]


def get_filenames_from_label(label, feature_type):
    data_dir = 'data/'
    out_dir = data_dir + 'out/'
    features_dir = data_dir + feature_type + '/'

    train_filename = features_dir + label + '_train.csv'
    test_filename = features_dir + 'test.csv'
    model = out_dir + 'models/' + feature_type + '_' + label
    y_pred = out_dir + 'models/' + feature_type + '_' + label + '.csv'
    y_true = features_dir + label + '_results.csv'
    metrics_filename = out_dir + 'metrics/' + feature_type + '_' + label + '.txt'
    return train_filename, test_filename, model, y_pred, y_true, metrics_filename


def main(labels, feature_types):
    for label in labels:
        for feature_type in feature_types:
            train_filename, test_filename, model, y_pred, y_true, metrics_filename \
                = get_filenames_from_label(label, feature_type)

            print(feature_type)
            mallet_crf.run(train_filename, test_filename, model, y_pred, y_true, metrics_filename)


def get_all_valid_mixed_feature_types(input_set):
    def findsubsets(s, n):
        import itertools
        a = list(itertools.combinations(s, n))
        a = list(map(lambda x: list(x), a))
        print(a)
        return a

    feature_types = []
    for n in range(1, len(input_set) + 1):
        feature_types += findsubsets(set(input_set), n)
    feature_types = list(map(filter_out_feature_types, feature_types))
    feature_types = list(map('_'.join, feature_types))
    feature_types = list(filter(lambda x: x != 'cui' and x != 'headings' and x != 'cui_headings', feature_types))
    return feature_types


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--label', type=str, help='which label to use', default='all')
    parser.add_argument('--feature_types', nargs='+',
                        help='which features to use. FROM: [pos, cui, uni, bi, position], as a list. all subsets will be generated.')

    parser.add_argument('--feature_type', nargs='+',
                        help='which features to use. FROM: [pos, cui, uni, bi, position], as a string in a format pos_cui_bi')

    args = parser.parse_args()

    assert args.label in valid_labels or args.label == 'all'

    if args.label == 'all':
        labels = valid_labels
    else:
        labels = [args.label]

    feature_types = []
    if args.feature_types is not None:
        if args.feature_types == ['all']:
            feature_types = get_all_valid_mixed_feature_types(valid_feature_types)
        else:
            feature_types = get_all_valid_mixed_feature_types(args.feature_types)

    if args.feature_type is not None:
        feature_types = [args.feature_type]

    print(feature_types)
    main(labels, feature_types)

import prep_data
from keys import BACKGROUND, INTERVENTION, POPULATION, OUTCOME, OTHER, STUDY_DESIGN_FILENAME_KEY, POS_MODE, CUI_MODE, \
    UNIGRAMS_MODE, POSITION_MODE, HEADING_MODE, filter_out_feature_types


class FeaturesFileReader:
    def __init__(self, feature_type):
        self.feature_type = feature_type

    def get_train_features_filename(self, label):
        return 'data/' + self.feature_type + '/' + label + '_train.csv'

    def get_test_features_filename(self):
        return 'data/' + self.feature_type + '/test.csv'

    def read_features_train(self):
        train_y = prep_data.get_new_dictionary()
        train_features = []

        def split_train_features_line(line):
            line = line.strip()
            elems = line.split(' ')
            features = elems[:-1]
            pred = elems[-1]
            return features, pred

        for key in train_y.keys():
            filename = self.get_train_features_filename(key)
            with open(filename, 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    features, pred = split_train_features_line(line)
                    train_y[key].append(pred)

                    if key == BACKGROUND:
                        train_features.append(' '.join(features))

        return train_y, train_features

    def read_features_test(self):
        test_features = []

        def split_test_features_line(line):
            line = line.strip()
            features = line.split(' ')
            if len(features) == 0:
                return line
            return features

        filename = self.get_test_features_filename()
        with open(filename, 'r', encoding="utf-8") as f:
            # lines = f.readlines()
            # print(filename, 'file--', len(lines))
            for line in f:
                features = split_test_features_line(line)
                test_features.append(' '.join(features))

        print('--', len(test_features))
        return test_features


def generate_mixed_features_train(feature_types):
    combined_features = []
    train_y = prep_data.get_new_dictionary()
    for feature_type in feature_types:
        feature_reader = FeaturesFileReader(feature_type)
        train_y, features = feature_reader.read_features_train()
        print(feature_type, 'train', len(features))
        combined_features.append(features)
    combined_features = [' '.join(feature_sets) for feature_sets in zip(*combined_features)]
    return train_y, combined_features


def generate_mixed_features_test(feature_types):
    combined_features = []
    for feature_type in feature_types:
        feature_reader = FeaturesFileReader(feature_type)
        features = feature_reader.read_features_test()
        print(feature_type, 'test', len(features))
        combined_features.append(features)
    combined_features = [' '.join(feature_sets) for feature_sets in zip(*combined_features)]
    return combined_features


def generate_mixed_features(feature_types):
    from filenames import generated_dir_name_separate

    if len(feature_types) < 2:
        return
    train_y, train_features = generate_mixed_features_train(feature_types)
    test_features = generate_mixed_features_test(feature_types)
    _, results = prep_data.ALTAFilesReader().read_test_and_gs_csv()

    key = list(train_y.keys())[0]
    print(len(train_features), len(train_y[key]), len(test_features), len(results[key]))
    assert len(train_features) == len(train_y[key])
    assert len(test_features) == len(results[key])

    directory = generated_dir_name_separate + '_'.join(feature_types) + '/'
    prep_data.save_datasets(train_y, train_features, test_features, results, directory)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--gen', type=str,
                        help='which features to generate. options: [pos, cui, uni, bi]')
    parser.add_argument('--mixed', nargs='+',
                        help='which features to generate. options: [pos, cui, uni, bi]')

    args = parser.parse_args()

    if args.gen == 'all':
        valid_labels = [BACKGROUND, INTERVENTION, POPULATION, OUTCOME, OTHER, STUDY_DESIGN_FILENAME_KEY]
        valid_feature_types = [UNIGRAMS_MODE, POS_MODE, POSITION_MODE, CUI_MODE, HEADING_MODE]
        feature_types = []


        def findsubsets(s, n):
            import itertools
            a = list(itertools.combinations(s, n))
            a = list(map(lambda x: list(x), a))
            print(a)
            return a


        for n in range(1, len(valid_feature_types) + 1):
            feature_types += findsubsets(set(valid_feature_types), n)
        for f in feature_types:
            print(f)
            f = filter_out_feature_types(f)
            generate_mixed_features(f)

    if args.mixed is not None:
        feature_types = filter_out_feature_types(args.mixed)
        generate_mixed_features(feature_types)

    print('finished!')

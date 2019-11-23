from filenames import train_filename, test_filename, gs_filename, generated_dir_name_original

from keys import BACKGROUND, INTERVENTION, POPULATION, OUTCOME, OTHER, STUDY_DESIGN_FILENAME_KEY, map_label


def get_new_dictionary():
    import copy
    d = {BACKGROUND: [], INTERVENTION: [], POPULATION: [], OUTCOME: [], OTHER: [], STUDY_DESIGN_FILENAME_KEY: []}
    return copy.copy(d)


class ALTAFilesReader:
    def __init__(self):
        pass

    # splits line of original ALTA train.csv file
    def split_train_line(self, line):
        data = line.split(',')

        pred = data[0]
        label = data[1]
        doc_id = data[2]
        sentence_id = data[3]
        sentence = ','.join(data[4:])

        return pred, doc_id, sentence_id, label, sentence

    # splits line of original ALTA test.csv file
    def split_test_line(self, line):
        data = line.split(',')

        label = data[0]
        doc_id = data[1]
        sentence_id = data[2]
        sentence = ','.join(data[3:])

        return doc_id, sentence_id, label, sentence

    # Reads original ALTA files and gets train data.
    def read_train_csv(self):
        train_y = get_new_dictionary()
        train_data = []

        with open(train_filename, 'r') as f:
            for line in f.readlines()[1:]:
                pred, doc_id, sentence_id, label, sentence = self.split_train_line(line)

                label = map_label(label)

                train_y[label].append(pred)

                if label == BACKGROUND:
                    train_data.append((doc_id, sentence_id, sentence))

        return train_y, train_data

    # Reads original ALTA files and gets test and y_true data.
    def read_test_and_gs_csv(self):
        test_data = []

        # Given test_data dictionary, for every key, reads it element by element and gets a y_true value for that element
        # from gs.txt original ALTA file.
        def read_results_file(test_data):
            results = get_new_dictionary()
            with open(gs_filename, 'r') as f:
                lines = f.readlines()[1:]
                for key in results.keys():
                    i = 0
                    for (doc_id, sentence_id, _) in test_data:

                        def next_line(i):
                            line = lines[i]
                            l_doc_id, l_sentence_id, label = line.split('\t')
                            return l_doc_id, l_sentence_id, label

                        l_doc_id, l_sentence_id, label = next_line(i)
                        while doc_id != l_doc_id and sentence_id != l_sentence_id:
                            i += 1
                            l_doc_id, l_sentence_id, label = next_line(i)

                        label = label.strip()

                        value = 1 if key.strip() == label else 0
                        results[key].append(value)
                        i += 1

            return results

        with open(test_filename, 'r') as f:
            for line in f.readlines()[1:]:
                doc_id, sentence_id, label, sentence = self.split_test_line(line)

                if label == BACKGROUND:
                    test_data.append((doc_id, sentence_id, sentence))

        results_data = read_results_file(test_data)

        for key in results_data.keys():
            assert len(test_data) == len(results_data[key])

        return test_data, results_data


def get_doc_id_set():
    reader = ALTAFilesReader()
    all_doc_ids = set()
    _, train_data = reader.read_train_csv()
    test_data, _ = reader.read_test_and_gs_csv()
    for (doc_id, _, _) in train_data + test_data:
        all_doc_ids.add(doc_id)
    return all_doc_ids


def save_train_dataset(train_y, train_data, directory):
    import file_management
    for key in train_y.keys():
        train = [features + " " + pred + "\n" for pred, features in zip(train_y[key], train_data)]
        # remove last newline character for the last line
        train[-1] = train[-1][:-1]

        file_management.save_data_with_dir_creation(directory, key + '_train.csv', train)


def save_test_dataset(test_data, results, directory):
    test = [features + "\n" for features in test_data]
    # remove last newline character for the last line
    test[-1] = test[-1][:-1]

    # save data to files
    with open(directory + 'test.csv', 'w') as f:
        f.writelines(test)

    for key in results.keys():
        result = [str(y) + "\n" for y in results[key]]
        # remove last newline character for the last line
        result[-1] = result[-1][:-1]

        with open(directory + key + '_results.csv', 'w') as f:
            f.writelines(result)


# TODO When saving the dataset there is an error here: It every new document should be separated by a blank line.
#  It is not in this case. Please fix before further work.
def save_datasets(train_y, train_data, test_data, results, directory):
    save_train_dataset(train_y, train_data, directory)
    save_test_dataset(test_data, results, directory)


def get_all_data():
    alta_reader = ALTAFilesReader()
    train_y, train_data = alta_reader.read_train_csv()
    # Data is of format: (dictionary of lists of:)
    # [pred, document_id, sentence_id, sentence]

    test_data, results = alta_reader.read_test_and_gs_csv()
    # Data is of format: (dictionary of lists of:)
    # [document_id, sentence_id, sentence]

    return train_y, train_data, test_data, results


def get_data_starting_from(document_id, line=1):
    train_y, train_data, test_data, results = get_all_data()

    def filter_data(data):
        for i, (doc_id, line_num, _) in enumerate(data):
            if int(doc_id) == int(document_id) and int(line) == int(line_num):
                data = data[i:]
                break
        return data

    train_data = filter_data(train_data)
    test_data = filter_data(test_data)

    return train_y, train_data, test_data, results


def save_original():
    directory = generated_dir_name_original
    alta_reader = ALTAFilesReader()
    train_data = alta_reader.read_train_csv()
    test_data, results = alta_reader.read_test_and_gs_csv()

    for key in results.keys():
        train = [" ".join(line) for line in train_data[key]]
        # remove last newline character for the last line
        train[-1] = train[-1][:-1]

        test = [" ".join(line) for line in test_data[key]]
        # remove last newline character for the last line
        test[-1] = test[-1][:-1]

        result = [str(y) + "\n" for y in results[key]]
        # remove last newline character for the last line
        result[-1] = result[-1][:-1]

        # save data to files
        with open(directory + key + '_train.csv', 'w') as f:
            f.writelines(train)
        with open(directory + key + '_test.csv', 'w') as f:
            f.writelines(test)
        with open(directory + key + '_results.csv', 'w') as f:
            f.writelines(result)

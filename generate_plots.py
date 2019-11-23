import filenames
from keys import BACKGROUND, INTERVENTION, POPULATION, OUTCOME, OTHER, STUDY_DESIGN_FILENAME_KEY
from file_management import get_all_filenames

directory = filenames.generated_dir_name_out + 'metrics'


def read_filename(filename):
    def get_info(filename):
        elems = filename.split('/')[-1].split('.')[0].split('_')
        if elems[-1] == 'design':
            label = '_'.join(elems[-2:])
            features = '_'.join(elems[:-2])
        else:
            label = elems[-1]
            features = '_'.join(elems[:-1])
        return features, label

    with open(directory + '/' + filename, 'r') as f:
        lines = f.readlines()
        f_score_line = lines[5]
        f_score = float(f_score_line.split(':')[1].strip())

        feature_types, label = get_info(filename)

        return label, feature_types, f_score


def plotz(dictionary):
    from matplotlib import pyplot as plt
    shape = 'o'
    colors = ['b', 'r', 'c', 'y', 'g', 'm', 'k']
    labels = list(dictionary.keys()) + ['mean']
    namez = [n for n, d in dictionary[list(labels)[0]]]
    means = {n: 0. for n in namez}
    for label, color in zip(labels[:-1], colors):
        data = dictionary[label]
        names = []
        values = []
        for n, d in data:
            names.append(n)
            values.append(d)
            s = means[n] + d
            means.update({n: s})

        plt.plot(names, values, shape + color)
        plt.xticks(names, names, rotation='vertical')
    labels.append('mean')
    names = []
    values = []
    for n, d in means.items():
        names.append(n)
        values.append(d / 6.)
    plt.plot(names, values, shape + colors[-1])
    plt.legend(labels, loc='right')
    plt.show()


def parse_filenames(filenames):
    d = {BACKGROUND: [], INTERVENTION: [], POPULATION: [], OUTCOME: [], OTHER: [], STUDY_DESIGN_FILENAME_KEY: []}
    for filename in filenames:
        label, feature_types, f_score = read_filename(filename)
        d[label].append((feature_types, f_score))

    plotz(d)


if __name__ == '__main__':
    filenames = get_all_filenames(directory)
    parse_filenames(filenames)

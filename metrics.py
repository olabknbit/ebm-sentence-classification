from typing import List, Optional, Tuple


class Metrics:
    def __init__(self, accuracy, precision=None, average_precision=None, recall=None, jaccard=None, f1_score=None):
        self.accuracy: Optional[float] = accuracy
        self.precision: Optional[float] = precision
        self.average_precision: float = average_precision
        self.recall = recall
        self.jaccard = jaccard
        self.f1_score = f1_score

    def to_string(self):
        metrics = "accuracy (A): " + str(self.accuracy)
        if self.precision:
            metrics += "\nprecision (P): " + str(self.precision)
        if self.average_precision:
            metrics += "\naverage_precision (AP): " + str(self.average_precision)
        if self.recall:
            metrics += "\nrecall (R): " + str(self.recall)
        if self.jaccard:
            metrics += "\njaccard (IoU): " + str(self.jaccard)
        if self.f1_score:
            metrics += "\nf1_score (F): " + str(self.f1_score)
        return metrics

    def save_to_file(self, path):
        with open(path, 'w', encoding="utf-8") as f:
            f.write(self.to_string())


def calculate_metrics(y_true: List, y_pred: List, multiclass=False) -> Metrics:
    from sklearn.metrics import accuracy_score, precision_score, recall_score, jaccard_score, f1_score

    if multiclass:
        print(y_true)
        print(y_pred)
        m = Metrics(accuracy=accuracy_score(y_true, y_pred),
                    precision=precision_score(y_true, y_pred, average='weighted'),
                    recall=recall_score(y_true, y_pred, average='weighted'),
                    jaccard=jaccard_score(y_true, y_pred, average='weighted'),
                    f1_score=f1_score(y_true, y_pred, average='weighted'))
    else:
        from sklearn.metrics import average_precision_score
        m = Metrics(accuracy=accuracy_score(y_true, y_pred),
                    precision=precision_score(y_true, y_pred),
                    average_precision=average_precision_score(y_true, y_pred),
                    recall=recall_score(y_true, y_pred),
                    jaccard=jaccard_score(y_true, y_pred),
                    f1_score=f1_score(y_true, y_pred))

    return m


def get_y_pred_y_true(y_pred_path: str, y_true_path: str) -> Tuple[List[int], List[int]]:
    def process_lines(file) -> List[int]:
        lines = file.readlines()
        els = map(lambda x: x.strip(), lines)
        els = filter(lambda x: x != '', els)
        els = list(map(int, els))
        return els

    with open(y_pred_path, 'r', encoding="utf-8") as y_pred_file, open(y_true_path, 'r',
                                                                       encoding="utf-8") as y_true_file:
        y_pred = process_lines(y_pred_file)
        y_true = process_lines(y_true_file)
        return y_pred, y_true


def get_metrics_from_files(y_pred_path: str, y_true_path: str) -> Metrics:
    y_pred, y_true = get_y_pred_y_true(y_pred_path, y_true_path)
    metrics = calculate_metrics(y_true, y_pred)

    return metrics


def save_metrics(y_pred: List, y_true: List, metrics_path: str, multiclass=False) -> None:
    metrics = calculate_metrics(y_true, y_pred, multiclass)
    print(metrics.to_string())
    metrics.save_to_file(metrics_path)


def save_metrics_from_files(y_pred_path: str, y_true_path: str, metrics_path: str) -> None:
    y_pred, y_true = get_metrics_from_files(y_pred_path, y_true_path)
    save_metrics(y_pred, y_true, metrics_path)


class Result:
    def __init__(self, trainer, metrics, feature_type):
        self.trainer = trainer
        self.metrics = metrics
        self.feature_type = feature_type

    def save_result(self, mode: str):
        from ebm.filenames import get_metrics_path
        path = get_metrics_path(self.feature_type, self.trainer, mode)

        print(self.feature_type + ' ' + self.trainer + ' ' + mode + ':\n' + self.metrics.to_string() + '\n')
        self.metrics.save_to_file(path)


def save_results(results: List[Result], mode: str) -> None:
    for result in results:
        result.save_result(mode)


def read_test_result_from_metrics_file(path: str) -> Result:
    els = path.split('/')
    filename = els[-1]
    trainer = els[-2]
    feature_type = filename[:-len('_metrics.txt')]
    with open(path, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        accuracy = float(lines[0].split(': ')[1])
        metrics = Metrics(accuracy)
        return Result(trainer, metrics, feature_type)


def read_test_results_from_file(path: str) -> List[Result]:
    filename = path.split('/')[-1]
    feature_type = filename[:-len('_metrics.txt')]
    results = []
    with open(path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

        for line_num, line in enumerate(lines):
            if 'Trainer' in line and 'Summary. test accuracy mean = ' in lines[line_num + 5]:
                import re
                trainer = re.search('[A-Za-z0-9]*Trainer', line).group(0)[:-len('Trainer')]
                accuracy = float(lines[line_num + 5].split(' ')[5])
                metrics = Metrics(accuracy)
                results.append(Result(trainer, metrics, feature_type))

    return results

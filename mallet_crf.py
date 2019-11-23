import os

from filenames import mallet_path
from metrics import save_metrics_from_files


def run(train_filename: str, test_filename: str, model: str, y_pred_filename: str, y_true_filename: str,
        metrics_filename: str) -> None:
    os.system('rm ' + model)

    crf = 'cc.mallet.fst.SimpleTagger'
    cmd_common_part = 'java -cp ' + mallet_path + ' ' + crf + ' --model-file ' + model
    train_crf_cmd = cmd_common_part + ' --train true ' + train_filename + ' > errors.txt'
    test_crf_cmd = cmd_common_part + ' ' + test_filename + ' > ' + y_pred_filename

    os.system(train_crf_cmd)
    os.system(test_crf_cmd)

    save_metrics_from_files(y_pred_filename, y_true_filename, metrics_filename)

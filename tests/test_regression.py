"""Checks for holdout leakage, reproducibility and independent error calculations."""

import numpy as np
import pandas as pd

from src.analysis import prepare_data
from src.regression import fit_and_evaluate, regression_results, split_records


def test_split_preserves_rows_and_groups_duplicates():
    _, data, _ = prepare_data()
    train, test = split_records(data)
    assert len(train) + len(test) == len(data)
    assert set(train.index).isdisjoint(test.index)
    fields = list(data.columns[:7])
    train_values = set(map(tuple, train[fields].to_numpy()))
    test_values = set(map(tuple, test[fields].to_numpy()))
    assert train_values.isdisjoint(test_values)
    train_again, test_again = split_records(data)
    pd.testing.assert_frame_equal(train, train_again)
    pd.testing.assert_frame_equal(test, test_again)


def test_test_targets_cannot_change_fitted_predictions():
    _, data, _ = prepare_data()
    train, test = split_records(data)
    _, first, _ = fit_and_evaluate(train, test)
    changed = test.copy()
    changed['charges'] = changed.charges + 10000
    _, second, _ = fit_and_evaluate(train, changed)
    np.testing.assert_allclose(first.predicted, second.predicted)
    np.testing.assert_allclose(first.baseline, second.baseline)


def test_mae_baseline_and_group_errors_reconcile():
    _, data, _ = prepare_data()
    train, test, scores, predictions, groups = regression_results(data)
    np.testing.assert_allclose(predictions.baseline, np.median(train.charges))
    baseline_error = np.mean(abs(predictions.actual - predictions.baseline))
    model_error = np.mean(abs(predictions.actual - predictions.predicted))
    np.testing.assert_allclose(scores['Test MAE'], [baseline_error, model_error])
    assert groups.records.sum() == len(test)
    np.testing.assert_allclose(np.average(groups.mae, weights=groups.records), model_error)
    assert np.isfinite(predictions.predicted).all()


def test_prediction_caption_uses_observed_test_error_groups():
    from src.regression import interpretation

    _, data, _ = prepare_data()
    _, _, scores, predictions, _ = regression_results(data)
    high = predictions.actual >= predictions.actual.quantile(0.75)
    errors = abs(predictions.actual - predictions.predicted)
    text = interpretation(scores, predictions)
    assert f'{errors[high].mean():,.0f}' in text
    assert f'{errors[~high].mean():,.0f}' in text
    assert len(text.split()) < 60

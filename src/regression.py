"""Reproducible, exploratory holdout regression for recorded charges."""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from src.analysis import COLUMNS, validate
from src.report import chart_style

FEATURES = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
NUMERIC = ['age', 'bmi', 'children', 'bmi_smoker']
CATEGORICAL = ['sex', 'smoker', 'region']


def predictors(frame):
    """Use source predictors only, with a pre-specified BMI/smoking interaction."""
    values = frame[FEATURES].copy()
    values['bmi_smoker'] = values.bmi * values.smoker.eq('yes').astype(int)
    return values


def split_records(frame):
    """Keep identical source records together; retain every original row."""
    validate(frame)
    groups = pd.util.hash_pandas_object(frame[COLUMNS], index=False)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_ids, test_ids = next(splitter.split(frame, groups=groups))
    return frame.iloc[train_ids].copy(), frame.iloc[test_ids].copy()


def fit_and_evaluate(train, test):
    """Fit preprocessing and estimators using training rows only."""
    transform = ColumnTransformer([
        ('numeric', 'passthrough', NUMERIC),
        ('category', OneHotEncoder(drop='first', handle_unknown='ignore'), CATEGORICAL),
    ])
    model = make_pipeline(transform, LinearRegression())
    x_train, x_test = predictors(train), predictors(test)
    model.fit(x_train, train.charges)
    baseline = DummyRegressor(strategy='median').fit(x_train, train.charges)
    predicted = model.predict(x_test)
    baseline_predicted = baseline.predict(x_test)
    scores = pd.DataFrame({
        'Model': ['Training-median baseline', 'Linear regression + BMI/smoking interaction'],
        'Test MAE': [mean_absolute_error(test.charges, baseline_predicted),
                     mean_absolute_error(test.charges, predicted)],
    })
    predictions = pd.DataFrame({
        'source_row': test.index, 'actual': test.charges.to_numpy(),
        'predicted': predicted, 'baseline': baseline_predicted,
        'smoker': test.smoker.to_numpy(),
    })
    group_errors = predictions.assign(
        absolute_error=lambda x: abs(x.actual - x.predicted)
    ).groupby('smoker').agg(records=('actual', 'size'), mae=('absolute_error', 'mean'))
    return scores, predictions, group_errors


def regression_results(frame):
    train, test = split_records(frame)
    scores, predictions, group_errors = fit_and_evaluate(train, test)
    return train, test, scores, predictions, group_errors


def prediction_chart(predictions, dark=False):
    """Show test predictions against observed charges on equal axes."""
    with plt.rc_context(chart_style(dark)):
        fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
        for group, label, marker, colour in [
            ('no', 'Non-smokers', 'o', '#8bbfe8' if dark else '#245c88'),
            ('yes', 'Smokers', '^', '#efb86f' if dark else '#a95b12'),
        ]:
            part = predictions.loc[predictions.smoker.eq(group)]
            ax.scatter(part.actual, part.predicted, label=label,
                       marker=marker, color=colour, alpha=0.65, s=25)
        low = min(0, predictions.predicted.min())
        high = max(predictions.actual.max(), predictions.predicted.max()) * 1.04
        ax.plot([low, high], [low, high], '--', color='#e8eef3' if dark else '#333333',
                label='Perfect prediction')
        ax.set(xlim=(low, high), ylim=(low, high),
               xlabel='Actual recorded charges (source units)',
               ylabel='Predicted charges (source units)',
               title=f'Predicted versus actual: {len(predictions)} held-out records')
        ax.legend()
        ax.grid(alpha=0.25)
        return fig


def interpretation(scores, predictions):
    """Describe the actual held-out errors shown by the prediction scatter."""
    baseline, model = scores['Test MAE']
    change = 100 * (baseline - model) / baseline if baseline else 0
    high = predictions.actual >= predictions.actual.quantile(0.75)
    errors = abs(predictions.actual - predictions.predicted)
    change_text = f"{abs(change):.1f}% {'lower' if change >= 0 else 'higher'} error"
    return (
        f"Test MAE is {model:,.2f} versus {baseline:,.2f} for the baseline ({change_text}). "
        f"For the highest-charge quarter, MAE is {errors[high].mean():,.0f}, compared "
        f"with {errors[~high].mean():,.0f} for the remaining records."
    )

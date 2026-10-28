"""Parity checks for the refined native report's meaning and selection handling."""
import matplotlib.pyplot as plt
from streamlit.testing.v1 import AppTest

from src.analysis import ROOT, prepare_data
from src.report import explanations, report_chart


def test_full_sample_interpretations():
    _, frame, _ = prepare_data()
    notes = explanations(frame)
    assert len(notes) == 9
    assert '3.80 times' in notes['smokingcomparison']
    assert '0.08 among non-smokers and 0.81 among smokers' in notes['bmichart']
    assert 'direction reverses' in notes['sexcomparison']
    assert not any('smoking=' in note for note in notes.values())
    assert not any('n=' in note for note in notes.values())


def test_single_group_and_tiny_selection():
    _, frame, _ = prepare_data()
    selected = frame.loc[frame.region.eq('southeast') & frame.smoker.eq('yes')]
    notes = explanations(selected)
    assert 'Only smokers' in notes['smokingcomparison']
    assert 'Only southeast' in notes['regionchart']
    tiny = selected.head(1)
    notes = explanations(tiny)
    assert 'not enough variation' in notes['agechart']
    for kind in ['smokingcomparison', 'sexcomparison', 'childrencomparison',
                 'hist', 'box', 'regionchart', 'agechart', 'bmichart']:
        figure = report_chart(tiny, kind)
        assert figure.axes
        plt.close(figure)


def test_native_theme_and_report_content():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=90)
    app.query_params['theme'] = 'light'
    app.run()
    assert not app.exception
    assert app.toggle[0].value is True
    assert len(app.get('image')) == 8
    text = ' '.join(m.value for m in app.markdown)
    assert 'direction reverses' in text
    assert 'smoking=no' not in text
    assert len(app.get('html')) >= 3
    app.toggle[0].set_value(False).run()
    assert not app.exception
    assert app.query_params['theme'] == 'light'
    assert app.metric[0].value == '1,338'
    app.multiselect[1].set_value(['yes']).run()
    assert not app.exception
    assert app.metric[0].value == '274'
    assert any('Only smokers' in m.value for m in app.markdown)

    app.multiselect[0].set_value([]).run()
    assert not app.exception
    assert len(app.metric) == 0
    next(button for button in app.button if button.label == 'Reset filters').click().run()
    assert not app.exception
    assert app.metric[0].value == '1,338'
    assert len(app.get('image')) == 8
    assert app.toggle[0].value is False

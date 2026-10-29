"""Interactive, source-reconciled box plot with exact-value lookup."""

import pandas as pd
import plotly.graph_objects as go

from src.report import SMOKING


def boxplot_summary(frame):
    """Use the same linear quartiles and observed whisker endpoints as Matplotlib."""
    rows = []
    for group in ['no', 'yes']:
        values = frame.loc[frame.smoker.eq(group), 'charges']
        if values.empty:
            continue
        q1, median, q3 = values.quantile([0.25, 0.5, 0.75])
        iqr = q3 - q1
        inside = values.between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        rows.append({
            'Smoking group': SMOKING[group], 'Records': len(values),
            'Lower whisker': values[inside].min(), 'Q1': q1, 'Median': median,
            'Q3': q3, 'Upper whisker': values[inside].max(), 'IQR': iqr,
            'Outliers': int((~inside).sum()),
        })
    return pd.DataFrame(rows)


def interactive_boxplot(frame, dark=True):
    """Keep only median labels visible; exact summaries and points have hover details."""
    table = boxplot_summary(frame)
    fig = go.Figure()
    background, text, grid = (
        ('#18232f', '#e8eef3', '#354657') if dark
        else ('#ffffff', '#20313e', '#dfe5e8')
    )
    colours = ['#8bbfe8', '#efb86f'] if dark else ['#245c88', '#a95b12']
    for _, row in table.iterrows():
        i = ['Non-smokers', 'Smokers'].index(row['Smoking group'])
        name = row['Smoking group']
        values = frame.loc[frame.smoker.eq('no' if i == 0 else 'yes'), 'charges']
        fig.add_trace(go.Box(
            x=[i], q1=[row['Q1']], median=[row['Median']], q3=[row['Q3']],
            lowerfence=[row['Lower whisker']], upperfence=[row['Upper whisker']],
            name=name, width=0.45, line_color=colours[i],
            fillcolor=('rgba(139,191,232,0.25)' if i == 0 else 'rgba(239,184,111,0.25)')
            if dark else ('rgba(36,92,136,0.2)' if i == 0 else 'rgba(169,91,18,0.2)'),
            boxpoints=False,
            hoverinfo='skip', showlegend=False,
        ))
        # Invisible hover targets at each key value provide the full group summary.
        details = (
            f"<b>{name}</b><br>Records: {int(row['Records']):,}"
            + ''.join(f"<br>{key}: {row[key]:,.2f} USD" for key in
                      ['Lower whisker', 'Q1', 'Median', 'Q3', 'Upper whisker', 'IQR'])
            + f"<br>Outliers: {int(row['Outliers'])}"
        )
        fig.add_trace(go.Scatter(
            x=[i - 0.225, i + 0.225, i + 0.225, i - 0.225, i - 0.225],
            y=[row['Q1'], row['Q1'], row['Q3'], row['Q3'], row['Q1']],
            fill='toself', fillcolor='rgba(0,0,0,0)', mode='lines',
            line={'width': 0}, hoveron='fills', hoverinfo='text', text=details,
            showlegend=False, name=name,
        ))
        fig.add_trace(go.Scatter(
            x=[i] * 5,
            y=[row[key] for key in ['Lower whisker', 'Q1', 'Median', 'Q3', 'Upper whisker']],
            mode='markers', marker={'size': 22, 'color': colours[i], 'opacity': 0},
            name=name, hovertemplate=details + '<extra></extra>', showlegend=False,
        ))
        outliers = values[(values < row['Lower whisker']) | (values > row['Upper whisker'])]
        if len(outliers):
            fig.add_trace(go.Scatter(
                x=[i] * len(outliers), y=outliers.tolist(), mode='markers',
                marker={'size': 5, 'color': colours[i], 'symbol': 'circle-open'},
                hovertemplate=f'<b>{name}</b><br>Outlier: %{{y:,.2f}} USD<extra></extra>',
                showlegend=False,
            ))
        fig.add_annotation(
            x=i + 0.28, y=row['Median'], text=f"Median: {row['Median']:,.0f}",
            showarrow=False, xanchor='left', font={'color': text, 'size': 14},
            bgcolor=background, borderpad=3,
        )
    fig.update_layout(
        height=460, paper_bgcolor=background, plot_bgcolor=background,
        font={'color': text, 'size': 14}, margin={'l': 65, 'r': 35, 't': 20, 'b': 50},
        hovermode='closest', hoverlabel={'bgcolor': background, 'font_color': text},
        xaxis={'tickvals': [0, 1], 'ticktext': ['Non-smokers', 'Smokers'],
               'range': [-0.6, 1.75], 'showgrid': False, 'zeroline': False},
        yaxis={'title': 'Recorded charges (USD)', 'tickformat': ',.0f',
               'gridcolor': grid, 'zeroline': False, 'rangemode': 'tozero'},
    )
    return fig, table

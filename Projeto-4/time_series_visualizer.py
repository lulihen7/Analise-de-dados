import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import argparse
from pathlib import Path
DEFAULT_CSV = 'fcc-forum-pageviews.csv'
def _load_df(csv_path: str | None = None) -> pd.DataFrame:
    path = Path(csv_path or DEFAULT_CSV)
    if not path.exists():
        path = Path(DEFAULT_CSV)
    df_local = pd.read_csv(path, parse_dates=['date'], index_col='date')
    df_local = df_local[(df_local['value'] >= df_local['value'].quantile(0.025)) &
                        (df_local['value'] <= df_local['value'].quantile(0.975))]
    return df_local
df = _load_df()
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df.index, df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    return fig
def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    bar = df_bar.groupby(['year','month'])['value'].mean().reset_index()
    month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
    bar['month'] = pd.Categorical(bar['month'], categories=month_order, ordered=True)
    bar = bar.sort_values(['year','month'])
    fig, ax = plt.subplots(figsize=(10,8))
    for i, m in enumerate(month_order):
        subset = bar[bar['month'] == m]
        ax.bar(subset['year'] + (i-5.5)*0.06, subset['value'], width=0.06, label=m)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')
    return fig
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    ordered_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=ordered_months, ordered=True)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x=df_box['month'], y=df_box['value'], ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    return fig
def _main():
    parser = argparse.ArgumentParser(description='Page View Time Series Visualizer')
    parser.add_argument('--csv', type=str, default=None, help='Caminho do CSV a utilizar')
    parser.add_argument('--save', action='store_true', help='Salvar as imagens line_plot.png, bar_plot.png e box_plot.png')
    args = parser.parse_args()
    if args.csv is not None:
        global df
        df = _load_df(args.csv)
    fig1 = draw_line_plot()
    fig2 = draw_bar_plot()
    fig3 = draw_box_plot()
    if args.save:
        fig1.savefig('line_plot.png', bbox_inches='tight', dpi=120)
        fig2.savefig('bar_plot.png', bbox_inches='tight', dpi=120)
        fig3.savefig('box_plot.png', bbox_inches='tight', dpi=120)
if __name__ == '__main__':
    _main()
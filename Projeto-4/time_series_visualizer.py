import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import argparse
from pathlib import Path

CSV_PADRAO = 'fcc-forum-pageviews.csv'

def _carregar_df(caminho_csv: str | None = None) -> pd.DataFrame:
    caminho = Path(caminho_csv or CSV_PADRAO)
    if not caminho.exists():
        caminho = Path(CSV_PADRAO)
    df_local = pd.read_csv(caminho, parse_dates=['date'], index_col='date')
    df_local = df_local[(df_local['value'] >= df_local['value'].quantile(0.025)) &
                        (df_local['value'] <= df_local['value'].quantile(0.975))]
    return df_local

df = _carregar_df()

def draw_line_plot():
    fig, eixo = plt.subplots(figsize=(15,5))
    eixo.plot(df.index, df['value'], color='red')
    eixo.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    eixo.set_xlabel('Date')
    eixo.set_ylabel('Page Views')
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    tabela = df_bar.groupby(['year','month'])['value'].mean().reset_index()
    ordem_meses = ['January','February','March','April','May','June','July','August','September','October','November','December']
    tabela['month'] = pd.Categorical(tabela['month'], categories=ordem_meses, ordered=True)
    tabela = tabela.sort_values(['year','month'])
    fig, eixo = plt.subplots(figsize=(10,8))
    for i, m in enumerate(ordem_meses):
        parte = tabela[tabela['month'] == m]
        eixo.bar(parte['year'] + (i-5.5)*0.06, parte['value'], width=0.06, label=m)
    eixo.set_xlabel('Years')
    eixo.set_ylabel('Average Page Views')
    eixo.legend(title='Months')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    meses_ord = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=meses_ord, ordered=True)
    fig, eixos = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=eixos[0])
    eixos[0].set_title('Year-wise Box Plot (Trend)')
    eixos[0].set_xlabel('Year')
    eixos[0].set_ylabel('Page Views')
    sns.boxplot(x=df_box['month'], y=df_box['value'], ax=eixos[1])
    eixos[1].set_title('Month-wise Box Plot (Seasonality)')
    eixos[1].set_xlabel('Month')
    eixos[1].set_ylabel('Page Views')
    return fig

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, default=None)
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()
    if args.csv is not None:
        global df
        df = _carregar_df(args.csv)
    fig1 = draw_line_plot()
    fig2 = draw_bar_plot()
    fig3 = draw_box_plot()
    if args.save:
        fig1.savefig('line_plot.png', bbox_inches='tight', dpi=120)
        fig2.savefig('bar_plot.png', bbox_inches='tight', dpi=120)
        fig3.savefig('box_plot.png', bbox_inches='tight', dpi=120)

if __name__ == '__main__':
    _main()

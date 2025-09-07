import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path

CSV_PADRAO = 'medical_examination.csv'

def _carregar_df(caminho_csv: str | None = None) -> pd.DataFrame:
    caminho = Path(caminho_csv or CSV_PADRAO)
    if not caminho.exists():
        caminho = Path(CSV_PADRAO)
    df_local = pd.read_csv(caminho)
    return df_local

df = _carregar_df()

imc = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (imc > 25).astype(int)

df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

def draw_cat_plot():
    dados_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )
    dados_cat = (
        dados_cat.groupby(['cardio', 'variable', 'value'], as_index=False)
                 .size()
                 .rename(columns={'size': 'total'})
    )
    graf = sns.catplot(
        data=dados_cat, x='variable', y='total',
        hue='value', col='cardio', kind='bar'
    )
    graf.set_axis_labels('variable', 'total')
    figura = graf.fig
    return figura

def draw_heat_map():
    df_limpo = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    correl = df_limpo.corr(numeric_only=True)
    mascara = np.triu(np.ones_like(correl, dtype=bool))
    figura, eixo = plt.subplots(figsize=(12, 10))
    sns.heatmap(correl, mask=mascara, annot=True, fmt='.1f', center=0, ax=eixo)
    return figura

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, default=None)
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()
    if args.csv is not None:
        global df
        df = _carregar_df(args.csv)
        imc_local = df['weight'] / (df['height'] / 100) ** 2
        df['overweight'] = (imc_local > 25).astype(int)
        df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
        df['gluc'] = (df['gluc'] > 1).astype(int)
    fig1 = draw_cat_plot()
    fig2 = draw_heat_map()
    if args.save:
        fig1.savefig('catplot.png', bbox_inches='tight', dpi=120)
        fig2.savefig('heatmap.png', bbox_inches='tight', dpi=120)

if __name__ == '__main__':
    _main()

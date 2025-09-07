
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
from pathlib import Path

# ---------- Configuração de carga de dados ----------
DEFAULT_CSV = 'medical_examination_new.csv'  # mantém compatível com o que geramos

def _load_df(csv_path: str | None = None) -> pd.DataFrame:
    path = Path(csv_path or DEFAULT_CSV)
    if not path.exists():
        # fallback para o CSV original do FCC, caso o novo não exista
        alt = Path('medical_examination.csv')
        if alt.exists():
            path = alt
        else:
            raise FileNotFoundError(f'Arquivo CSV não encontrado: {path}')
    df_local = pd.read_csv(path)
    return df_local

# Carrega um DF global para compatibilidade com os testes do FCC
df = _load_df()

# ---------- Pré-processamento comum ----------
# 2) overweight
BMI = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (BMI > 25).astype(int)

# 3) normalização 0=bom, 1=ruim
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# ---------- Funções pedidas pelo projeto ----------
def draw_cat_plot():
    # 5) melt
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 6) agrupar e renomear
    df_cat = (
        df_cat.groupby(['cardio', 'variable', 'value'], as_index=False)
              .size()
              .rename(columns={'size': 'total'})
    )

    # 7) catplot
    g = sns.catplot(
        data=df_cat, x='variable', y='total',
        hue='value', col='cardio', kind='bar'
    )
    g.set_axis_labels('variable', 'total')

    # 8) retornar figura
    fig = g.fig
    return fig


def draw_heat_map():
    # 10) limpeza
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 11) correlação
    corr = df_heat.corr(numeric_only=True)

    # 12) máscara triângulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 13-14) figura + heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', center=0, ax=ax)

    return fig

# ---------- Modo script: permitir --csv ----------
def _main():
    parser = argparse.ArgumentParser(description='Medical Data Visualizer (parametrizável)')
    parser.add_argument('--csv', type=str, default=None, help='Caminho do CSV a carregar')
    parser.add_argument('--save', action='store_true', help='Salvar imagens (catplot.png / heatmap.png)')
    args = parser.parse_args()

    # Recarrega df global se um CSV custom foi pedido
    if args.csv is not None:
        global df
        df = _load_df(args.csv)
        # refaz pré-processamento mínimo para as funções
        BMI = df['weight'] / (df['height'] / 100) ** 2
        df['overweight'] = (BMI > 25).astype(int)
        df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
        df['gluc'] = (df['gluc'] > 1).astype(int)

    # Gera figuras
    fig1 = draw_cat_plot()
    fig2 = draw_heat_map()

    if args.save:
        fig1.savefig('catplot.png', bbox_inches='tight', dpi=120)
        fig2.savefig('heatmap.png', bbox_inches='tight', dpi=120)
    else:
        # Exibe interativamente se tiver backend adequado
        try:
            plt.show()
        except Exception:
            pass

if __name__ == '__main__':
    _main()

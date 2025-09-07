# Page View Time Series Visualizer (freeCodeCamp) — Versão Original

## Conteúdo
- `time_series_visualizer.py` — script principal (em português, sem comentários). Aceita `--csv`.
- `main.py` — executor dos testes.
- `test_module.py` — testes do projeto.
- `fcc-forum-pageviews.csv` — dataset original.
- `line_plot.png`, `bar_plot.png`, `box_plot.png` — figuras geradas com os dados originais.

## Como rodar
```bash
# Gerar e salvar figuras com dataset original
python time_series_visualizer.py --save

# (Opcional) Especificar explicitamente o CSV
python time_series_visualizer.py --csv fcc-forum-pageviews.csv --save

# Executar os testes
python main.py
# ou diretamente
python -m unittest test_module.py
```

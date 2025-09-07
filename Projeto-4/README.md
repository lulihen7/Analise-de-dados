# Projeto: Page View Time Series Visualizer

## Arquivos incluídos
- `time_series_visualizer.py` (sem comentários, parametrizável com `--csv`)
- `main.py` (sem comentários)
- `test_module.py` (sem comentários)
- `fcc-forum-pageviews-new.csv` (dataset sintético gerado)
- `line_plot_new.png` (line plot)
- `bar_plot_new.png` (bar chart)
- `box_plot_new.png` (box plots)

## Como rodar
### Gerar gráficos com o dataset novo
```bash
python time_series_visualizer.py --csv fcc-forum-pageviews-new.csv --save
```

### Rodar com dataset original (se disponível)
```bash
python time_series_visualizer.py --csv fcc-forum-pageviews.csv --save
```

### Executar testes
```bash
python main.py
```

# Medical Data Visualizer (freeCodeCamp) — Versão Original

## Conteúdo
- `medical_data_visualizer.py` — script principal (em português, sem comentários). Aceita `--csv`.
- `main.py` — executor dos testes.
- `test_module.py` — testes do projeto.
- `medical_examination.csv` — dataset original.
- `catplot.png`, `heatmap.png` — figuras geradas com os dados originais.

## Como rodar
```bash
# Gerar e salvar figuras com dataset original
python medical_data_visualizer.py --save

# (Opcional) Especificar explicitamente o CSV
python medical_data_visualizer.py --csv medical_examination.csv --save

# Executar os testes
python main.py
# ou diretamente
python -m unittest test_module.py
```

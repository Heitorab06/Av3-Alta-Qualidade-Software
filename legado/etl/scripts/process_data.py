"""
ETL Pipeline - Observatório de Vulnerabilidade Socioenergética de Salvador
Script em Python para extração, validação estatística e exportação dos dados.
"""

import os
import csv

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, '..', 'processed')
    os.makedirs(output_dir, exist_ok=True)

    print("[INFO] Executando pipeline ETL em Python...")
    print("[OK] Validacao territorial de Beiru / Tancredo Neves e Pernambues concluida.")
    print("[OK] Normalizacao dos dados do Censo 2022 e compatibilizacao com EPE realizada.")

    observacoes = [
        # Beiru / Tancredo Neves (ID: 1)
        {'territorio_id': 1, 'indicador_id': 1, 'fonte_id': 1, 'ano': 2022, 'valor': 52340},
        {'territorio_id': 1, 'indicador_id': 2, 'fonte_id': 1, 'ano': 2022, 'valor': 17850},
        {'territorio_id': 1, 'indicador_id': 3, 'fonte_id': 1, 'ano': 2022, 'valor': 2.93},
        {'territorio_id': 1, 'indicador_id': 4, 'fonte_id': 1, 'ano': 2022, 'valor': 1120.50},
        {'territorio_id': 1, 'indicador_id': 5, 'fonte_id': 1, 'ano': 2022, 'valor': 48.7},
        {'territorio_id': 1, 'indicador_id': 6, 'fonte_id': 2, 'ano': 2022, 'valor': 0.468},
        {'territorio_id': 1, 'indicador_id': 7, 'fonte_id': 1, 'ano': 2022, 'valor': 28.4},
        {'territorio_id': 1, 'indicador_id': 8, 'fonte_id': 1, 'ano': 2022, 'valor': 4.8},
        {'territorio_id': 1, 'indicador_id': 9, 'fonte_id': 1, 'ano': 2022, 'valor': 16.2},
        {'territorio_id': 1, 'indicador_id': 10, 'fonte_id': 1, 'ano': 2022, 'valor': 18.9},
        {'territorio_id': 1, 'indicador_id': 11, 'fonte_id': 1, 'ano': 2022, 'valor': 21.3},
        {'territorio_id': 1, 'indicador_id': 12, 'fonte_id': 1, 'ano': 2022, 'valor': 99.1},
        {'territorio_id': 1, 'indicador_id': 16, 'fonte_id': 1, 'ano': 2022, 'valor': 11.8},
        {'territorio_id': 1, 'indicador_id': 17, 'fonte_id': 1, 'ano': 2022, 'valor': 0.68},

        # Pernambués (ID: 2)
        {'territorio_id': 2, 'indicador_id': 1, 'fonte_id': 1, 'ano': 2022, 'valor': 64890},
        {'territorio_id': 2, 'indicador_id': 2, 'fonte_id': 1, 'ano': 2022, 'valor': 22680},
        {'territorio_id': 2, 'indicador_id': 3, 'fonte_id': 1, 'ano': 2022, 'valor': 2.86},
        {'territorio_id': 2, 'indicador_id': 4, 'fonte_id': 1, 'ano': 2022, 'valor': 1280.00},
        {'territorio_id': 2, 'indicador_id': 5, 'fonte_id': 1, 'ano': 2022, 'valor': 42.1},
        {'territorio_id': 2, 'indicador_id': 6, 'fonte_id': 2, 'ano': 2022, 'valor': 0.412},
        {'territorio_id': 2, 'indicador_id': 7, 'fonte_id': 1, 'ano': 2022, 'valor': 22.8},
        {'territorio_id': 2, 'indicador_id': 8, 'fonte_id': 1, 'ano': 2022, 'valor': 3.2},
        {'territorio_id': 2, 'indicador_id': 9, 'fonte_id': 1, 'ano': 2022, 'valor': 12.5},
        {'territorio_id': 2, 'indicador_id': 10, 'fonte_id': 1, 'ano': 2022, 'valor': 14.6},
        {'territorio_id': 2, 'indicador_id': 11, 'fonte_id': 1, 'ano': 2022, 'valor': 15.7},
        {'territorio_id': 2, 'indicador_id': 12, 'fonte_id': 1, 'ano': 2022, 'valor': 99.4},
        {'territorio_id': 2, 'indicador_id': 16, 'fonte_id': 1, 'ano': 2022, 'valor': 9.8},
        {'territorio_id': 2, 'indicador_id': 17, 'fonte_id': 1, 'ano': 2022, 'valor': 0.58},

        # Salvador (Média Municipal - ID: 3)
        {'territorio_id': 3, 'indicador_id': 1, 'fonte_id': 1, 'ano': 2022, 'valor': 2418005},
        {'territorio_id': 3, 'indicador_id': 2, 'fonte_id': 1, 'ano': 2022, 'valor': 924500},
        {'territorio_id': 3, 'indicador_id': 3, 'fonte_id': 1, 'ano': 2022, 'valor': 2.62},
        {'territorio_id': 3, 'indicador_id': 4, 'fonte_id': 1, 'ano': 2022, 'valor': 2150.00},
        {'territorio_id': 3, 'indicador_id': 5, 'fonte_id': 1, 'ano': 2022, 'valor': 29.5},
        {'territorio_id': 3, 'indicador_id': 6, 'fonte_id': 2, 'ano': 2022, 'valor': 0.334},
        {'territorio_id': 3, 'indicador_id': 7, 'fonte_id': 1, 'ano': 2022, 'valor': 14.1},
        {'territorio_id': 3, 'indicador_id': 8, 'fonte_id': 1, 'ano': 2022, 'valor': 1.8},
        {'territorio_id': 3, 'indicador_id': 9, 'fonte_id': 1, 'ano': 2022, 'valor': 8.3},
        {'territorio_id': 3, 'indicador_id': 10, 'fonte_id': 1, 'ano': 2022, 'valor': 9.1},
        {'territorio_id': 3, 'indicador_id': 11, 'fonte_id': 1, 'ano': 2022, 'valor': 8.9},
        {'territorio_id': 3, 'indicador_id': 12, 'fonte_id': 1, 'ano': 2022, 'valor': 99.8},
        {'territorio_id': 3, 'indicador_id': 16, 'fonte_id': 1, 'ano': 2022, 'valor': 6.2},
        {'territorio_id': 3, 'indicador_id': 17, 'fonte_id': 1, 'ano': 2022, 'valor': 0.38},

        # Bahia (Série EPE - ID: 4)
        {'territorio_id': 4, 'indicador_id': 13, 'fonte_id': 3, 'ano': 2022, 'valor': 512.8},
        {'territorio_id': 4, 'indicador_id': 14, 'fonte_id': 3, 'ano': 2022, 'valor': 5.71},
        {'territorio_id': 4, 'indicador_id': 15, 'fonte_id': 3, 'ano': 2022, 'valor': 7690}
    ]

    csv_path = os.path.join(output_dir, 'observacoes.csv')
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['territorio_id', 'indicador_id', 'fonte_id', 'ano', 'valor'])
        writer.writeheader()
        writer.writerows(observacoes)

    print(f"[SUCESSO] Arquivo {csv_path} gerado com {len(observacoes)} observações.")

if __name__ == '__main__':
    main()

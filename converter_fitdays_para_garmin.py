import xlrd
import csv
import sys
import os
import re
from datetime import datetime

def limpar_data(valor):
    """Remove a hora de um valor de data, deixando apenas a parte da data."""
    if isinstance(valor, (int, float)):  # Pode ser uma data numérica do Excel
        try:
            # Converte data Excel (número de dias desde 1899-12-30)
            data = datetime(1899, 12, 30) + timedelta(days=int(valor))
            return data.strftime("%d/%m/%Y")
        except Exception:
            return str(valor)
    elif isinstance(valor, str):
        match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', valor)
        if match:
            return match.group(1)
        return valor.strip()
    return valor

def limpar_peso(valor):
    """Mantém apenas o número principal antes do parêntese ou texto."""
    if isinstance(valor, str):
        match = re.match(r'^\s*([\d.,]+)', valor)
        if match:
            return match.group(1).replace(',', '.')
        return valor.strip()
    return valor

def limpar_gordura(valor):
    """Mantém apenas o número principal antes de parênteses, % ou texto."""
    if isinstance(valor, str):
        match = re.match(r'^\s*([\d.,]+)', valor)
        if match:
            return match.group(1).replace(',', '.')
        return valor.strip()
    return valor

def xls_para_csv_convertido(arquivo_xls, arquivo_csv=None, indice_planilha=0):
    colunas_desejadas = ["Data", "Peso", "IMC", "Gordura corporal"]
    novos_nomes = ["date", "weight", "bmi", "fat"]

    if arquivo_csv is None:
        base = os.path.splitext(arquivo_xls)[0]
        arquivo_csv = base + "_convertido.csv"

    workbook = xlrd.open_workbook(arquivo_xls)
    sheet = workbook.sheet_by_index(indice_planilha)

    header = sheet.row_values(0)

    indices = []
    nomes_colunas_encontradas = []
    for col in colunas_desejadas:
        try:
            idx = header.index(col)
            indices.append(idx)
            nomes_colunas_encontradas.append(col)
        except ValueError:
            print(f"Aviso: coluna '{col}' não encontrada no arquivo.")

    if not indices:
        print("Nenhuma das colunas desejadas foi encontrada. Nada será exportado.")
        return

    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # 🔹 Linha extra no topo
        writer.writerow(["Body"])

        # Cabeçalhos renomeados
        header_final = [
            novos_nomes[colunas_desejadas.index(nome)]
            for nome in nomes_colunas_encontradas
        ]
        writer.writerow(header_final)

        for row_idx in range(1, sheet.nrows):
            linha = sheet.row_values(row_idx)
            nova_linha = []

            for col_nome, i in zip(nomes_colunas_encontradas, indices):
                valor = linha[i]
                coluna = col_nome.strip().lower()

                if coluna == "data":
                    valor = limpar_data(valor)
                elif coluna == "peso":
                    valor = limpar_peso(valor)
                elif coluna == "gordura corporal":
                    valor = limpar_gordura(valor)

                nova_linha.append(valor)

            writer.writerow(nova_linha)

    print(f"Arquivo CSV convertido de Fitdays para Garmin criado com sucesso: {arquivo_csv}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python converter_xls_para_csv_convertido.py arquivo.xls [arquivo.csv]")
    else:
        xls_para_csv_convertido(*sys.argv[1:])


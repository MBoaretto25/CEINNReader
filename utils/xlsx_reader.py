import pandas as pd


def read_xlsl(file_path):
    """
    Read the xlsx files and return a dataframe with cleaned and parsed data
    :param file_path: path of the file
    :return: dataframe
    """
    df = pd.read_excel(file_path,
                       header=10,
                       keep_default_na=False,
                       parse_dates=True,
                       sheet_name="Ana")

    cols = df.columns
    cols_to_drop = [c for c in cols if "Unnamed" in c]
    cols_to_drop.append("Mercado")
    cols_to_drop.append("Especificação do Ativo")
    cols_to_drop.append("Prazo")

    # Drop Columns
    df = df.drop(columns=cols_to_drop)
    # Drop Last 4 Rows
    df = df.drop(df.index[-4:])

    return df

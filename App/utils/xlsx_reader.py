import pandas as pd
from pandas.core.indexes.datetimes import DatetimeIndex


def read_xls(file_path):
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

    date_column = df.columns[0]
    c_v_column = df.columns[1]

    #  stripping spaces in date columns
    for index, row in df.iterrows():
            row = row.copy()
            df.loc[index, date_column] = row[0].strip()
            df.loc[index, c_v_column] = row[1].strip()

    df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%y')

    df['Year'] = DatetimeIndex(df[date_column]).year
    df['Month'] = DatetimeIndex(df[date_column]).month
    df['Day'] = DatetimeIndex(df[date_column]).day

    return df

from prettytable import PrettyTable

from CEINNReader.App.df_handler import DFHandler


def monthly_portfolio(dfh):
    porfolio = dict()

    years = dfh.get_years()
    months = dfh.get_months(year=years[0])
    # stocks = dfh.get_stocks(year=years[0], month=months[0])

    for month in months:
        ops = dfh.filter_operations(
        year=years[0],
        month=month,
        typecv="")

        for idx, row in ops.iterrows():
            typecv = row[1]
            stock = row[2]
            qtd = row[3]
            price = row[4]

            if typecv == "C":
                op_stock = porfolio.get(stock)

                if not op_stock:
                    porfolio.update(stock={
                        'price': price,
                        'qtty': qtd,
                    })
                else:
                    old_price = porfolio.get(stock).get("price")
                    old_qtd = porfolio.get(stock).get("qtty")

                    new_qtd = old_qtd + qtd
                    new_price = (old_price + price)/(new_qtd)

                    porfolio.update(stock={
                        'price': new_price,
                        'qtty': new_qtd,
                    })







def generate_monthly_portfolio(df, dfh, m, y, portfolio):
    t = PrettyTable(['Stock', 'Qtd', 'Price (R$)', 'Total (R$)', '%'])

    for idx, row in df.iterrows():
        try:
            if row[1] == "C":
                t.add_row([row[0].strftime('%d'), row[1], row[2], "{0:0.02f}".format(row[4]), row[3], "{0:0.02f}".format(row[5]), "{0:0.02f}%".format(row[5]*100/total_C)])
            else:
                t.add_row([row[0].strftime('%d'), row[1], row[2], "{0:0.02f}".format(row[4]), row[3], "{0:0.02f}".format(row[5]), "---"])
        except ZeroDivisionError:
            pass


    print("======================================================================================")
    print("                               ===  {}/{} ===                                         ".format(m, y))
    print(t)
    print("======================================================================================")


def monthly_reports(dfh):
    years = dfh.get_years()
    months = dfh.get_months(year=years[0])
    # stocks = dfh.get_stocks(year=years[0], month=months[0])

    for month in months:
        ops = dfh.filter_operations(
        year=years[0],
        month=month,
        typecv=""
        )
        generate_montly_reports(ops, dfh, month, years[0])

def generate_montly_reports(df, dfh, m, y):
    t = PrettyTable(['Date', 'C/V', 'Stock', 'Price (R$)', 'Qtd', 'Total (R$)', '%'])

    total_C = df[df['C/V'].eq("C")][dfh.total_price_col].sum()

    total_V = df[df['C/V'].eq("V")][dfh.total_price_col].sum()

    total_final = total_V - total_C

    df = df.sort_values(["C/V"])

    for idx, row in df.iterrows():
        try:
            if row[1] == "C":
                t.add_row([row[0].strftime('%d'), row[1], row[2], "{0:0.02f}".format(row[4]), row[3], "{0:0.02f}".format(row[5]), "{0:0.02f}%".format(row[5]*100/total_C)])
            else:
                t.add_row([row[0].strftime('%d'), row[1], row[2], "{0:0.02f}".format(row[4]), row[3], "{0:0.02f}".format(row[5]), "---"])
        except ZeroDivisionError:
            pass

    t.add_row([" ", " ", " ", " ", " ", "{0:0.02f}".format(total_final), "100%"])

    print("======================================================================================")
    print("                               ===  {}/{} ===                                         ".format(m, y))
    print(t)
    print("======================================================================================")


if __name__ == "__main__":

    file_name = "data/InfoCEI_2019.xls"
    dfh = DFHandler(file_name)

    monthly_reports(dfh)
    monhtly_portfolio(dfh)






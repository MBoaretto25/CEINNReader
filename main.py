import collections

from prettytable import PrettyTable

from CEINNReader.App.df_handler import DFHandler


def monthly_portfolio(dfh, portfolio=None):

    if not portfolio:
        portfolio = collections.OrderedDict()

    years = dfh.get_years()
    # stocks = dfh.get_stocks(year=years[0], month=months[0])
    for year in years:
        months = dfh.get_months(year=year)
        for month in months:
            ops = dfh.filter_operations(
                year=year,
                month=month,
                typecv="")

            for idx, row in ops.iterrows():
                typecv = row[1]
                stock = row[2]
                qtd = row[3]
                price = row[4]

                if typecv == "C":
                    op_stock = portfolio.get(stock)
                    if op_stock:
                        old_price = portfolio.get(stock).get("price")
                        old_qtd = portfolio.get(stock).get("qtty")

                        new_qtd = old_qtd + qtd
                        new_price = ((old_qtd*old_price) + (qtd*price))/(new_qtd)

                        price = new_price
                        qtd = new_qtd
                else:
                    op_stock = portfolio.get(stock)

                    if not op_stock:
                        continue

                    old_price = portfolio.get(stock).get("price")
                    old_qtd = portfolio.get(stock).get("qtty")

                    new_qtd = old_qtd - qtd

                    if new_qtd == 0:
                        portfolio.pop(stock)
                        continue
                    else:
                        new_price = ((old_qtd*old_price) + (qtd*price))/(new_qtd)

                        price = new_price
                        qtd = new_qtd

                portfolio.update(
                    {stock: {
                        'price': price,
                        'qtty': qtd,
                    }})

            generate_monthly_portfolio(month, year, portfolio)

    return portfolio


def generate_monthly_portfolio(m, y, portfolio):
    t = PrettyTable(['Stock', 'Qtd', 'Price (R$)', 'Total (R$)', '%'])

    total_P = sum([v['price']*v['qtty'] for k, v in sorted(portfolio.items())])
    total_S = sum([v['qtty'] for k, v in sorted(portfolio.items())])

    for k, v in sorted(portfolio.items()):
        try:
            price = v['price']
            qtty = v['qtty']
            total = v['price']*v['qtty']
            t.add_row([k, qtty, "{0:0.02f}".format(price), "{0:0.02f}".format(total), "{0:0.02f}%".format(total*100/total_P)])
        except ZeroDivisionError:
            pass
    t.add_row([" ", total_S, " ", "{0:0.02f}".format(total_P), "100%"])

    print("======================================================================================")
    print("                               ===  {}/{} ===                                         ".format(m, y))
    print(t)
    print("======================================================================================")



def monthly_reports(dfh):
    years = dfh.get_years()

    for year in years:
        months = dfh.get_months(year=year)
        # stocks = dfh.get_stocks(year=years[0], month=months[0])

        for month in months:
            ops = dfh.filter_operations(
                year=year,
                month=month,
                typecv=""
            )

            if ops.empty:
                continue
            generate_montly_reports(ops, dfh, month, year)


def generate_montly_reports(df, dfh, m, y):
    t = PrettyTable(['Date', 'C/V', 'Stock', 'Price (R$)', 'Qtd', 'Total (R$)', '%', "DayTrade"])

    total_C = df[df['C/V'].eq("C")][dfh.total_price_col].sum()

    total_V = df[df['C/V'].eq("V")][dfh.total_price_col].sum()

    total_final = total_V - total_C

    # df = df.sort_values(["C/V"])

    for idx, row in df.iterrows():
        try:
            day_trade_show = row[-1] if row[-1] else "---"
            if row[1] == "C":
                t.add_row([row[0].strftime('%d'), row[1], row[2], "{0:0.02f}".format(row[4]), row[3], "{0:0.02f}".format(row[5]), "{0:0.02f}%".format(row[5]*100/total_C), day_trade_show])
            else:
                t.add_row([row[0].strftime('%d'), row[1], row[2], "{0:0.02f}".format(row[4]), row[3], "{0:0.02f}".format(row[5]), "---", day_trade_show])

        except ZeroDivisionError:
            pass

    t.add_row([" ", " ", " ", " ", " ", "{0:0.02f}".format(total_final), "100%", "---"])

    print("======================================================================================")
    print("                               ===  {}/{} ===                                         ".format(m, y))
    print(t)
    print("======================================================================================")


if __name__ == "__main__":

    file_name = "data/InfoCEI_All_time.xls"
    dfh = DFHandler(file_name)

    monthly_reports(dfh)
    # portfolio = monthly_portfolio(dfh)







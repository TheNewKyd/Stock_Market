"""
    Application displays current stack market
    and sums up buy/sell orders best prices

    Variables:
        STOCK - dictionary, global object storing stark market raws
        order_raw - list, keyboard input for STOCK object
        sell_df - data frame with only 'Sell' orders
        buy_df - data frame with only 'Buy' orders
        buy_best_price - max value from 'Price' column in buy_df
        sell_best_price - max value from 'Price' column in sell_df
        best_buy_id - string, value of 'Id' column in 'Buy' type with the best price
        best_sell_id - string, value of 'Id' column in 'Sell' type with the best price
"""

import pandas as pd

# 1) create object to store stock
STOCK = {'Id': [],
         'Order': [],
         'Type': [],
         'Price': [],
         'Quantity': []
         }

def printDataFrame():
    """
        Prints current stock state
    """
    print("\n", pd.DataFrame(data=STOCK), "\n")

def createSellDf(clean_stock):
    """
        Creates sorted data frame with 'Sell' orders only
    """
    return clean_stock.loc[clean_stock.Order == 'Sell'].sort_values(by='ValuePerStock', ascending=False)

def createBuyDf(clean_stock):
    """
        Creates sorted data frame with 'Buy' orders only
    """
    return clean_stock.loc[clean_stock.Order == 'Buy'].sort_values(by='ValuePerStock', ascending=False)

def sumBestPrices(filtered_stock):
    """
        Sums up max values in 'Price' column, in sell and buy data frames
        Returns sum and ids of buy and sell best orders
    """
    sell_df = createSellDf(filtered_stock)
    buy_df = createBuyDf(filtered_stock)

    try:
        buy_best_price = buy_df.iloc[0]['ValuePerStock']
        best_buy_id = buy_df.iloc[0]['Id']

        sell_best_price = sell_df.iloc[0]['ValuePerStock']
        best_sell_id = sell_df.iloc[0]['Id']

        _sum = buy_best_price + sell_best_price
        return _sum, best_buy_id, best_sell_id
    except IndexError:
        return 0, 'no id', 'no id'

def filterDataFrame(stock):
    """
        Filters out rows with 'Remove' type and sharing same id as 'Remove' row
        Adds column 'ValuePerStock' with values per stock in every order
    """
    filtered_stock = stock.drop_duplicates(subset='Id', keep=False)

    filtered_stock.Price = filtered_stock.Price.astype(float)
    filtered_stock.Quantity = filtered_stock.Quantity.astype(float)
    filtered_stock['ValuePerStock'] = filtered_stock.Quantity / \
        filtered_stock.Price

    return filtered_stock

def appFlow():
    """
        Adds input to STOCK and performs application flow
        2) write a piece of code that in every step displays the sum
        of buy/sell orders with a best price
    """
    try:

        while True:
            # keyboard input
            order_raw = [x for x in input().split(" ")]
            i = 0
            for column in STOCK.values():
                column.append(order_raw[i])
                i += 1
            # creates stock data frame from STOCK dictionary
            printDataFrame()
            stock = pd.DataFrame(data=STOCK)
            # filters
            filtered_stock = filterDataFrame(stock)
            # display best price sum up
            _sum, best_buy_id, best_sell_id = sumBestPrices(filtered_stock)
            print('Best buy/sell prices sum value: ', "%.3f" % _sum, "\n")
            print("Buy id: ", best_buy_id)
            print("Sell id: ", best_sell_id)

    except KeyboardInterrupt:
        print("\n")
        printDataFrame()
        print("Application closed")

if __name__ == '__main__':
    appFlow()

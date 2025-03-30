from data_loader import YahooStockDataSource

class MyTradingParams:
    def __init__(self, tradingFunctions):
        self.__tradingFunctions = tradingFunctions
        self.__instrumentIds = tradingFunctions.getSymbolsToTrade()
        self.__startDate = '2024-01-01'
        self.__endDate = '2024-12-31'
        self.__dataLoader = YahooStockDataSource(self.__instrumentIds, self.__startDate, self.__endDate)

    def getDataLoader(self):
        return self.__dataLoader

    def getSymbolsToTrade(self):
        return self.__instrumentIds

    def getStartDate(self):
        return self.__startDate

    def getEndDate(self):
        return self.__endDate

    def getStartingCapital(self):
        return 1000 * len(self.__instrumentIds)
    
    def getTradingFunctions(self):
        return self.__tradingFunctions
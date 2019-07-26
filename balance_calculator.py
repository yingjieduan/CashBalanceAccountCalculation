# -*- coding: utf-8 -*-
"""
@author: yingjie
"""

import numpy as np
from utility import *

class BalanceCalculator(object):

    balance = None

    def __init__(self):
        self._loadInputFiles()

    def _loadInputFiles(self):
        self.beginBalance = FileLoader.csvLoader(r'./input\BeginningBalance.csv', ['Date'])
        self.trans = FileLoader.csvLoader(r'./input/Transactions.csv', ['Date'])
        self.EURinterest = FileLoader.csvLoader(r'./input\EURinterest.csv', ['Date'])
        self.JPYinterest = FileLoader.csvLoader(r'./input\JPYinterest.csv', ['Date'])
        self.USDinterest = FileLoader.csvLoader(r'./input\USDinterest.csv', ['Date'])
        self.dates = FileLoader.csvLoader(r'./input\date.csv', ['Date'])

        self.interest = {'USD':0.0,
                    'EUR':0.0,
                    'JPY':0.0}

        self.EURinterest.loc[:, 'Rate'] *= 0.01
        self.JPYinterest.loc[:, 'Rate'] *= 0.01
        self.USDinterest.loc[:, 'Rate'] *= 0.01

    def _calculateInterest(self, row, interest):
        #print(row)
        #print(self.interest)
        if row['Type'] == 'D':
            return row
        row['Value'] = row['Value'] * (1 + self.interest[row['Curr']]/356)
        return row['Value']
    
    def calculateFinalBalance(self):
        for i, day in self.dates.iterrows():
            currDate = np.datetime64(day['Date'])
            print('\n', currDate)
        
            # cal self.interest
            self.interest['USD'] = self.USDinterest.loc[self.USDinterest['Date'] == currDate, 'Rate'].values[0] \
                if currDate in self.USDinterest['Date'].values else self.interest['USD']
            self.interest['EUR'] = self.EURinterest.loc[self.EURinterest['Date'] == currDate, 'Rate'].values[0] \
                if currDate in self.EURinterest['Date'].values else self.interest['EUR']
            self.interest['JPY'] = self.JPYinterest.loc[self.JPYinterest['Date'] == currDate, 'Rate'].values[0] \
                if currDate in self.JPYinterest['Date'].values else self.interest['JPY']
            
            # read balance in
            if self.balance is None and currDate in self.beginBalance.loc[:,'Date'].values:
                self.balance = self.beginBalance.loc[self.beginBalance['Date'] == currDate,:]
                continue
            elif currDate in self.beginBalance.loc[:,'Date'].values:
                self.balance = self.balance.append(self.beginBalance.loc[self.beginBalance['Date'] == currDate,:])
        
            # calculate and add self.interest into account
            self.balance.loc[:,'Value'] = self.balance.apply(self._calculateInterest, axis=1, interest=self.interest)
        
            # transactions happened
            currTrans = self.trans.loc[self.trans['Date'] == currDate, :]
        
            # update balance of account
            for i, tran in currTrans.iterrows():
                account = tran['AccountNumber']
                self.balance.loc[self.balance['AccountNumber'] == account, 'Value'] += tran['SettlementValue']
                #print(balance)
        
            self.balance['Date'] = currDate
            # print(balance)

    def getBalance(self):
        FileSaver.saveToCSV(self.balance,'./output', 'Balance.csv', index=False)
    
if __name__ == '__main__':
    cal = BalanceCalculator()
    cal.calculateFinalBalance()
    cal.getBalance()
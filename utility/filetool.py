import os
import pandas as pd

class FileLoader(object):
    #@classmethod

    defaultDateFormat = "%m/%d/%Y"
    databaseDateFormat = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def csvLoader(strDirectory, listDateColumns = None, format = defaultDateFormat):
        df = None
        strDirectory.replace('\\', '/')
        if os.path.isfile(strDirectory):
            df = pd.read_csv(strDirectory)
            if listDateColumns is not None and len(listDateColumns) > 0:
                for id in listDateColumns:
                    df[id] = pd.to_datetime(df[id], format = format)

        return df

    @staticmethod
    def excelLoader(strDirectory, sheetname = 0, listDateColumns=None, format=defaultDateFormat):
        df = None
        strDirectory.replace('\\', '/')
        if os.path.isfile(strDirectory):
            df = pd.read_excel(strDirectory, sheetname = sheetname)
            if listDateColumns is not None and len(listDateColumns) > 0:
                for id in listDateColumns:
                    df[id] = pd.to_datetime(df[id], format=format)

        return df


class FileSaver(object):

    @staticmethod
    def saveToCSV(df, strDirectory, fileName, index = False):

        if not os.path.isdir(strDirectory):
            try:
                os.makedirs(strDirectory)
            except:
                #todo: should use logging
                print("strDirectory is not a proper directory. Save in current directory.")
                df.to_csv(fileName, index = index )

        strDirectory.replace('\\', '/')
        df.to_csv(strDirectory + '/' + fileName, index = index )

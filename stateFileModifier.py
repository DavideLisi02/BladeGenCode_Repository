import os

class BGIData:

    def __init__(self, filePath ='defaultBGI\geometry00.bgi', **kwargs):
        """
        Class containing all functions and data about a specific .bgi file
        """
        super(BGIData, self).__init__()

        self.filePath = filePath
        self.DataList = self.readfile(filePath)
        return

    def readfile(filePath = 'defaultBGI\geometry00.bgi'):
        file = open(filePath, 'r')
        DataList = file.read()
        return DataList
    
    def convert_list_to_json(list):

        return



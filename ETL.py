
import ResultsParser
import XmlReader
import DataLoader


MaxLens  = {}
AttrsDI  = XmlReader.AttrsDI
ValuesDI = XmlReader.ValuesDI

def Extract():

    ResultsParser.Get__stidues__with__results()

    outline = 'Extract studies with results : done'
    print(outline)


def Transform():

    XmlReader.Get__range()
    outline = 'Transform : prepare information on study results: done'
    print(outline)
     

def Load():

    DataLoader.Start()



def Start():

    Load()

Start()

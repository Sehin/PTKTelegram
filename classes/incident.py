class Incident:
    ESPPNum = ''
    EK = ''
    description = ''
    date = ''
    def __init__(self, ESPPNum, EK, description, date='0'):
        self.ESPPNum = ESPPNum
        self.EK = EK
        self.description = description
        self.date = date
        pass

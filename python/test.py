class DataCreator:
    def __init__(self):
        self.data = [1, 2, 3]

    def get_data(self):
        return self.data

class DataConsumer:
    def __init__(self):
        creator = DataCreator()
        self.data = creator.get_data()

    def print_data(self):
        print(self.data)


DataCreator.__init__(self)
DataConsumer.__init__(self)

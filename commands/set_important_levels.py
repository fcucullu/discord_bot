from utils.json_file_manager import JSONFileManager
from tabulate import tabulate

class GetInfoFromJSON(JSONFileManager):
    def run(self): 
        return self.pretty_print(self.read_file())
    def pretty_print(self, data):
        return tabulate(data, headers='keys')

class WriteInfoJSON(JSONFileManager):
    def run(self, pair, level): 
        self.write_file(pair, level)
        return

class DeleteInfoJSON(JSONFileManager):
    def run(self, pair, level): 
        self.delete_info_from_file(pair, level)
        return 
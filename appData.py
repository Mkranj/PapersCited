class AppData:
    def __init__(self, startup_filename, startup_results):
        self.active_filename = startup_filename
        self.active_results = startup_results
        
    def set_new_filename(self, filename, list_affected_wg):
        self.active_filename = filename
        for widget in list_affected_wg:
            widget["text"] = self.active_filename
            
    def set_new_results(self, results, list_affected_wg):
        self.active_results = results
        for widget in list_affected_wg:
            widget["text"] = self.active_results
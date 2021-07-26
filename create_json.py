import json
import io

class CreteJsonFile:
    def __init__(self):
        self.cord = []
        self.mouse = []
        
    def create(self,cord_cam):
        data = {'coord': str(cord_cam) }
        print(cord_cam[0], ' ')
        with io.open('data.json', 'w', encoding='utf8') as outfile:
            str_ = outfile.write(json.dumps(data))
        print('good job man')
        
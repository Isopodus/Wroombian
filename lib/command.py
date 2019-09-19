# Comand class

def split(line, ignorechars:list=['\'', '"'], splitchars:list=[' ', ',', ';']): 
        result = []
        string = ""
        ignore = False
        for c in line:
            if c in ignorechars:
                ignore = True if ignore == False else False
            elif c in splitchars and not ignore:
                if string != '':
                    result.append(string)
                string = ""
            else:
                string += c
                
        if string != '':
            result.append(string)
        return result
    
class Command:
    
    sudo = False
    command = '-1'
    options = []
    
    def __init__(self, raw_text):
        substrings = split(raw_text)
        if len(substrings) > 1 and substrings[0] == 'sudo':
            self.sudo = True
            self.command = substrings[1]
            self.options = substrings[2:]
            
        elif len(substrings) == 1 and substrings[0] == 'sudo':
            pass # TODO provide message about missing command
        elif len(substrings) > 0:
            self.command = substrings[0]
            self.options = substrings[1:]
            
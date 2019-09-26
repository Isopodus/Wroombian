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
    
class CommandString:
    
    sudo = False
    command_name = None
    keys = []
    
    def __init__(self, raw_text):
        substrings = split(raw_text)

        if len(substrings) > 0:
            if substrings[0] == 'sudo':
                self.sudo = True
                substrings.pop(0)
            if len(substrings) > 0:
                self.command_name = substrings[0]
                self.keys = substrings[1:]
            
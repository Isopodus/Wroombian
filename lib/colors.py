# Colored text
def red(skk):
    return "\033[91m{}\033[0m" .format(skk)
def green(skk):
    return "\033[92m{}\033[0m" .format(skk)
def yellow(skk):
    return "\033[93m{}\033[0m" .format(skk)
def lPurple(skk):
    return "\033[94m{}\033[0m" .format(skk)
def purple(skk):
    return "\033[95m{}\033[0m" .format(skk)
def blue(skk):
    return "\033[34;1m{}\033[0m" .format(skk)
def cyan(skk):
    return "\033[96m{}\033[0m" .format(skk)
def lGray(skk):
    return "\033[97m{}\033[0m" .format(skk)
def black(skk):
    return "\033[98m{}\033[0m" .format(skk)
def keepRed():
    print("\033[91m")
def resetColor():
    print("\033[0m")
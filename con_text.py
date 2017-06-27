import re
def con_text(x):
    #for use with Beautiful Soup objects that have the text attribute
    #replaces Nones with "Not available"
    if type(x) == tuple:
        new = list(x)
    elif type(x) == list:
        new = x
    else:
        return "Argument must be either tuple or list"
    for i in range(0, len(new)):
        try:
            new[i] = new[i].text
        except AttributeError as AE:
            if type(new[i]) == str:
                new[i] = new[i]
            else:
                new[i] = "Not available"
    return list(new)

def con_text_s(x):
    #for use with a single Beautiful Soup object that has the text attribute
    try:
        x = re.sub('\n', '', x.text)
    except AttributeError as AE:
        if type(x) == str:
            return x
        else:
            return "Not Available"
    return x

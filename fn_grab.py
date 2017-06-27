def fn_grab(x):#returns file name at the end of a url or file path
    if '/' in x:
        path_div = '/'
    elif '\\' in x:
        path_div = '\\'#won't work unless the input is properly formatted since a normal forward slash will be escaped
    else:
        return x #if there are no slashes then it just returns x
    new = x.split(path_div)
    return new[len(new)-1]
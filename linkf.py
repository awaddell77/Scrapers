def linkF(s,n, base = 0, attrs= 0, default = '"'):#x is the item, n = tag takes link tag (MUST BE STRING) and extracts the link
    l =[]
    ln = ''
    x = s
    if attrs != 0:
        x = re.sub('<a','', x)#strips the tag from the string, helps in certain situations where the location of the link changes in between elements
    elif type(attrs) == str:
        x = re.sub(attrs, '', x)
    ln_s = x.split(default)
    for i in range(0, len(ln_s)):
        if ln_s[i] == n or ln_s[i] == ' ' + n:
            if ln_s[i+1] != 'javascript:void(0);':
                ln = ln_s[i+1] #ln is the link (still needs to be joined witht the base URL
    if base == 0 and not ln or ln is None:
        return ""
    else:
        ln = base + ln #MAJOR WORKAROUND!!!! IN THE FUTURE THS SHOULD CALL A FUNCTION THAT FINDS THE BASE
        return ln

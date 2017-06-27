
def text_wc(x,output='listoutput.txt', directory = 'C:\\Users\\Owner\\', v = 0):#takes list writes to text
    n_l = x
    name = directory + output
    with open(name, 'w') as wf:
        for i in range(0, len(n_l)):
            if v != 0:
                print(n_l[i])
                new = n_l[i]+ "\n"
                wf.writelines(new)

            else:
                new = n_l[i]+ "\n"
                wf.writelines(new)
    print("%s saved to %s" % (output, directory))
    return True
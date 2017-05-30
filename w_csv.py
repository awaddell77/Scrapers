#writes csv
import csv


def w_csv(x,output='FCfile.csv'):
    #accepts lists of other lists, spits out CSV file
    count = 1
    while file_present(output):
        output = output.split('.')[0] + "-" + str(count) + '.csv'
        count += 1
        if not file_present(output):
            break
 

    csv_out = open(output, 'w', newline='', encoding='utf-8')
    mywriter = csv.writer(csv_out)
    try:
        print("This is x: %s" % (x))
    except UnicodeEncodeError as UE:
        print("Cannot print to console due to Unicode Error")
    print("Saved file as \"{0}\"".format(output))

    mywriter.writerows(x)
    csv_out.close()
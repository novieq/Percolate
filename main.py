import sys
import os 
import re
import json 

def parse(line, index):
    entry = None
    regexes = [re.compile('([a-zA-Z]+).*?([a-zA-Z]+).*?(?:\d{1}\s)?\(?(\d{3,})\)?-?\s?(\d{3,})-?\s?(\d{4,}).*?([a-zA-Z\s.{1}]+).*?(\d{5,})'),
               re.compile('([a-zA-Z\s.{1}]+).*?([a-zA-Z\s.{1}]+).*?(\d{5,}).*?(?:\d{1}\s)?\(?(\d{3,})\)?-?\s?(\d{3,})-?\s?(\d{4,}).*?([a-zA-Z\s.{1}]+)'),
               re.compile('([a-zA-Z]+)\s([a-zA-Z]+).*?([a-zA-Z\s.{1}]+).*?(\d{5,}).*?(?:\d{1}\s)?\(?(\d{3,})\)?-?\s?(\d{3,})-?\s?(\d{4,})')]
    
    for i,regex in enumerate(regexes):
        match = regex.match(line)
        if(match):
            if(i == 0):
                indices = [6, 2, 1, 3, 4, 5, 7]
            elif(i == 1):
                indices = [7, 1, 2, 4, 5, 6, 3]
            elif(i == 2):
                indices = [3, 1, 2, 5, 6, 7, 4]
            
            color = match.group(indices[0]).strip()
            firstname = match.group(indices[1]).strip()
            lastname = match.group(indices[2]).strip()
            phonenumber = (match.group(indices[3]) + "-" + match.group(indices[4]) + "-" + match.group(indices[5])).strip()
            zipcode = match.group(indices[6]).strip()
    
            if len(phonenumber) == 12 and len(zipcode) == 5 and len(color)>0 and len(firstname)>0 and len(lastname) >0:    
                entry = dict([('color', color), ('firstname', firstname), ('lastname', lastname),
                    ('phonenumber', phonenumber), ('zipcode', zipcode)])
                return entry
                
    return index 

def convert_to_json(entries, errors):
    entries = sorted(entries, key=lambda k: (k['lastname'], k['firstname']))
    data = dict({'entries': entries, 'errors': errors})
    json_dump = json.dumps(data, sort_keys=True, indent=2)
    return json_dump

def process_data(infile, outfile):
    entries = []
    errors = []
    print "Processing input file ", infile
    print "Output stored in file ", outfile
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    try:
        input = open(__location__ + "/" + infile)
        output = open(__location__ + "/" + outfile, "w")
    except IOError:
        print('Input file or output file not available')
    else:
            for count, line in enumerate(input):
                entry = parse(line, count)
                if(type(entry) is int):
                    errors.append(entry)
                else:
                    entries.append(entry)
    input.close()
    json_dump = convert_to_json(entries, errors)
    output.write(json_dump)
    output.close()
            
    
def usage():
    print "Usage : python main.py <input_file> <output_file>"
    
if __name__ == '__main__':
    print "This only executes when %s is executed rather than imported" % __file__
    print sys.argv
    if(len(sys.argv) != 3):
        usage()
    else:
        process_data(sys.argv[1], sys.argv[2])

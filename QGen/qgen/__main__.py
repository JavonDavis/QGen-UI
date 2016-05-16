import getopt
import sys
import qgen
import os


def main(argv):
    input_file = ''
    output_format = "plain"
    count = 10
    try:
        opts, args = getopt.getopt(argv, "hi:f:c:", ["ifile=", "format=", "count="])
    except getopt.GetoptError:
        print 'qgen.py -i <input_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: qgen.py -i <input_file> -f [plain, moodle]'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-f", "--format"):
            output_format = arg
        elif opt in ("-c", "--count"):
            count = arg
        else:
            print 'Usage: qgen.py -i <input_file> -f [plain, moodle] -c <count>'
            sys.exit()

    if input_file != '':
        if output_format == "moodle":
            file_path = "{0}/{1}".format(os.getcwd(),input_file)
            qgen.build_moodle_xml(file_path, int(count))
    else:
        print "Must specify input file"
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
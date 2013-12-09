import minicollider.parser
try:
    import argparse
except ImportError:
    from minicollider.external import argparse


def parsear_argumentos():
    argparser = argparse.ArgumentParser(formatter_class=
                                        argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-s', '--samplerate',
                           help="The desired sample rate.",
                           default=8000,
                           type=int)
    argparser.add_argument('-b', '--beat',
                           help="The desired beat.",
                           default=8000 / 12,
                           type=int)
    argparser.add_argument('-f', '--file',
                           help="A file with a buffer to parse (optional).")
    return argparser.parse_args()


def parsear_archivo(file):
    try:
        archivo = open(args.file, 'r')
        entrada = archivo.read()
        archivo.close()
    except IOError:
        print 'Error opening the file.'
        exit(1)
    try:
        minicollider.parser.parse(entrada)
    except Exception, e:
        if e: msg = str(e)
        else: msg = 'Syntax Error'
        print "Error: %s" % msg

def prompt():
    while 1:
        try:
            entrada = raw_input('buffer > ')
        except EOFError:
            print
            break
        if entrada != '':
        	try:
        		minicollider.parser.parse(entrada)
        	except Exception, e:
        		print "Error: %s" % e
            


if __name__ == '__main__':
    args = parsear_argumentos()
    minicollider.parser.init(args.samplerate, args.beat)
    if args.file is not None:
        parsear_archivo(args.file)
    else:
        prompt()

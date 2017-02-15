import argparse


URL = None
USER_NAME = None
PASSWORD = None

def createFile(output):
    try:
        with open('output123.xml', 'w') as f:
            f.write(output.encode('utf8'))
    except:
        print 'Error while writing to file: ' ,  sys.exc_info()[0]
        raise


if __name__ == "__main__":
    str = 'Hello Dockerfile'
    print str
    createFile(str)

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Download Resumes from CindyJob.')

    # required arguments definition
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-u', '--url', help='SOAP Endpoint of Cindy Job', required=True)
    required_args.add_argument('-i', '--id', help='Username registered with CindyJob', required=True)
    required_args.add_argument('-p', '--password', help='Password', required=True)

    args = parser.parse_args()

    URL = args.url
    USER_NAME = args.id
    PASSWORD = args.password

    print URL

    print USER_NAME

    print PASSWORD


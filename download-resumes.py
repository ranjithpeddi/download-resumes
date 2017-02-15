# Install the Python Requests library:
# `pip install requests`

import requests
import re
from xml.dom import minidom
import sys
import argparse


URL = None
USER_NAME = None
PASSWORD = None

END_TAG_RESUMES = '</Resumes>'
LAST_PAGE_REGEX = '<LastPage xsi:type="xsd:integer">(.*)<\/LastPage>'
TOTAL_COUNT_REGEX = '<TotalCount xsi:type="xsd:integer">(.*)<\/TotalCount>'

def downloadResumes():
    try:
        requestXmlString = getRequest(1)

        response_xml = getResumePage(requestXmlString)

        lastPageNode = response_xml.getElementsByTagName('LastPage')[0].toxml()

        totalCountNode = response_xml.getElementsByTagName('TotalCount')[0].toxml()

        print 'Total Count: ' + re.match(TOTAL_COUNT_REGEX, totalCountNode).group(1)

        lastPage = re.match(LAST_PAGE_REGEX, lastPageNode).group(1)

        print 'Number of Pages: ' + lastPage

        output = getDefaultXmlOutput()

        output = appendResumeNodes(output, response_xml)

        numberOfPages = int(lastPage)

        numberOfPages = 2

        # Invoke CindeJob for each pageNumber
        for pageNumber in range(2, numberOfPages +1):
            requestXmlString = getRequest(pageNumber)
            response_xml = getResumePage(requestXmlString)
            output = appendResumeNodes(output, response_xml)

        output+= END_TAG_RESUMES

        createFile(output)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        raise
    except :
        print 'Exception while downloading resumes: ' , sys.exc_info()[0]
        raise


def appendResumeNodes(output, response_xml):
    # Append Resumes to output
    resumesNode = getResumeNodes(response_xml)
    output += resumesNode
    return output


def getResumeNodes(response_xml):
    resumesNode = response_xml.getElementsByTagName('Resumes')[0].toxml()
    resumesStr = re.match('<Resumes xsi:type="ns1:ResumesType">([\s\S]*?)<\/Resumes>', resumesNode).group(1)
    return resumesStr


def getResumePage(requestXmlString):
    response = requests.post(
        url=URL,
        headers={
            "Content-Type": "application/xml",
            "Accept": "application/xml",
        },
        data=requestXmlString
    )
    print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status_code))
    return minidom.parseString(response.content)


def getRequest(pageNumber) :
    return """
    <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cin="http://www.cindejobfair.com">
   <soapenv:Header/>
   <soapenv:Body>
      <cin:GetResumePage soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <WebAuthentication xsi:type="cin:WebAuthenticationType">
            <Username xsi:type="xsd:string">""" + str(USER_NAME)+ """</Username>
            <Password xsi:type="xsd:string">""" + str(PASSWORD) + """</Password>
         </WebAuthentication>
         <PageNumber xsi:type="xsd:integer">""" + str(pageNumber) + """</PageNumber>
         <PageSize xsi:type="xsd:integer">100</PageSize>
      </cin:GetResumePage>
   </soapenv:Body>
</soapenv:Envelope>
    """

def getDefaultXmlOutput():
    return """
            <?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.cindejobfair.com" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <Resumes xsi:type="ns1:ResumesType">
    """


def createFile(output):
    try:
        with open('output.xml', 'w') as f:
            f.write(output.encode('utf8'))
    except:
        print 'Error while writing to file: ' ,  sys.exc_info()[0]
        raise

if __name__ == "__main__":
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

    downloadResumes()


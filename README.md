# download-resumes

1) Build the docker image
`docker build -t ranjithpeddi/download-resumes .`

2) Push the docker image
`docker login`
`docker push ranjithpeddi/download-resumes`

3) How to use this docker image.
Upon sucessfull execution this docker image downloads the xml file - output.xml to 'download-resumes/' location.

Using Mac OSX:

``docker  run  -v `pwd`:`pwd` -w `pwd` -i -t  ranjithpeddi/download-resumes -u <URL> -i <ID/USER_NAME> -p <PASSWORD>``

## Simple docker file which will copy the current directory
## and download the respective golang and its package necessary to run the server
## finally it will run the simple perzis api server
FROM golang:1.8

WORKDIR /go/src/simple-factorial-goapp
COPY simple-factorial-goapp /go/src/simple-factorial-goapp/

RUN go-wrapper download   
RUN go-wrapper install    
RUN cd /go/src/simple-factorial-goapp/ && go build

CMD ["/go/src/simple-factorial-goapp/simple-factorial-goapp"]

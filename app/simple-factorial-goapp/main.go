package main

import (
	"log"
	"net/http"
)

func main() {

	// This router will be redifened in the router.go to define how many routes are available for this
	router := NewRouter()

	// This below will direct access to the folder struture that are in the server
	// Dummy Index Page
	router.PathPrefix("/home").Handler(http.StripPrefix("/home", http.FileServer(http.Dir("./static/html/"))))

	// Server will run on particular port
	log.Fatal(http.ListenAndServe(":"+serverPort, router))
}

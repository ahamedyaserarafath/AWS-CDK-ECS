package main

import (
	"fmt"
	"net/http"
    "strconv"
	"strings"

)

// Just entring the dns name will be redirected to upload page
func Index(w http.ResponseWriter, r *http.Request) {

	http.Redirect(w, r, "/home/index.html", http.StatusFound)

}

// This will help for whether the server is up and running successfully
func HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "Welcome To the health check!")
}

/*     function declaration        */
func factorial(n int) string {  
	var factVal uint64 = 1	 
    if(n < 0){
        return("Factorial of negative number doesn't exist.")    
    }else{        
        for j:=1; j<=n; j++ {
            factVal *= uint64(j)
        }
        
    }
    s := fmt.Sprintf("Factorial of the %d is %d ", n, factVal)
	return s
}


// Function helps to get all the data data from database
func calculateFactorial(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	r.ParseForm()
	factorialNumber := r.Form["factorialNumber"]
	factorialNumber1, _  := strconv.Atoi(strings.Join(factorialNumber, ""))
	fmt.Fprintln(w, factorial(factorialNumber1))
}

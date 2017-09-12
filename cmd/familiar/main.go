package main

import (
	"encoding/json"
	"log"
	"net/http"
)

// Message :
type Message struct {
	Message string `json:"message"`
}

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "application/json")
		message := Message{Message: "hello world"}
		encoder := json.NewEncoder(w)
		encoder.Encode(&message)
	})

	log.Println("run (port=8080)...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

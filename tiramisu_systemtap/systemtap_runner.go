package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"syscall"
	"time"
)

type Iosize struct {
	Name string `json:name`
	Avg  int    `json:avg`
}

func timedSIGTERM(p *os.Process, d time.Duration) {
	log.Println("couting down:", d)
	_ = <-time.After(d)
	log.Println("count finished, sending signal")
	err := p.Signal(syscall.SIGTERM)
	log.Println("signal sent")
	if err != nil {
		log.Panic(err)
	}
}

func main() {
	fmt.Print()
	iosizecmd := exec.Command("stap", "bitesize-nd-json.stp")
	iosizeStdoutPipe, err := iosizecmd.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}
	// iosizecmd.Stdout = os.Stdout

	err = iosizecmd.Start()
	if err != nil {
		panic(err)
	}
	go timedSIGTERM(iosizecmd.Process, 20*time.Second)
	log.Println("pid:", iosizecmd.Process.Pid)

	iosizeDecoder := json.NewDecoder(iosizeStdoutPipe)

	openToken, err := iosizeDecoder.Token()
	if err != nil {
		log.Fatalf("error reading openToken: %v\n", err)
	}
	fmt.Printf("%v %T\n", openToken, openToken)

	for iosizeDecoder.More() {
		var message Iosize
		err := iosizeDecoder.Decode(&message)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("Executable: [%v], IO Size: [%v]\n", message.Name, message.Avg)
	}

	closeToken, err := iosizeDecoder.Token()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%v %T\n", closeToken, closeToken)

	err = iosizecmd.Wait()
	if err != nil {
		panic(err)
	}

}

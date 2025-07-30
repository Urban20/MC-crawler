package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

const (
	PUERTO = 25565
	LIMITE = 100             // no tocar a menos que sepas lo que haces (gorountines maximas en simultaneo)
	STDOUT = "ip_escan.data" // donde se desvia el stdout, no modificar
)

var n0 = flag.Int("n0", 0, "")
var n1 = flag.Int("n1", 0, "")

// 130 61
// 54.36.0.0/14 178.32.0.0/15 151.80.0.0/16

/*
	"n1.n2.0.0/16"

- retorna todas las ips del barrido
*/
func Barrido16(n1 int, n2 int) chan string {
	ip := make(chan string)
	var i1 int
	var i2 int

	go func() {
		defer close(ip)
		for i1 < 256 {

			i2++
			ipv4 := fmt.Sprintf("%d.%d.%d.%d", n1, n2, i1, i2)

			if i2 > 256 {
				i2 = 0
				i1++
			}
			ip <- ipv4

		}
	}()
	select {
	case <-ip:
		return ip
	}
}

func main() {
	flag.Parse()
	n0 := *n0
	n1 := *n1

	arch, _ := os.Create(STDOUT)

	os.Stdout = arch

	lim := make(chan struct{}, LIMITE)
	wg := sync.WaitGroup{}

	for ip := range Barrido16(n0, n1) {
		wg.Add(1)
		lim <- struct{}{}

		go func() {
			defer wg.Done()
			defer func() { <-lim }() //liberar el espacio para otra goroutine

			dir := fmt.Sprintf("%s:%d", ip, PUERTO)

			cx, conerr := net.DialTimeout("tcp", dir, time.Second*1)
			if conerr == nil {

				fmt.Println(ip)
				cx.Close()

			}

		}()

	}
	wg.Wait()
	fmt.Scanln()

}

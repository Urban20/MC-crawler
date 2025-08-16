package main

/*
programa simple pensado para utilizar de forma automatizada con python
permite escanear rangos de ips especificos
*/
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
	STDOUT = "ip_escan.data" // donde se desvia el stdout, no modificar
)

var n0 = flag.Int("n0", 0, "")
var n1 = flag.Int("n1", 0, "")
var n2 = flag.Int("n2", 0, "") // solo se usa en barrido /24

var hl = flag.Int("hl", 50, "")

// barridos

var b24 = flag.Bool("b24", false, "") // booleano que se habilita para barrer en /24

// barrido n0.n1.n2.0/24
func Barrido24(n1 int, n2 int, n3 int) chan string {
	ipv4 := make(chan string)
	go func() {
		defer close(ipv4)

		for x := range 255 {
			ip := fmt.Sprintf("%d.%d.%d.%d", n1, n2, n3, x)

			ipv4 <- ip
		}

	}()
	return ipv4

}

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

func Ejecucion24(n1 int, n2 int, n3 int, lim chan struct{}) {

	wg := sync.WaitGroup{}

	for ip := range Barrido24(n1, n2, n3) {

		lim <- struct{}{}
		wg.Add(1)

		go func() {
			defer wg.Done()
			defer func() { <-lim }()

			dir := fmt.Sprintf("%s:%d", ip, 25565)
			cx, conerr := net.DialTimeout("tcp", dir, time.Millisecond*300)
			if conerr == nil {
				defer cx.Close()
				fmt.Println(ip)
			}

		}()

	}

	wg.Wait()
}

func Ejecucion16(n0 int, n1 int, lim chan struct{}) {
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
				defer cx.Close()
				fmt.Println(ip)

			}

		}()

	}
	wg.Wait()

}

func main() {
	flag.Parse()
	n0 := *n0
	n1 := *n1
	n2 := *n2 //solo se usa en barrido 24
	hl := *hl
	b24 := *b24 // booleano que habilita el barrido /24 , por defecto se usa /16

	arch, _ := os.OpenFile(STDOUT, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

	os.Stdout = arch

	lim := make(chan struct{}, hl)

	if b24 {

		Ejecucion24(n0, n1, n2, lim)

	} else {

		Ejecucion16(n0, n1, lim)
	}

}

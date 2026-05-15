package main

/*
programa simple pensado para utilizar de forma automatizada con python
permite escanear rangos de ips especificos
*/
import (
	"flag"
	"fmt"
	"net"
	"sync"
	"time"
)

const (
	PUERTO  = 25565
	VERSION = "V4.0" //version del escaner, debe coincidir con el resto del programa
)

var n0 = flag.Int("n0", 0, "")
var n1 = flag.Int("n1", 0, "")
var n2 = flag.Int("n2", 0, "") // solo se usa en barrido /24
var tiempo = flag.Int("t", 300, "")
var vr = flag.Bool("v", false, "")

var hl = flag.Int("hl", 50, "")

// barridos

var b24 = flag.Bool("b24", false, "") // booleano que se habilita para barrer en /24
var b8 = flag.Bool("b8", false, "")   // booleano que se habilita para barrer en /8

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

func Barrido8(n int) chan string {

	// n.i3.i2.i1/8

	var long int = 255

	var i1, i2, i3 int = long, long, long
	var ip = make(chan string)

	go func() {

		defer close(ip)

		for i3 >= 0 {
			i1--
			if i1 < 0 {
				i1 = long
				i2--

				if i2 < 0 {
					i2 = long
					i3--
				}

			}

			ip <- fmt.Sprintf("%d.%d.%d.%d", n, i3, i2, i1)

		}

	}()

	return ip
}

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

	return ip

}

func Ejecucion(generador chan string, lim chan struct{}, timeout time.Duration) {
	wg := sync.WaitGroup{}

	for ip := range generador {
		wg.Add(1)
		lim <- struct{}{}
		go func() {

			defer wg.Done()
			defer func() { <-lim }()

			dir := fmt.Sprintf("%s:%d", ip, PUERTO)

			cx, conerr := net.DialTimeout("tcp", dir, time.Millisecond*timeout)
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
	b8 := *b8
	timeout := *tiempo // tiempo en miliseg
	version := *vr

	if version {
		fmt.Println(VERSION)
		return
	}

	lim := make(chan struct{}, hl)

	var gen chan string

	if b24 {

		gen = Barrido24(n0, n1, n2)

	} else if b8 {

		gen = Barrido8(n0)

	} else {

		gen = Barrido16(n0, n1)
	}

	Ejecucion(gen, lim, time.Duration(timeout))
}

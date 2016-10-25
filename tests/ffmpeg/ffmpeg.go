package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func printStdoutOneline() {
	fmt.Fprint(os.Stdout, "This is printed to stdout")
}

func printStderrOneline() {
	fmt.Fprint(os.Stderr, "This is printed to stderr")
}

func printStdoutMultiline() {
	fmt.Fprint(os.Stdout, "These are\nmultiple lines\nprinted to stdout")
}

func printStderrMultiline() {
	fmt.Fprint(os.Stderr, "These are\nmultiple lines\nprinted to stderr")
}

func main() {
	args := os.Args[1:]

	if len(args) == 0 {
		os.Exit(0)
	}

	var stdIn, stdOut, stdErr, exitCode string
	longRun := false

	for i, arg := range args {
		switch arg {
		case "--stdin":
			stdIn = args[i+1]
		case "--stdout":
			stdOut = args[i+1]
		case "--stderr":
			stdErr = args[i+1]
		case "--exit-code":
			exitCode = args[i+1]
		case "--long-run":
			longRun = true
		}
	}

	if stdIn == "pipe" {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			fmt.Fprintln(os.Stdout, scanner.Text())
		}
	}

	if stdOut == "oneline" {
		printStdoutOneline()
	} else if stdOut == "multiline" {
		printStdoutMultiline()
	}

	if stdErr == "oneline" {
		printStderrOneline()
	} else if stdErr == "multiline" {
		printStderrMultiline()
	}

	if longRun {
		for {
		}
	}

	code, _ := strconv.Atoi(exitCode)
	os.Exit(code)
}

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

	stdin := args[1]
	stdout := args[3]
	stderr := args[5]
	exitCode := args[7]

	if stdin == "pipe" {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			fmt.Fprintln(os.Stdout, scanner.Text())
		}
	}

	if stdout == "oneline" {
		printStdoutOneline()
	} else if stdout == "multiline" {
		printStdoutMultiline()
	}

	if stderr == "oneline" {
		printStderrOneline()
	} else if stderr == "multiline" {
		printStderrMultiline()
	}

	code, _ := strconv.Atoi(exitCode)
	os.Exit(code)
}

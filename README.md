**README.md**

# Repository Overview

This repository contains a collection of utility scripts designed to streamline various tasks and enhance productivity.

## Available Scripts

### add
* **Purpose:** Creates and adds predefined files to the current directory/project.
* **Functionality:** Leverages modules and imports from the `./static/defaults` directory.

### ascii
* **Purpose:** Displays an ASCII table or provides ASCII values for given input.
* **Usage:**
  - To display the ASCII table: `ascii`
  - To get the ASCII value of a character: `ascii 'a'`

### ctx
* **Purpose:** Adds context functionality by adding a utility function to your path.
* **Functionality:** Similar to a conda environment, it provides a convenient way to manage project-specific contexts.

### dfmt
* **Purpose:** Docker format utility for the `--format` flag.
* **Functionality:** Simplifies formatting Docker output.

### google
* **Purpose:** Quickly performs Google searches and accesses predefined websites from the terminal.
* **Usage:**
  - To search for a query: `google what is the fastest mamel in the world`
  - To access a predefined website: `google drive`

### gutil
* **Purpose:** GitHub utility functions for managing a directory of Git repositories.
* **Functionality:** Originally used for grading student labs, these functions can pull all repositories, run tests, and push results.

### pawk
* **Purpose:** Execution tool for Pawk, a Python-based AWK-like tool.
* **Functionality:** Provides a powerful and flexible way to process text data.

### run
* **Purpose:** Quickly compiles and/or runs scripts and applications.
* **Functionality:** Streamlines the execution process.

## Usage Instructions
To use these scripts locally:

1. clone the git repository:
```bash
cd $HOME
git clone https://github.com/cswaltzinger/csw-bin 

```
2. Add the repo to your `$PATH` enviornmnet variable by adding the following line of code to your .zshrc, .bashrc, or other shell config file.
```bash
export PATH=$HOME/csw-bin:$PATH
```
3. Reset your shell or run `source <config-file>` where config-file is the config file you just modified.  Now you should be able to run all commands in this repository.  

**NOTES:** 
 - You may need to allow yourself to run the scripts by using the `chmod` command.  Simply run:
 `chmod u+x ./*` to allow yourself to exec all the commands in the repository.  
 - You may also need to install additional packages as well such as python, make, docker to get the full functionality of the repository.  

 ### EXAMPLES:

### add:
Suppose you want to make several java classes that share mostly the same imported classes.  

With `add` it can be as simple as the following program:
```bash
add --modules 'scn list r' first.java -m='m ex arr hm' second.java
```
This will create `first.java` that imports java.util.Scanner, java.util.List, and java.util.Random in addtion to `second.java` that imports java.util.Scanner, java.util.List, java.util.Random, java.lang.Math, java.lang.Exception, java.util.ArrayList, and java-hm java.util.HashMap.  

### dfmt
Suppose you want to see specific aspects of docker images such as thier id, Repository, Size, Containers, and SharedSize.  Normally, you would need to run something along the lines of :
```bash
docker imsage ls -a --format "table {{.ID}}\t{{.Repository}}\t{{.Size}}\t{{.Containers}}\t{{.SharedSize}}"
```
dfmt or docker-format helps allieviate this problem by compressing the table description into a function with numerious aliases.  The above command would then simplify to:
```bash
docker container ls -a --format "table $(dfmt i repo sz cont ssize)" 
```
or without using the aliases:
```bash
docker container ls -a --format "table $(dfmt i repository size containers sharedSize)" 
```

### pawk

Parse large text and files with the pawk utility.  Based on the `awk` function, `pawk` or python-awk provides similar functionality.  Suppose you wanted to extract all headings from this README.md file.  With `pawk` it is as simple as the following:

```bash
cat README.md | pawk '
if inp.startswith("###"):
    print(inp)
'
```
Alternatively, `pawk` also can also be given python boolean expression and print the input line by default while achiving similar functionality:

```bash
cat README.md | pawk 'inp.startswith("###")'
```
In addition, `pawk` also can also be given python boolean expression and object(s) to print as a result by using the printif functionality : 

```bash
cat README.md | pawk 'printif inp.startswith("###"), line[-1]'
```



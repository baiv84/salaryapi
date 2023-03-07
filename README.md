# Description

`salaryapi` is a console tool to prepare job market statistics from 2 most popular vacancies search sites: [hh.ru](https://hh.ru/) and [superjob.ru](https://superjob.ru/)

The tool shows tables, filled with software engineers month salary rates for most popular programming languages. 

This statistics based on Moscow labor market, all vacancies being taken into account have salary fork and publishing date no longer then 1 month.

# Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

# Prerequisites

Firstly, we need to install package `python3-venv` to work with python virtual environment.

Please, update packages on your system `!(it depends on your operating system)`

as for me, I use Ubuntu as a host operating system. 

So I run:
```console
$ sudo apt update
```

and install python virtual environment package:
```console
$ sudo apt install -y python3-venv
```

Then jump to project folder:
```console
$ cd salaryapi
```

and create new virtual environment to run the code:
```console
$ python3 -m venv venv
```

Activate new virtual environment:
```console
$ source venv/bin/activate
```

As a result, you will see command line prompt like this:
```console
(venv) salaryapi $ 
```

# Install dependencies

In the virtual environment run command:

```console
(venv) salaryapi $  pip install -r requirements.txt
```

This command installs all necessary libraries (`requests`, `environs`, `terminaltables`) into the `venv` environment.

# Setup environment variables

To work with [superjob.ru API](https://api.superjob.ru/) we need to define `SUPERJOB_API_KEY` environment variable.

To do this, in project folder create new file with name - `.env` and add the line:

```
SUPERJOB_API_KEY=xxxx
```

where `xxxx` - please, replace with your personal token value.

Save and close the file, go ahead with running program.

---

# Run program 

To run program, in console execute command:

```console
(venv) salaryapi $ python salary.py
```

# Control results

If program runs successfully, you will see the results like these:

![Alt text](img/1.png?raw=true "salaryapi")


# Final steps

Deactivate virtual environment:

```console
(venv) salaryapi $ deactivate
```

Close console:
```console
$ exit
```
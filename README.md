
# PDFTool

This project is a small tool written in [Python 3.10](https://www.python.org/) that can perform operations on PDFs that I personally need quite often.

It has a small TUI using [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) and [clintermission](https://github.com/sebageek/clintermission) (which uses the former) to select, configure and execute the operations.
For manipulating the PDFs it uses [pypdf](https://github.com/py-pdf/pypdf).



## Installation

#### Requirements: python, pip, (pipenv)

There are multiple ways to install and run the project. Since I use [pipenv](https://github.com/pypa/pipenv) it is probably the easiest and most straightforward way to also use it. Other than that you can also use your favorite tool using the provided requirements.txt (given that the tool supports that) or just plain old pip.

Besides that there is also a .spec-file provided for use using [pyinstaller](https://github.com/pyinstaller/pyinstaller) to create a single executable. To do so the development requirements are also needed. Please refer to requirements-full.txt.

In general, it is recommended to use a [virtual environment](https://docs.python.org/3.10/library/venv.html) (pipenv does this automatically, for other tooling/pip you might have to do this by yourself).

### Running using pipenv
```bash
pipenv install
pipenv run python pdftool/main.py
```

### Building an executable [recommended]
```bash
pipenv install -d
pipenv run pyinstaller pdftool.spec
```
After running the commands there should be an executable file in the dist folder. You can add it to your PATH variable to invoke it from anywhere.

## Features/Usage

I tried to make the tool easy, self-explanatory and straightforward to use, which resulted in a kind of guided way through the different operations.

After executing the tool (see section [Installation](https://github.com/moritz-baumgart/PDFTool#Installation) above). You will be greeted by the main menu from where you can select which operation you want to perform using the arrow keys and enter. Currently, there are the following operations supported:
- #### Merging
    - Merge multiple PDFs into a single one.
    - You can specify single files and/or (a) complete folder(s).
    - When specifying  (a) folder(s) the tool will search for and merge all PDFs inside it/them in the order they are given.
- #### Reordering Dual Page Scans
    - This feature was mainly implemented, because the document feeder of my scanner does not support scanning sheets that are printed on both sides.
    - To solve this issue I just put a stack of sheets through the feeder and then flip it around, scan the backsides and append them to the document. After that, this operation can be used to put the sheets back in order.
    - If some of the sheets don't have a backside (i.e. an empty backside), you can remove them using the "delete pages" operation below.
    - Generally if you have a PDF with pages ordered in the following style, with pn being the n-th page and the suffixes f and b standing for front and back respectively:
        - p1f, p2f, p3f, ..., p3b, p2b, p1b, ...
    - ..., then you can use this operation to reorder them, resulting in the following order:
        - p1f, p1b, p2f, p2b, p3f, p3b, ...
- #### Delete pages
    - Deletes the pages with the given indices (starting with 1) from the given file.

## Author

- [@moritz-baumgart](https://github.com/moritz-baumgart)


## Acknowledgements

- [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
- [clintermission](https://github.com/sebageek/clintermission)
- [pypdf](https://github.com/py-pdf/pypdf)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

# Python

Python is a bad programming language that unfortunately is very popular among data people. As such, if you're making a machine learning project you're likely going to have to work with Python.
This will serve as an introduction and a few tips to hopefully make the experience less painful.

## Installation

## Set Up

Once Python is installed, you're ready to work. However running many `pip install` will get up to you eventually. I recommend **always** creating virtual environments for every python project, local installations of python with local libraries independent of the global ones on the computer.
To create and activate a virtual environment under the `backend` directory:

```bash
cd backend
python -m venv .venv

# Activation on Linux
source .venv/bin/activate
# Activation on Windows
.\.venv\Scripts\activate
```

Then all the libraries you need to install for the project to work are tracked in the `backend/requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Type Check

When opened in VSCode and the proper extension is installed type checking will be run on python code, to help catch sooner wrong function call, assingments, implementations, and so on...
This behaviour is configured in the `.vscode/settings.json` file with:

```
{
  ...
  "python.analysis.typeCheckingMode": "standard",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    ...
  }
}
```

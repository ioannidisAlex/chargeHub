# tlmpa

With your global version of Python

```python
python -m pip install nox,pre-commit
```

Or if you're in Windows

```python
py -3.7 -m pip install nox,pre-commit
```

then run

```python
pre-commit install
```

Now every time you commit isort and black are going to be running. A potential issue you might face is if they need to  modify file, the committee is going to fail and though the file will be styled properly, it will not be staged automatically so if you try to commit again the next commit is also going to fail. in order to resolve this 

```python
git update-index --again
```

and then commit normally

For more information #22




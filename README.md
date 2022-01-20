# python-unmarshal-decompile
Unmarshal and decompile Python script starting with exec(marshal.loads(...

- works with Python 2.X to 3.9
- using uncompyle6 (Python < 3.7) and decompyle3 (Python >= 3.7)

# Installation
```
pip install uncompyle6
pip install decompyle3
```

# Usage

given a file named "marshaledFile.py" like

```python
#!/usr/bin/env python
import marshal
exec(marshal.loads('c\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00@\x00\x00\x00s\x90\x00\x00\x00d...
```

call
```
python2 marshaledFile.py 27
```
output
```
unmarshal/decompile Python
open file marshaledFile.py
decompile Python 2.7 code with Python 2.7
write decompiled code to marshaledFile_decompiled.py
```


# or

given a file named "marshaledFile38.py" like

```python
#!/usr/bin/env python
import marshal
exec(marshal.loads(b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00@...
```

call
```
python3 marshaledFile.py 38
```
output
```
unmarshal/decompile Python
open file marshaledFile38.py
decompile Python 3.8 code with Python 3.9
write decompiled code to marshaledFile38_decompiled.py
```

which will look like
```python
# decompyle3 version 3.8.0
# Python bytecode 3.8
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: <source>

def test():
    return 0

print(test())
```




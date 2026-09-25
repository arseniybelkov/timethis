# timethis

```python
@timethis
def f():
    import time
    time.sleep(0.1)

f()

```
Logger output:
```bash
f @ /path/to/file.py:83 took 100.066931 ms.
```

You cab also use arbitrary names for logging.  
```python
@timethis("new_impl_of_f")
def f():
    ...
```  

As well as change the logger.  
```python
import logging
@timethis(log_callback=logging.info)
def f():
    ...
```

It might also be useful, if you want to profile some code snippet.  
```python
from collections import Counter
result = timethis("some_counter_work")(
    lambda: Counter([1, 1, 3]).most_common(1)[0]
)()
assert result[0] == 1
```
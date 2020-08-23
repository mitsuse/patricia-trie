# CHANGELOG

## 2014/12/14

### *Bugfix*

Added the missing README to PyPI package.(MANIFEST.in)


## 2014/09/15

### *Bugfix*:

Correct behaviour when using an exactly matching prefix as query (issue described in #1 by @zachrahan). Also fixes code-smells (PEP8, code complexity) and a failing test case code.


## yyyy/MM/dd

### *Bugfix*: Correct behavior when using a negative start index.

Added a comparison to `marisa-trie`_ - by now, it seems, patricia-trie is roughly only a factor two slower than the marisa-trie PyPI version wrapping a C library. Also makes it nice to compare the two usages.


## yyyy/MM/dd

### *Improvement*

Switched back to a very efficient internal dictionary implementation; Runs about two- to three times as fast as the two-tuple list from update 4 against the simple (and newly added) ``time_patricia.py`` "benchmark".


## yyyy/MM/dd

### *Feature*

Added optional keyword parameter ``end`` to the methods key(), keys(), item(), items(), value(), and values(), so it is not necessary to scan within a window::

```python
T.key('string', start=2, end=3, default=None)
T.keys('string', start=2, end=3)
```


## yyyy/MM/dd

### *Bugfix*

When splitting edges while adding a new key that is shorter than the current edge, a index error would have occurred.


## yyyy/MM/dd

### **Important API change**

item() now returns key, value pairs even when a default value is given, using ``None`` as the "key"::

```python
# Old behaviour was:
T.item('string', default=False) # False

# While now, the same call produces:
T.item('string', default=False) # None, False
```

### *Improvement*

Switched from using dictionaries to two-tuple lists internally (thanks to Pedro Gaio for the suggestion!) to improve the overall performance a bit (about 20% faster on simple tests). 


## yyyy/MM/dd

### *Feature*

optional keyword parameters to indicate an offset ``start`` when scanning a string with the methods key(), keys(), item(), items(), value(), and values(), so it is not necessary to slice strings for each scan:: 

```python
# Old usage to scan 'string' in 'the string' was:
T.keys('the string'[4:])

# With the new optional keyword parameter:
T.keys('the string', start=4)
```


## yyyy/MM/dd

- *Update*: Full documentation and corrections.


## yyyy/MM/dd

- Initial release.
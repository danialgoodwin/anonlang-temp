


### https://rosettacode.org/wiki/Temperature_conversion#Python

```
app() = input('Input K: ', float)
    then(k) output('Kelvin={}\nCelsius={}\nFahrenheit={}\nRankine='.format(k, k - 273.15, k * 1.8 - 459.67, k * 1.8))
loop True app()
 
loop True
    k = input('Input K: ') as float
        then output(f'Kelvin={k}\nCelsius={k - 273.15}\nFahrenheit={k * 1.8 - 459.67}\nRankine={k * 1.8}')

k = c + 273.15
k = (f + 459.67) / 1.8
k = r / 1.8
loop True
    input('<k|c|f|r> = <value>') as config
        then solve($variables, config)
        then output($variables)
```

### Tokenize a string
https://rosettacode.org/wiki/Tokenize_a_string#Python: `'.'.join('Hello,How,Are,You,Today'.split(',')'` 

https://rosettacode.org/wiki/Tokenize_a_string#Kotlin: `"Hello,How,Are,You,Today".split(',').joinToString(".")`

```
;; Anonlang knows the datatype `[String]`, thus is has `join()`. Or, maybe it assumes String?
'Hello,How,Are,You,Today'.split(',').join('.')
```

### CSV to HTML

https://rosettacode.org/wiki/CSV_to_HTML_translation#Python:
```python
csv = ''
html = '<table>\n'
for row in csv.split('\n'):
    html += '  <tr>'
    html += ''.join([f'<td>{data}</td>' for data in row.split(',')])
    html += '</tr>'
html += '</table>\n'
```

```java
String csv = "";
html = '<table>\n'
StringJoiner sj = new StringJoiner("</td><td>", "  <tr><td>", "</td></tr>") 
for row in csv.split('\n') {
  html += row.split(',').stream().collect(Collectors.joining("</td><td>", "<tr><td>", "</td></tr>"))
}
html += '</table>\n'
```

```anonlang
csv.split('\n').loop().split(',').join('</td><td>', '  <tr><td>', '</td></tr>').join('\n', '<table>\n', '\n</table>')
```

### Time a function
https://rosettacode.org/wiki/Time_a_function#Python
```python
import sys, timeit
...
```

```anonlang
myFunction() = {
  start = time.now()
  ;; Do stuff
  output(f'time = {time.now - start}')
}
```

### Sum to 100

https://rosettacode.org/wiki/Sum_to_100#Python

```anonlang

```

### [Sum of squares](https://rosettacode.org/wiki/Sum_of_squares)

https://rosettacode.org/wiki/Sum_of_squares#Kotlin
```kotlin
doubleArrayOf(1, 2, 3, 4, 5).map { it * it }.sum()
```

https://rosettacode.org/wiki/Sum_of_squares#Python
```python
sum(x * x for x in [1, 2, 3, 4, 5])
sum(x ** 2 for x in [1, 2, 3, 4, 5])
sum(pow(x, 2) for x in [1, 2, 3, 4, 5])
sum(map(lambda x: x ** 2, [1, 2, 3, 4, 5]))

# using reduce
from functools import reduce
powers_of_two = (x * x for x in [1, 2, 3, 4, 5])
reduce(lambda x, y : x + y, powers_of_two)
reduce(lambda a, x: a + x*x, [1, 2, 3, 4, 5])
```

```anonlang
[1, 2, 3, 4, 5].loop(it ** 2).sum()
[1, 2, 3, 4, 5].map(it ** 2).sum()
```


### [Strip comments from a string](https://rosettacode.org/wiki/Strip_comments_from_a_string)

https://rosettacode.org/wiki/Strip_comments_from_a_string#Python
```python
i = line.find('#')
if i >= 0:
    line = line[:i]
```

```anonlang
line.split(';;')[0]
```


### [Strip a set of characters from a string](https://rosettacode.org/wiki/Strip_a_set_of_characters_from_a_string)

```anonlang
text = 'The quick brown fox jumps over the lazy dog.'
remove = 'aei'
text = text.replace(r'[{remove}]', '')
```


### []()



### []()




### []()



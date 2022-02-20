# Funny Nation 代码规范

### 1 背景

本文档规定了代码的具体风格，在开发Funny Nation时，为了让其他人看得懂你的代码，请认真遵守本文档的规范。

如果你在代码中看到有人未遵守以下规定，记得提醒ta修改

### 2 命名

#### 2.1 使用英文的驼峰命名法

```python
someData = 1 # ✅

some_data = 1 # ❌

yiXieShuJu = 1 # ❌
```

#### 2.2 类名开头大写，其他变量名小写开头

```python
SomeData = 1 # ❌

class SomeData: # ✅

class someData: # ❌
```

#### 2.3 变量名尽可能包含详细信息

```python
data = 123 # ❌

dataFromGoogleAPI = 123 # ✅
```

### 3 Import的使用

#### 3.1 只允许绝对路径，不能用相对路径

```python
from src.utils.readConfig import getMajorConfig # ✅

from ..utils.readConfig import getMajorConfig # ❌
```

### 4 Typing的使用

#### 4.1 必须加Typing

```python
i = 1 # ❌

i: int = 1 # ✅
```

#### 4.2 Typing需要具体

```python
arr: list = [1, 2, 3] # ❌

from typing import List
arr: List[int] = [1, 2, 3] # ✅
```

#### 4.3 函数需要Typing

```python
def fun(i: int, j: int) -> int: # ✅
    return i + j

def fun(i, j): # ❌
    return i + j
```

### 5 注释

#### 5.1 必须用英文

```python
# This is a comment ✅

# 这是一个注释 ❌

# Zhe shi yi ge zhu shi ❌
```

#### 5.2 每一个函数都需要一个注释

```python
def fun(i: int, j: int) -> int: 
    return i + j
❌
```

```python
def fun(i: int, j: int) -> int: 
    """
    This is a function
    :param i: a number, int
    :param j: another number, int
    :return: the result of two parameters add up together. int
    """
    return i + j
✅
```

### 6 if的使用

#### 6.1 尽可能避免嵌套if

```python
if i == 0:
    if j == 0:
        print(i + j)
❌
```

```python
if i == 0 and j == 0:
    print(i + j)
✅
```

#### 6.2 在controller中，if用于判断异常条件，而不是判断成功条件，且经可能用return来代替else

```python
if len(moneyStrings) == 0:
    await message.channel.send("amountNotFound")
    return

if len(message.mentions) == 0:
    await message.channel.send("userNotFound")
    return

await message.channel.send("Done")

✅
```

```python
if len(moneyStrings) != 0:
    if len(message.mentions) != 0:
        await message.channel.send("Done")
    else:
        await message.channel.send("userNotFound")
else:
    await message.channel.send("amountNotFound")
    
❌
```

### 7 单元测试

#### 7.1 每一个单元测试需要以```filename_test.py```命名

```
filename_test.py ✅

filenametest.py ❌

filename.test.py ❌
```
# Funny Nation 代码规范

### 1 背景

本文档规定了代码的具体风格，在开发Funny Nation时，为了让其他人看得懂你的代码，请认真遵守本文档的规范。

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

#### 每一个函数都需要一个注释

```python
def fun(i: int, j: int) ->:
    return i + j
```
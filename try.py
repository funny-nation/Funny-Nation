import re

txt = '老板 sf'
result = re.match(r"^老板 (.+)$", txt)
print(result)

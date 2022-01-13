import re

command = "发红包 2000 3"

result = re.findall(f"^发红包 ([0-9]+) ([0-9]+)$", command)[0]
print(result)
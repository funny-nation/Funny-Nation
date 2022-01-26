import re
command = "领奖 内战 200"

result = re.findall(f"^领奖 (.+) ([0-9]+)$", command)
print(result)

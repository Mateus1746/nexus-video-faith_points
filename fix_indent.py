import sys

with open("web/app.js", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "window.__appReady = true;" in line:
        if i > 255:
            lines[i] = "    window.__appReady = true;\n"

with open("web/app.js", "w") as f:
    f.writelines(lines)

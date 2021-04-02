import os

text = """
# COVID19-ITALY-GRAPHS

## Epidemia

"""

epidemia = os.listdir("graphs/epidemia")
vaccini = os.listdir("graphs/vaccini")
epidemia.sort()
vaccini.sort()

for f in epidemia:
    f = f.replace(" ", "%20")
    #text += f"![{f[:-4]}](graphs/epidemia/{f})\n"
    text += f"### {f[:-4]}\n<img src=\"graphs/epidemia/{f}\" width=\"600\" height=\"500\"></img>\n"

text += "\n## Vaccini\n"

for f in vaccini:
    f = f.replace(" ", "%20")
    #text += f"![{f[:-4]}](graphs/vaccini/{f})\n"
    text += f"### {f[:-4]}\n<img src=\"graphs/vaccini/{f}\" width=\"600\" height=\"500\"></img>\n"

with open("README.md", "w") as f:
    f.write(text)
    
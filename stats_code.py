import sys

sum_file = 0
sum_code = 0

sys.stdin.__next__()
sys.stdin.__next__()

languages = ['JSON', 'Markdown']
partials = {}

for l in sys.stdin:
    file, language, blank, command, code = l.split(',')
    if language in languages:
        continue
    if language == "Bourne Shell":
        language = "Shell script"
    partials[language] = int(code)
    sum_code += int(code)
    sum_file += int(file)
    print ("\\textit{{{}}}\t&\t{}\t&\t{} \\\\".format(language, file, code.strip()))


print ("\midrule\nSUM\t&\t{}\t&\t{}\\\\ \\bottomrule".format(sum_file, sum_code))


res_percentage = []
for l, c in partials.items():
    perc = c / sum_code *100
    res_percentage.append((l, perc))
x = 5
rank = sorted(res_percentage, key=lambda x: x[1])

rankmax = rank[len(rank)-x:]
other = rank[0:-x]

#print(rankmax)
#print(other)

res = ""
for l,c in rankmax:
    res += "{:.2f}/{},".format(c,l)

sum =0
for l,c in other:
    sum += c

res += "{:.2f}/{}".format(sum,"Other")
print(res)

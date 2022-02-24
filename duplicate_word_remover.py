seen = set()

fname = input("What is the file name (include.txt)?: ")

with open(fname, "r") as fin, open(fname[:-3] + "_removed_duplicates", "w") as fout:
    for line in fin:
        # h = hash(line)
        if line not in seen:
            # fout.write(line)
            seen.add(line)
    fout.writelines(sorted(seen))

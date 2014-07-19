import argparse, sys
from parse_tex import render_math, TEX_MODE

desc = '''Transforms github with LaTeX as $$ into images'''.strip()

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('markdown', help='Input Markdown file')
args = parser.parse_args()

large_mag = 15000

def markdown_image(line,f_eq):
    eq = line.strip("$")
    base = '''!["{}"]({})\n'''
    return base.format(eq,f_eq)
    

def render_large(line):
    f_eq = render_math(line,
                    magnification=large_mag,
                    force=True)
    return markdown_image(line, f_eq)

with open(args.markdown) as FIN:
    new_lines = []
    
    for line in FIN:
        sline = line.rstrip()
        
        if sline and sline[0]=="$" and sline[-1] == "$":
            line = render_large(sline)

        new_lines.append(line)

output = "".join(new_lines)

# Overwrites the input file
with open(args.markdown,'w') as FOUT:
    FOUT.write(output)

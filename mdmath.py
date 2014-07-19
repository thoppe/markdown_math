import argparse, sys
from src.parse_tex import render_math, TEX_MODE
import bs4

desc = '''Transforms github with LaTeX as $$ into images'''.strip()

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('markdown',
                    nargs="?",
                    default="README.md",
                    help='Input Markdown file [uses README.md as default]')

parser.add_argument('--revert',
                    default=False,                
                    action="store_true",
                    help='Revert any changes made')

parser.add_argument('--force',
                    default=False,                
                    action="store_true",
                    help='Force rendering')

args = parser.parse_args()

large_mag = 2000

# This is what we look for to revert
paragraph_open_tag = '''<p align="center" class="mdequation">'''


def markdown_image(line,f_eq):
    base = '''{para_tag}<img src="{src}" alt="{alt}" /></p>'''
    return base.format(para_tag = paragraph_open_tag,
                       src=f_eq, alt=line)

def render_large(line):
    f_eq = render_math(line,
                    magnification=large_mag,
                    force=True)
    return markdown_image(line, f_eq)

def parse_md(f_md):
    new_lines = []

    with open(f_md) as FIN:
        for line in FIN:
            sline = line.rstrip()

            if sline and sline[0]=="$" and sline[-1] == "$":
                line = render_large(sline)

            new_lines.append(line)
    return "".join(new_lines)

def revert_md(f_md):
    new_lines = []

    with open(f_md) as FIN:
        for line in FIN:
            if paragraph_open_tag in line:
                soup = bs4.BeautifulSoup(line)
                line = soup.p.img["alt"] + '\n'
            new_lines.append(line)
    return "".join(new_lines)


# If forced, remove formatting first
if args.force:
    output = revert_md(args.markdown)
    with open(args.markdown,'w') as FOUT:
        FOUT.write(output)


output = (parse_md(args.markdown) if not args.revert else 
          revert_md(args.markdown))

# Overwrites the input file
with open(args.markdown,'w') as FOUT:
    FOUT.write(output)

import re, os, tempfile, shutil, sys
from extra_io import mkdir_p, run_shell, unique_filename

_render_dir = ".equations"

# %TEXT% mode which is the default LaTeX mode.
TEX_MODE = re.compile(r'(?=(?<!\\)\%).(.+?)(?<!\\)\%',
        re.MULTILINE | re.DOTALL)

# $MATH$ mode which is the typical LaTeX math mode.
MATH_MODE = re.compile(r'(?=(?<!\\)\$).(.+?)(?<!\\)\$',
        re.MULTILINE | re.DOTALL)

# %%PREAMBLE%% text that modifys the LaTeX preamble for the document
PREAMBLE_MODE = re.compile(r'(?=(?<!\\)\%\%).(.+?)(?<!\\)\%\%',
        re.MULTILINE | re.DOTALL)


_f_tex_template_base = "latex_template.tex"

def render_math(tex,
                color_rgb = (25,25,25), 
                extra_preamble="", 
                magnification=10000,
                verbosity=True,
                force=False):

    # Create the eq. directory if it doesn't exist
    mkdir_p(_render_dir)

    # Load the tex template
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    f_template = os.path.join(__location__,
                              _f_tex_template_base)
    
    with open(f_template) as FIN:
        tex_template = FIN.read()
    
    # Join the extra preamble if it is not a string
    try: extra_preamble = '\n'.join(extra_preamble)
    except: pass

    org_dir = os.getcwd()
    TEX_OUT = tex_template % (color_rgb[0],
                              color_rgb[1],
                              color_rgb[2],
                              extra_preamble,tex)
    hash_name = unique_filename(TEX_OUT) + '.png'

    f_png_final = os.path.join(org_dir,
                               _render_dir,
                               hash_name)

    # Use a relative path for f_png
    f_png_file_out = os.path.join(_render_dir, hash_name)
    
    # Do not render if already found
    if os.path.exists(f_png_final) and not force:
        return f_png_file_out

    # Output what we are doing if begin verbose
    if verbosity:
        print " + Rendering equation\n\t%s" % tex

    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)    

    tmp_file = tempfile.mktemp(dir=tmp_dir)
    with open(tmp_file, "w") as FOUT:
        FOUT.write(TEX_OUT)

    dvi = "%s.dvi" % tmp_file
    png = "%s.png" % tmp_file

    # Compile the version to latex
    cmd_tex = 'latex -halt-on-error %s'

    try:
        run_shell(cmd_tex, tmp_file)
    except:
        print "LaTeX render failure for (%s), log dump:"%tex
        os.system('grep -C 3 \! *.log')
        os.chdir(org_dir)
        return f_png_file_out

    # Run dvipng on the generated DVI file. Use tight bounding box.

    # Extract the image
    cmd_dvi  = "dvipng -q -T tight -bg Transparent -x %i -z 9 %s -o %s"
    args = (magnification, dvi, png)
    run_shell(cmd_dvi, args)

    shutil.copyfile(png, f_png_final)
    os.chdir(org_dir)

    return f_png_file_out

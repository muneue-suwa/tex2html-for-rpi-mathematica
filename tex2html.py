from pathlib import Path
import argparse

html_str = """
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Document</title>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>

<body></body>

</html>
"""


def main():
    """
    Main script
    """
    tex_filename = Path("test.tex")
    parser = argparse.ArgumentParser(
        description=(
            "Convert TeX file to HTML file for Mathematica in Raspberry Pi"
        )
    )
    parser.add_argument(
        "tex_filename", type=Path,
        help="Select target TeX filename"
    )
    args = parser.parse_args()
    # print(args.tex_filename)
    tex_filename = args.tex_filename
    if tex_filename.suffix != ".tex":
        raise Exception(f"Tex file is required: {tex_filename}")
    tex2html(tex_filename)


def tex2html(tex_filename: Path, html_str=html_str):
    """
    Create HTML file from TeX file
    """
    html_basename = f"{tex_filename.stem}.html"
    html_filename = tex_filename.parent / html_basename
    with open(tex_filename, "r") as tex_f:
        tex_lines = tex_f.readlines()
        do_add_line = False
        equation_str = ""
        for line in tex_lines:
            striped_line = line.strip()
            if striped_line == r"\begin{document}":
                do_add_line = True
                continue
            elif striped_line == r"\end{document}":
                break

            if do_add_line is True and striped_line != "":
                equation_str += striped_line

    with open(html_filename, "w") as html_f:
        html_str = html_str.replace(
            "<body></body>", f"<body>\n{equation_str}\n</body>"
        )
        html_f.write(html_str)


if __name__ == "__main__":
    main()

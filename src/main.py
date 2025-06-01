import os

from resume_parser.resume_parser import extract_text_from_pdf


def main():
    cwd = os.getcwd()
    path_to_pdf = os.path.join(cwd, "src/data/resume_ligne.pdf")
    pdf_text = extract_text_from_pdf(path_to_pdf)
    print(pdf_text)

if __name__ == "__main__":
    main()
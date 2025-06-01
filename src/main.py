import os

from resume_parser.resume_parser import ResumeParser


def main():
    cwd = os.getcwd()
    path_to_pdf = os.path.join(cwd, "src/data/resume_ligne.pdf")
    resume_parser = ResumeParser(ner_model_name="manishiitg/resume-ner")

    if os.path.exists(path_to_pdf):
        pdf_results = resume_parser.parse(path_to_pdf)
        if pdf_results:
            print("\n--- Parsed PDF Results ---")
            for key, value in pdf_results["entities"].items():
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()
import re
import pdfplumber

class PDFQuizConverter:

    def extract_text_from_pdf(self, pdf_file):

        text = ""

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text


    def split_into_questions(self, text):

        pattern = r'(?=Q\.?\s*\d+\)|Q\.?\s*\d+\.|Q\s*\d+|Question\s*\d+|\n\d+\.)'

        parts = re.split(pattern, text)

        questions = []

        for p in parts:

            p = p.strip()

            if len(p) > 20:
                questions.append(p)

        return questions


    def parse_single_question(self, block):

        lines = [x.strip() for x in block.split("\n") if x.strip()]

        if len(lines) < 2:
            return None

        question = ""
        options = []
        answer = None

        option_started = False

        for line in lines:

            if re.match(r'^\(?[A-Da-d]\)', line):

                option_started = True
                options.append(line)

            elif re.match(r'^[A-Da-d][\.\)]', line):

                option_started = True
                options.append(line)

            elif line.lower().startswith("answer"):

                m = re.search(r'[A-D]', line,re.I)

                if m:
                    answer = m.group().upper()

            else:

                if option_started:

                    if len(options):

                        options[-1] += " " + line

                else:

                    question += " " + line

        return {

            "question": question.strip(),

            "options": options,

            "correct_answer": answer,

            "explanation":""

        }

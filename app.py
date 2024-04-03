from flask import Flask, render_template, request
import PyPDF2
import spacy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file.filename != '':
            pdf_text = extract_text(file)
            summary, keywords = process_text(pdf_text)
            return render_template('result.html', summary=summary, keywords=keywords)
    return render_template('index.html')

def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text += page.extract_text()
    return text

def process_text(text):
    nlp = spacy.load('xx_ent_wiki_sm')
    nlp.add_pipe('sentencizer')  # Add the sentencizer component
    doc = nlp(text)
    summary = " ".join(sent.text for sent in list(doc.sents)[:100])  # Get first 100 sentences as summary
    keywords = [token.text for token in doc if not token.is_stop and token.is_alpha][:5]  # Extract keywords
    return summary, keywords

if __name__ == '__main__':
    app.run(debug=True)

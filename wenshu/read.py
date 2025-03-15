import sys
import csv
import ollama
import spacy

csv.field_size_limit(sys.maxsize)

if __name__ == '__main__':
    csv_file_path = sys.argv[1]
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(row[-2])
            if len(row[-1]) > 1000:
                nlp = spacy.load('zh_core_web_sm')
                doc = nlp(row[-1])
                print(doc.text)
                for token in doc:
                    print(token.text, token.pos_, token.dep_)
                response = ollama.generate(model='llama3.2', stream=False, prompt='summarize the following in <= 200 English words:' + row[-1])
                print(response['response'])
                break

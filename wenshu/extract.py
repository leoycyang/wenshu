import sys
import csv
import ollama
import spacy
import re

csv.field_size_limit(sys.maxsize)

if __name__ == '__main__':
    csv_file_path = sys.argv[1]
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            match = re.search('指导.{0,10}案例', row[-1])
            if match is None:
                continue
            title_match = re.search('《([^》]*)》.{0,50}指导.{0,10}案例', row[-1])
            if title_match is not None:
                print(title_match.group(0))
                print(title_match.group(1))
                continue
            title_match1 = re.search('(第\d*[^。》]{0,50}指导[^》]{0,10}案例)', row[-1])
            if title_match1 is not None:
                print(title_match1.group(1))
                continue
            title_match2 = re.search('(\d*号[^。》]{0,20}指导[^》]{0,10}案例)', row[-1])
            if title_match2 is not None:
                print(title_match2.group(1))
                continue
            title_match3 = re.search('(第\d*.{0,20}《[^》]*》.{0,20}指导.{0,10}案例)', row[-1])
            if title_match3 is not None:
                print(title_match3.group(1))
                continue
            # print(row[-2])
            # if len(row[-1]) > 1000:
            #     nlp = spacy.load('zh_core_web_sm')
            #     doc = nlp(row[-1])
            #     print(doc.text)
            #     for token in doc:
            #         print(token.text, token.pos_, token.dep_)
            #     response = ollama.generate(model='llama3.2', stream=False, prompt='summarize the following in <= 200 English words:' + row[-1])
            #     print(response['response'])

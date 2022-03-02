import csv
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=str, 
        help="Previous attempts (comma separated <word>:<colour result codes>, e.g. adieu:gbbyb,groan=bbbyy)",
        default='')
    parser.add_argument("--letter",
        type=str,
        help="Single character to give options for next guesses",
        required=True)
    
    return parser.parse_args()

def get_rawdata (): 
    words=[]
    with open('data.csv', newline='') as csvfile:
        rawdata = csv.reader(csvfile, delimiter=',')
        for row in rawdata:
            for word in row:
                words.append(word)
    print( f"Raw data has {len(words)} words")
    return words

def get_possibles(letter, words):
    print (f"Searching {len(words)} for occurrences of letter '{letter}':")
    possibles = { 0 : [], 1: [], 2 : [], 3 : [], 4: []}
    discarded = []
    for word in words:
        l = [idx for idx, item in enumerate(word) if letter in item]
        if len(l) > 0:
            for idx in l:
                possibles[idx].append(word)
        else:
            discarded.append(word)

    return { 'possible' : possibles, 'discards': discarded}

def report_results(possibles, desc):
    descriptions = ['first', 'second', 'third', 'fourth', 'last']
    for key in possibles.keys():
        print( f"Possibilities for {descriptions[key]} letter given {desc}:")
        print( sorted(possibles[key]))

def get_list(wordlist, letter, pos, status):
    words = []
    if status in ['y', 'g']:
        for word in wordlist:
            if check_word(word, letter, pos) == status:
                words.append(word)
    else:
        raise ValueError(f"Use remove_words to remove letter with status {status}")
    return words

def remove_words(words, removelist):
    newdata = []
    for word in words:
        if not any(x in word for x in removelist):
            newdata.append(word)
    return newdata

def check_word(word, letter, pos):
    l = [idx for idx, item in enumerate(word) if letter in item]
    if len(l) > 0 :
        for idx in l:
            if idx == pos:
                return 'g'
        return 'y'
    else:
        return 'b'

def get_testwords(results):
    testwords=[]
    for item in results:
        (k,v), = item.items()
        testwords.append(k)
    return testwords

def build_results(res_str):
   
    results = []
    if not res_str:
        return results

    values = res_str.split(',')
    for value in values:
        parts = value.split(':')
        if len(parts) == 2 and len(parts[0]) ==5 and len(parts[1])==5:
            word = parts[0]
            codes = parts[1]
            if any( c  for c in codes if c not in ['b', 'g', 'y']):
                raise ValueError(f"Unexpected character code in result '{value}'")
            results.append({ word: codes})
        else:
            raise ValueError(f"Unexpected length in result '{value}'")
    return results

def process_results(results):
    words = get_rawdata()

    for result in results:
        blist = []
        (testword, colours), = result.items()
        for idx, letter in enumerate(testword):
            status = colours[idx]
            if status == 'b':
                blist.append(letter)
            else:
                words = get_list(words, letter, idx, status)
        words=remove_words(words, blist)
        print( f"Number of words remaining after analysing '{testword}': {len(words)}")
    return words
    
def main():
    args = get_args()
    results = build_results(args.results)
    words=process_results(results)

    letter = args.letter
    ideas = get_possibles( letter, words)
    report_results(ideas['possible'], f"letter '{letter}' and results {get_testwords(results)}")

if __name__ == '__main__':
    main()
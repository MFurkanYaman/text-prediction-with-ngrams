import os
import dill
import config
from pynput import keyboard
from nltk import ngrams

path = config.SAVEFILE
fileExtension = config.FILEEXTENSION
rateDict = {}
rateDice={}

loaded_ngram_list = []
word = ""
ngramToWords = []
flag = True
oldWord=""

def load_dataset(word):
    """pkl dosyasını yükler ve ngram listesini döndürür."""
    global path, fileExtension
    file = path + word.lower() + fileExtension
    with open(file, "rb") as f:
        loaded_ngram_list = list(dill.load(f))
    return loaded_ngram_list

def jaccard_score(input_ngram, data_ngram):
    """Jaccard skoru hesaplar."""
    intersection = len(input_ngram.intersection(set(data_ngram)))
    union = len(input_ngram.union(set(data_ngram)))
    return intersection / union

def Dices_Coefficient(input_ngram, data_ngram):
    intersection = len(input_ngram.intersection(set(data_ngram)))*2
    cluster1=len(input_ngram)
    cluster2=len(data_ngram)
    total=cluster1+cluster2
    return intersection/total


def ngram_to_words(sorted_ngram_values):
    """Ngram çiftlerini kelimeye çevirir."""
    words = []
    for ngram, _ in sorted_ngram_values:
        ngramword = ngram[0][0]  
        for pair in ngram:
            ngramword += pair[1]  
        words.append(ngramword)
    return words

def handle_special_keys(key):
    """Boşluk ve silme gibi özel tuşlara göre işlemler yapar."""
    global word, flag,oldWord
    print("Kullanıcı:", oldWord,word)
    if key == keyboard.Key.space:
        word+=" "
        oldWord+=word
        word=""
        flag = True
    elif key == keyboard.Key.backspace:
        word = word[:-1]
        if word=="":
            flag=True
    elif key == keyboard.Key.esc:
        quit()
    print(word)

def on_press(key):
    """Her tuş basımında ngram oluşturur ve öneriler gösterir."""
    
    global word, flag, loaded_ngram_list, rateDict, rateDice

    try:
        os.system('cls')
        word += key.char       
        print("Kullanıcı:", oldWord,word)
        print("\n---Öneriler---")

        input_ngram = set(list(ngrams(word, 2)))
        
        if flag:
            loaded_ngram_list = load_dataset(word)
            flag = False

        rateDict.clear()
        rateDice.clear()

        for data_ngram in loaded_ngram_list:
            rate = jaccard_score(input_ngram, data_ngram)
            rate2=Dices_Coefficient(input_ngram, data_ngram)
            rateDice[tuple(data_ngram)] = rate2
            rateDict[tuple(data_ngram)] = rate

        sorted_by_values = sorted(rateDict.items(), key=lambda item: item[1], reverse=True)[:3]
        sorted_by_values2 = sorted(rateDice.items(), key=lambda item: item[1], reverse=True)[:3]
        ngramToWords = ngram_to_words(sorted_by_values)
        ngramToWords2=ngram_to_words(sorted_by_values2)
        print("---Jaccard Similarty---")
        for suggestion in ngramToWords:
            print(suggestion)
        print("\n ---Dice Coefficient---")
        for suggestion in ngramToWords2:
            print(suggestion)

    except AttributeError:
        handle_special_keys(key)

def start_keyboard_listener():
    """Klavye dinleyiciyi başlatır."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

start_keyboard_listener()

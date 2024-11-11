import os
import dill
import config
from pynput import keyboard
from nltk import ngrams

#Kelime ilk harf boşluk ve silme karakter hatası fixle
#yabancı karakter fixle


rateJaccard = {}
rateDice={}
loaded_ngram_list = []
word = ""
ngramToWords = []
flag = True
oldWord=""
deleteCheck=False

def load_dataset(word):
    """pkl dosyasını yükler ve ngram listesini döndürür."""
    
    path=config.SAVEFILE
    fileExtension=config.FILEEXTENSION
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
    global word, flag,oldWord,deleteCheck

    print("Kullanıcı:", oldWord,word)

    if key == keyboard.Key.space:
            
        word+=" "
        oldWord+=word
        input_ngram=inputToNgram(word)
        get_similarity_suggestions(input_ngram)
        word=""
        flag = True
        

    elif key == keyboard.Key.backspace:
        deleteCheck=True 

        os.system('cls')
        
        word = word[:-1]
        input_ngram=inputToNgram(word)
        print("Kullanıcı: ", oldWord,word) # silmede output burda tetikleniyor
        get_similarity_suggestions(input_ngram)
    
        deleteCheck=False
        if word=="":
            flag=True
              
    elif key == keyboard.Key.esc:
        os.system('cls')
        print("Code execution stopped")
        quit()

def sortAndCombine(rateJaccard,rateDice):
    sorted_by_values_jaccard = sorted(rateJaccard.items(), key=lambda item: item[1], reverse=True)[:3]
    sorted_by_values_dice = sorted(rateDice.items(), key=lambda item: item[1], reverse=True)[:3]
    ngramToWords_J = ngram_to_words(sorted_by_values_jaccard) #jaccard
    ngramToWords_D=ngram_to_words(sorted_by_values_dice)  #Dice
    return ngramToWords_J,ngramToWords_D

def get_similarity_suggestions(input_ngram):
    global word, flag, loaded_ngram_list, rateJaccard, rateDice
    if flag:
        loaded_ngram_list = load_dataset(word)
        flag = False

    rateJaccard.clear()
    rateDice.clear()

    for data_ngram in loaded_ngram_list:
        rate_J = jaccard_score(input_ngram, data_ngram)
        rate_D=Dices_Coefficient(input_ngram, data_ngram)

        rateDice[tuple(data_ngram)] = rate_J
        rateJaccard[tuple(data_ngram)] = rate_D

    ngramToWords_J,ngramToWords_D=sortAndCombine(rateJaccard,rateDice)
    
    print("---Jaccard Similarty---")
    for suggestion in ngramToWords_J:
        print(suggestion)
    print("\n ---Dice Coefficient---")
    for suggestion in ngramToWords_D:
        print(suggestion)

def inputToNgram(word,n=2):
    input_ngram = set(list(ngrams(word, n)))
    return input_ngram

def on_press(key):
    """Her tuş basımında ngram oluşturur ve öneriler gösterir."""
    
    global word, flag, loaded_ngram_list, rateJaccard, rateDice, input_ngram

    try:
        os.system('cls')

        word += key.char  

        if deleteCheck==False:
            print("Kullanıcı:", oldWord,word)
        
        input_ngram=inputToNgram(word)

        get_similarity_suggestions(input_ngram)
   
    except AttributeError:
        
        handle_special_keys(key)
        
        

def start_keyboard_listener():
    """Klavye dinleyiciyi başlatır."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

start_keyboard_listener()

import time
import os
import logging
import dill
from nltk import ngrams
import config 

# 114 saniye sürdü.

def generate_bigrams_from_words(datasetPath):

    """
    Verilen bir dosya yolundan Türkçe kelimeler okur ve her kelimenin bigramlarını oluşturur.

    Parametreler:
        datasetPath (str): Kelimelerin okunduğu dosyanın yolu.
    
    Return Değeri:
        word_list (list): Her kelimenin bigramlarını içeren bir liste. Her öğe bir kelimenin bigram listesi olur.
    """

    try:
        data = open(datasetPath, 'r',encoding="utf-8").read().splitlines()
    except Exception as e:
        logging.error(f"Dataset dosyası açılırken hata: {e}")
        return []

    word_list=[]

    for value in data:
        ngrammer=list(ngrams(value,n=2))
        if not ngrammer:
            continue
        word_list.append(ngrammer)

    return word_list
    

def save_words_by_first_letter(word_list,save_file,fileExtension):

    """
    Kelimeleri ilk harflerine göre gruplar ve her grubu bir .pkl dosyasına kaydeder.
    
    Parametreler:
        word_list (list): Bigram listelerini içeren kelime listesi.
        save_file (str): Kaydedilecek dosyaların dizini.
        fileExtension (str): Dosyaların uzantısı.
    """

    if not os.path.exists(save_file):
        os.makedirs(save_file)

    save_list=[]
    first_letter=word_list[0][0][0]
    isLetterChange=False

    try:
        for word in word_list:
            
            if isLetterChange==True:
                first_letter=word[0][0]
                isLetterChange=False
                print("Harf Değişti: ",first_letter)
        
            if first_letter==word[0][0]:
                save_list.append(word)
            else:
                
                file_name=first_letter+fileExtension
                save_path=save_file+file_name

                with open(save_path,"wb") as f:
                    dill.dump(save_list,f)
                save_list=[]
                save_list.append(word)
                isLetterChange=True


        file_name=first_letter+fileExtension
        save_path=save_file+file_name

    
        with open(save_path,"wb") as f:
            dill.dump(save_list,f)

    except Exception as e:
        logging.error(f"{file_name} kaydedilirken hata: {e}")



def main():

    """
    Programın ana fonksiyonu.
    
    Yaptığı İşlemler:
        - Loglama ayarlarını yapılandırır.
        - Kelime listesini oluşturur ve bigram'ları alır.
        - Kelimeleri ilk harflerine göre .pkl dosyalarına kaydeder.
        - Çalışma süresini ölçer ve ekrana yazar.
    """

    start=time.time()

    config.setup_logging()
    word_list=generate_bigrams_from_words(config.DATASETPATH)
    save_words_by_first_letter(word_list,config.SAVEFILE,config.FILEEXTENSION)

    end=time.time()
    print("Execution Time: ", end-start)




if __name__=="__main__":
    main()
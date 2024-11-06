import logging

DATASETPATH="ngram/full_words_tr.txt"
SAVEFILE="pkl_files/"
FILEEXTENSION="_ngram_file.pkl"
LOG_FILE="wordguess/log file/app_errors.log"





def setup_logging(log_file=LOG_FILE,level=logging.INFO):
    """
    Bu fonksiyon, loglama ayarlarını yapılandırır.

    Parametreler:
        log_file: Logların kaydedileceği dosyanın yolu (varsayılan config.LOG_FILE).
        level: Loglama seviyesi (varsayılan INFO).

    Yaptığı İşlemler:
        1. Loglama ayarlarını yapılandırır (log dosyası, seviye, format vb.).
    
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S", 
    )
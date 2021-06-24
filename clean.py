import time
import data

if __name__ == "__main__":
    t_start = time.perf_counter()
    
    for fileCsv in data.get_files_list(data.DATA_DIR, 'csv'):
        remove(fileCsv)

    for fileCache in data.get_files_list(data.CACHE_DIR, 'h5'):
        remove(fileCache)

    t_stop = time.perf_counter()
    print("--------------------------------------------------")
    print("Elapsed time: %.1f [sec]" % ((t_stop-t_start)))
    print("--------------------------------------------------") 
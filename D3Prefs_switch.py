import os,re,sys

""" 逐行讀取文字檔並傳回陣列 """
def read_file_into_list(file_loc,write_mode="r",encode_set="utf-8",split_char="\n"):
    tmp_list=open(file_loc,write_mode,encoding=encode_set).read().split(split_char)
    return tmp_list

""" 將陣列元素逐行寫入文字檔 """
def write_file_from_list(file_loc,tmp_list=[],write_mode="w+",encode_set="utf-8"):
    if len(tmp_list)!=0:
        with open(file_loc,write_mode,encoding=encode_set) as f:
            for i in tmp_list:
                f.writelines(i+'\n')
        f.close()
        print("[ OK ] 陣列寫入文字檔 "+get_file_fullname(file_loc)+" 完成!  文件編碼:"+encode_set+"")
    else:
        print("[ XX ] 陣列寫入文字檔 "+get_file_fullname(file_loc)+" 失敗!")
        return False

""" 取得完整檔名(不含路徑) """
def get_file_fullname(input_str1):
    return input_str1.split("\\")[-1]

""" 取得副檔名 """
def get_file_type(input_str2):
    return input_str2.split(".")[-1]

def read_d3_txt(d3_txt_url):
    print(d3_txt_url)
    with open(d3_txt_url,"r") as f:
        content=f.readlines()
    return content

def process_d3_txt(tmp_dict,tmp_arr):
    tmp_list=[i for i in tmp_dict.keys()]
    for i in range(0,len(tmp_arr)):
        tmp_str=re.findall("(^[^ ]+) ",tmp_arr[i])[0] if tmp_arr[i]!="" else ""
        if tmp_str!="" and tmp_str in tmp_list:
            tmp_arr[i]=tmp_str+' "'+tmp_dict[tmp_str]+'"'
    return tmp_arr

if __name__=="__main__":
    ini_filename="D3Prefs.ini"
    if len(sys.argv)>1 and sys.argv[1]!="" and (sys.argv[1]).split(".")[1]=="ini":
        ini_filename=sys.argv[1]
        #讀取 D3Prefs.ini參數
    with open(ini_filename,"r",encoding="utf-8") as f:
        tmp_content=f.read()
    exec(tmp_content)
    D3TXT_DIR=os.path.expanduser("~\\Documents\\Diablo III\\")
    D3TXT_URL=D3TXT_DIR+"D3Prefs.txt"

    txt_arr=read_file_into_list(D3TXT_URL)
    write_file_from_list(D3TXT_URL.replace(".txt","_BACKUP.txt"),txt_arr)
    print(get_file_fullname(D3TXT_URL)+" 已備份為"+get_file_fullname(D3TXT_URL.replace(".txt","_BACKUP.txt"))+"\n-----------------------------------------------")
    print("D3Prefs.txt 設定快速切換器")
    while 1:
        choose=((lambda x:int(x) if re.search("^[0-9]+$",x)!=None else "Not Number!")(input("請輸入選項:(1-5) \n1)設為1024x768視窗模式\n2)設為1920x1080視窗模式\n3)降低硬件級數為2\n4)提高硬件級數為5\n5)離開程式\n "))) 
        if choose==5:
            exit(0)
        elif choose==1:
            txt_arr=process_d3_txt(DICT_1024X768,txt_arr)
            write_file_from_list(D3TXT_URL,txt_arr)
        elif choose==2:
            txt_arr=process_d3_txt(DICT_1920X1080,txt_arr)
            write_file_from_list(D3TXT_URL,txt_arr)
        elif choose==3:
            for i in range(0,len(txt_arr)):
                if txt_arr[i].find('HardwareClass')!=-1:
                    txt_arr[i]='HardwareClass "'+HWCLASS_LOW+'"'
            write_file_from_list(D3TXT_URL,txt_arr)
        elif choose==4:
            for i in range(0,len(txt_arr)):
                if txt_arr[i].find('HardwareClass')!=-1:
                    txt_arr[i]='HardwareClass "'+HWCLASS_HIGH+'"'
            write_file_from_list(D3TXT_URL,txt_arr)
        else:
            print("INPUT ERROR!!! PLEASE RETRY")
        print(choose)

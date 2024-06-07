import time
import os,sys

# 导入第三方库-docx2pdf
from docx2pdf import convert


# 导入subprocess
from subprocess import Popen, PIPE

# 将当前文件夹的上一级目录添加到系统路径中
sys.path.append(os.path.split(sys.path[0])[0])


# 从txt中逐行读取文本生成MergeList
def ReadTxtToMergeList(txtPath) -> list:
    MergeList = []
    with open(txtPath,'r',encoding='utf-8') as f:
        for line in f.readlines():
            MergeList.append(line.strip())
    return MergeList


# 递归获取文件夹中的所有文件，返回一个文件列表FileList
def AllFilesList(dir,FileList) -> list:
    if os.path.isfile(dir):
        FileList.append(dir)
    elif os.path.isdir(dir):  
        newDir = dir
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            AllFilesList(newDir,FileList)
    return FileList
    

# 对于文件夹及子文件夹中的所有docx文件，将其转换为pdf文件
def ConvertAndMergePdfPackage(FolderPath,MergeList,MergeOutputName) -> None:
    # 导入第三方库-pypdf
    importpypdfbegin = time.time()
    from pypdf import PdfWriter
    importpypdfend = time.time()
    print('导入pypdf库耗时：%s秒' % str(round(importpypdfend - importpypdfbegin,2)))
    # 获取当前文件夹中的所有文件,并储存在files这一个列表中
    files = AllFilesList(FolderPath,[])
    # 文件计数器初始化
    MergeFileCount = 0

    for MergeFileName in MergeList:            # 遍历files列表中的所有文件字符串
        for file in files:
            filename = file.split('.')[0]
            # 如果要合并的文件名与当前文件的文件名不相同，则跳到下一个文件
            if MergeFileName not in filename:
                continue
            # 获取合并文件名之前的时间
            beforeconverttime = time.time()
    
            # 如果确定是符合要求的文件，则将这些docx文件转换为pdf文件

            # 定义输出文件的名称及路径
            OutputFileName = str(MergeFileCount)+ '.pdf'
            OutputPath = FolderPath + "\\" + OutputFileName
            # 目前使用的是docx2pdf库，但是感觉效率非常的低，后期需要修改
            convert(input_path=file,
                    output_path=OutputPath)
            # 获取合并文件名之后的时间
            afterconvertime = time.time()
            print('第%d个文件转换完成，文件名：%s，耗时：%s秒' % 
                  (MergeFileCount+1,file.spilt(".")[-1],
                   str(round(afterconvertime - beforeconverttime ,2)))
                )
            # 合并完成后，文件计数器加1
            MergeFileCount += 1
        
    # 合并部分将所有pdf文件合并为一个pdf文件
    MergeBegin = time.time()
    merger = PdfWriter()   
    for i in range(MergeFileCount):
        merger.append(FolderPath + "\\" + str(i)+ '.pdf')

    # 写合并文件
    merger.write(FolderPath + "\\" + MergeOutputName + '.pdf')
    # 关闭合并的文件
    merger.close()
    MergeEnd = time.time()
    print('合并文件耗时：%s秒' % str(round(MergeEnd - MergeBegin,2))
        )
    # 随后删除所有此前作为中间变量pdf文件
    for i in range(MergeFileCount):
        os.remove(FolderPath + "\\" + str(i)+ '.pdf')


        


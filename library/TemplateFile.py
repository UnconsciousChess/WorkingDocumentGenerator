import os,sys

# 导入nanoid模块
from nanoid import generate

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

# 不要生成字节码
sys.dont_write_bytecode = True

# 该类为模板文件类，每一个对象都对应一个模板文件
class TemplateFile():

    def __init__(self):
        # 模板文件的id
        self._TemplateFileId = ""
        # 模板文件的名称
        self._TemplateFileName = ""
        # 模板文件的路径
        self._TemplateFileDir = ""
        # 模板文件的类型（直接复制或者docxtpl）
        self._TemplateFileType = ""
        # 模板文件的阶段（委托、立案、审理、执行、归档）
        self._TemplateFileStage = ""

    # ======= Get方法 ======= #
    def GetTemplateFileId(self):
        return self._TemplateFileId
    
    def GetTemplateFileName(self):
        return self._TemplateFileName

    def GetTemplateFileDir(self):
        return self._TemplateFileDir
    
    def GetTemplateFileType(self):
        return self._TemplateFileType
    
    def GetTemplateFileStage(self):
        return self._TemplateFileStage
    
    # ======= Set方法 ======= #
    def SetTemplateFileId(self,TemplateFileId,Debug=False) -> int:
            
        # 输入检查
        # 检查id是否为字符串
        if not isinstance(TemplateFileId,str):
            if Debug:
                print("TemplateFileId should be a string.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileId = TemplateFileId
        return 0
    
    def SetTemplateFileName(self,TemplateFileName,Debug=False) -> int:

        # 输入检查
        # 检查文件名是否为字符串
        if not isinstance(TemplateFileName,str):
            if Debug:
                print("TemplateFileName should be a string.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileName = TemplateFileName
        return 0
    
    def SetTemplateFileDir(self,TemplateFileDir,Debug=False) -> int:

        # 输入检查
        # 检查路径是否为字符串
        if not isinstance(TemplateFileDir,str):
            if Debug:
                print("TemplateFileDir should be a string.") 
            return -1
        # 检查路径是否存在
        if not os.path.exists(TemplateFileDir):
            if Debug:
                print("TemplateFileDir does not exist.")
            return -1
        # 检查路径是否为文件
        if not os.path.isfile(TemplateFileDir):
            if Debug:
                print("TemplateFileDir should be a file.")
            return -1
        # 检查文件是否为docx文件
        if TemplateFileDir.split(".")[-1] != "docx":
            if Debug:
                print("TemplateFileDir should be a docx file.")
            return -1

        # 经过检查后，赋值
        self._TemplateFileDir = TemplateFileDir
        return 0
    
    def SetTemplateFileType(self,TemplateFileType,Debug=False) -> int:

        # 输入检查
        # 检查文件类型是否为字符串
        if not isinstance(TemplateFileType,str):
            if Debug:
                print("TemplateFileType should be a string.")
            return -1
        
        # 检查文件类型是否为directCopy或docxtpl
        if TemplateFileType != "directCopy" and TemplateFileType != "docxtpl":
            if Debug:
                print("TemplateFileType should be 'directCopy' or 'docxtpl'.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileType = TemplateFileType

        return 0

    def SetTemplateFileStage(self,TemplateFileStage,Debug=False) -> int:

        # 输入检查
        # 检查阶段是否为字符串
        if not isinstance(TemplateFileStage,str):
            if Debug:
                print("TemplateFileStage should be a string.")
            return -1
        
        # 检查阶段是否为委托、立案、审理、执行、归档 这五个阶段之一
        if TemplateFileStage != "委托" and TemplateFileStage != "立案" and TemplateFileStage != "审理" and TemplateFileStage != "执行" and TemplateFileStage != "归档":
            if Debug:
                print("TemplateFileStage should be '委托' or '立案' or '审理' or '执行' or '归档'.")
            return -1
        
        # 经过检查后，赋值
        self._TemplateFileStage = TemplateFileStage

        return 0 
            

    # ======= 更抽象一些的Set方法 ======= #

    # 下面是对于读入文件中的每一行进行处理
    def SetTemplateFileFromString(self,InputString,Debug=False) -> str:
        
        # 每一个合法的字符串格式应当为：TemplateFileStage|TemplateFileDir@TemplateFileType


        # 去除首尾空格
        InputString = InputString.strip()

        # 检查字符串是否符合规则
        if "|" not in InputString:
            if Debug:
                print("SetTemplateFromString函数报错:读入的字符串%s缺少字符【|】，不符合规则" % InputString)
                return "Error"
        if "@" not in InputString:
            if Debug:
                print("SetTemplateFromString函数报错:读入的字符串%s缺少字符【@】，不符合规则" % InputString)
                return "Error"
        
        # 将字符串按照|分割
        try:
            FileStage,FiledirAndFileType = InputString.split("|")
        except:
            if Debug:
                print("SetTemplateFromString函数报错:读入的字符串%s无法按照【|】分割" % InputString)
            return "Error"
        # 将剩下的字符串按照@分割
        try:
            Filedir,FileType = FiledirAndFileType.split("@")
        except:
            if Debug:
                print("SetTemplateFromString函数报错:读入的字符串%s无法按照【@】分割" % InputString)
            return "Error"
        
        # 调用Set方法分别赋值
        if self.SetTemplateFileStage(FileStage) == -1:
            return "Error"
        if self.SetTemplateFileDir(Filedir) == -1:
            return "Error"
        if self.SetTemplateFileType(FileType) == -1:
            return "Error"
        # 将文件名从路径中提取出来
        FileName = Filedir.split("\\")[-1]
        # 去掉后缀名
        FileName = FileName.split(".")[0]
        if self.SetTemplateFileName(FileName) == -1:     
            return "Error"
        # 生成id
        if self.SetTemplateFileId(generate(alphabet='ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnpqrstuvwxyz', size=8)) == -1:
            return "Error"

        # 全部正常运行，返回Success
        return "Success"

    # 下面对于读入字典进行处理
    def SetTemplateFileFromDict(self,InputDict,Debug=False) -> str:
        # 检查是否为字典
        if not isinstance(InputDict,dict):
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入不是字典")
            return "Error"
        
        # 检查是否有templateFileName键
        if "templateFileName" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileName】")
            return "Error"
        # 检查是否有templateFileDir键
        if "templateFileDir" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileDir】")
            return "Error"
        # 检查是否有templateFileType键
        if "templateFileType" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileType】")
            return "Error"
        # 检查是否有templateFileStage键
        if "templateFileStage" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileStage】")
            return "Error"
        # 检查是否有templateFileId键
        if "templateFileId" not in InputDict:
            if Debug:
                print("SetTemplateFileFromDict函数报错:输入字典缺少键【templateFileId】")
            return "Error"
        
        # 调用Set方法分别赋值
        if self.SetTemplateFileName(InputDict["templateFileName"]) == -1:
            return "Error"
        if self.SetTemplateFileDir(InputDict["templateFileDir"]) == -1:
            return "Error"
        if self.SetTemplateFileType(InputDict["templateFileType"]) == -1:
            return "Error"
        if self.SetTemplateFileStage(InputDict["templateFileStage"]) == -1:
            return "Error"
        if self.SetTemplateFileId(InputDict["templateFileId"]) == -1:
            return "Error"
        
        # 全部正常运行，返回Success
        return "Success"

    # ======= Output方法 ======= #

    # 输出为该模板文件的字符串，方便写入txt文件(只输出3个属性)
    def OutputTemplateFileToString(self) -> str:
        return self.GetTemplateFileStage() + "|" + self.GetTemplateFileDir() + "@" + self.GetTemplateFileType()

    # 输出为字典，方便写入json文件或输出到前端
    def OutputTemplateFileToDict(self) -> dict:
        return {"templateFileName":self.GetTemplateFileName(),
                "templateFileDir":self.GetTemplateFileDir(),
                "templateFileType":self.GetTemplateFileType(),
                "templateFileStage":self.GetTemplateFileStage(),
                "templateFileId":self.GetTemplateFileId()
                }
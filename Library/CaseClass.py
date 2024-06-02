import os,sys
sys.path.append(os.path.split(sys.path[0])[0])

from Library.LitigantClass import *

class Case():

    def __init__(self) -> None:
        # 初始化案件类的各项属性，均设为初始值
        # 案件类型
        self._CaseType = 0
        # 诉讼标的额
        self._LitigationAmount = 0
        # 案由
        self._CaseOfAction = ""
        # 管辖法院
        self._Jurisdiction = ""        
        # 上传文件列表
        self._UploadFilesList = []
        # 诉讼请求
        self._ClaimText = ""
        # 事实与理由
        self._FactAndReasonText = ""
        # 案件文件所在文件夹路径
        self._CaseFolderPath = ""
        # 原告主体列表,如原告[0]（原告一）、原告[1]（原告二）...
        self._PlaintiffList = []
        # 被告主体列表,如被告[0]（被告一）、被告[1]（被告二）...
        self._DefendantList = []
        # 第三人主体列表,如第三人[0]（第三人一）、第三人[1]（第三人二）...
        self._LegalThirdPartyList = []
        # 调解意向
        self._Mediation = False
        # 拒绝调解理由
        self._RejectMediationReasonText = ""
        # 案件代理的阶段
        self._CaseAgentStage = []
        # 风险代理情况
        self._RiskAgentStatus = None
        # 风险代理前期费用
        self._RiskAgentUpfrontFee = 0
        # 风险代理后期比例
        self._RiskAgentPostFeeRate = 0
        # 非风险代理的固定费用(是一个数组，第一个元素对应第一个阶段的费用，第二个元素对应第二个阶段的费用...)
        self._AgentFixedFee = []


    # 定义外部访问时，返回各属性的函数
    # 案件类型
    def GetCaseType(self):
        return self._CaseType
    # 诉讼标的额
    def GetLitigationAmount(self):
        return self._LitigationAmount
    # 案由
    def GetCauseOfAction(self):
        return self._CaseOfAction
    # 管辖法院
    def GetJurisdiction(self):
        return self._Jurisdiction
    # 上传文件列表
    def GetUploadFilesList(self):
        return self._UploadFilesList
    # 诉讼请求
    def GetClaimText(self):
        return self._ClaimText
    # 事实与理由
    def GetFactAndReasonText(self):
        return self._FactAndReasonText
    # 案件文件所在文件夹路径
    def GetCaseFolderPath(self):
        return self._CaseFolderPath
    # 原告主体列表
    def GetPlaintiffList(self):
        return self._PlaintiffList
    # 获取原告数量
    def GetPlaintiffCount(self):
        return len(self._PlaintiffList)
    # 被告主体列表
    def GetDefendantList(self):
        return self._DefendantList
    # 获取被告数量
    def GetDefendantCount(self):
        return len(self._DefendantList)
    # 第三人主体列表
    def GetLegalThirdPartyList(self):
        return self._LegalThirdPartyList
    # 获取第三人数量
    def GetLegalThirdPartyCount(self):
        return len(self._LegalThirdPartyList)
    # 调解意愿
    def GetMediation(self):
        return self._Mediation
    # 拒绝调解理由
    def GetRejectMediationReasonText(self):
        return self._RejectMediationReasonText
    # 案件代理的阶段
    def GetCaseAgentStage(self):
        return self._CaseAgentStage
    # 风险代理情况
    def GetRiskAgentStatus(self):
        return self._RiskAgentStatus
    # 风险代理前期费用
    def GetRiskAgentUpfrontFee(self):
        return self._RiskAgentUpfrontFee
    # 风险代理后期比例
    def GetRiskAgentPostFeeRate(self):
        return self._RiskAgentPostFeeRate
    # 非风险代理的固定费用数组
    def GetAgentFixedFee(self):
        return self._AgentFixedFee
    

    # 非直接返回值，进行一些字符串处理的函数
    # 返回所有原告的名称的函数
    def GetAllPlaintiffNames(self) -> str:
        Plaintiffs = ""
        for litigant in self._PlaintiffList:
            Plaintiffs += litigant.GetName() + "、"
        Plaintiffs = Plaintiffs[:-1]
        return Plaintiffs
    # 返回所有被告的名称的函数
    def GetAllDefendantNames(self) -> str:
        Defendants = ""
        for litigant in self._DefendantList:
            Defendants += litigant.GetName() + "、"
        Defendants = Defendants[:-1]
        return Defendants

    # 定义外部访问的时候的设置属性
    # 案件类型设定方法，1为民事案件，2为行政案件，3为执行案件
    def SetCaseType(self,CaseType):
        if isinstance(CaseType,int):
            if CaseType == 1 or CaseType == 2 or CaseType == 3:
                self._CaseType = CaseType
            else:
                print("参数只能为1 2 3 ")
        else:
            print("参数必须为整型") 
    # 诉讼标的额设定方法
    def SetLitigationAmount(self,LitigationAmount):
        # 尝试将输入值转换为整数
        try:
            LitigationAmount = int(LitigationAmount)
        except:
            print("输入值并非整数")
            # 尝试将输入值转换为浮点数
            try:
                LitigationAmount = float(LitigationAmount)
            except:
                print("输入值并非浮点数")
                return
        # 诉讼标的额不能小于零
        if LitigationAmount >= 0:
            self._LitigationAmount = LitigationAmount
        else:
            print("诉讼标的不能小于零")
            return

    # 案由设定方法
    def SetCauseOfAction(self,CaseOfAction):
        with open("Data\PublicInfomationList\CauseOfActionList.txt","r",encoding="utf-8") as f:
            CaseOfActionList = f.readlines()
        # 去除每个案由的换行符
        CaseOfActionList = [i.strip() for i in CaseOfActionList]
        if (CaseOfAction in CaseOfActionList):
            self._CaseOfAction = CaseOfAction
            print("输入的案由【%s】添加成功" % CaseOfAction)
        else:
            print("你输入的【%s】名称不符合现有民事、行政、执行案由规定,请重新输入" % CaseOfAction)
    # 管辖法院设定方法(考虑使用检测，但这个不是必须的，因为有可能没有必要)
    def SetJurisdiction(self,Jurisdiction):
        # 准备所有合法法院名称的列表，方便进行对比，以防止输入的法院名称有误
        with open("Data\PublicInfomationList\CourtNameList.txt","r",encoding="utf-8") as f:
            JurisdictionList = f.readlines()
        # 去除每个法院名称的换行符
        JurisdictionList = [i.strip() for i in JurisdictionList]
        if (Jurisdiction in JurisdictionList):
            self._Jurisdiction = Jurisdiction
            print("添加管辖法院【%s】成功" % Jurisdiction)
        else:
            print("你输入的【%s】名称不符合现有法院名称,请重新输入" % Jurisdiction)
    # 上传文件列表设定方法
    def SetUploadFilesList(self,UploadFilesList):
        if isinstance(UploadFilesList,list):      
            self._UploadFilesList = UploadFilesList
        else:
            print("该输入对象的类型与属性不匹配,文件上传列表输入值为列表")
    # 诉讼请求设定方法
    def SetClaimText(self,ClaimText):
        if isinstance(ClaimText,str):
            self._ClaimText = ClaimText
        else:
            print("该输入对象的类型与属性不匹配,诉讼请求输入值为字符串")
    # 事实与理由设定方法
    def SetFactAndReasonText(self,FactAndReasonText):
        if isinstance(FactAndReasonText,str):
            self._FactAndReasonText = FactAndReasonText
        else:
            print("该输入对象的类型与属性不匹配,事实与理由输入值为字符串")
    # 案件文件所在文件夹路径设定方法
    def SetCaseFolderPath(self,CaseFolderPath):
        if isinstance(CaseFolderPath,str):
            print("输入的是字符串无误，进入下一步检测")
            if os.path.exists(CaseFolderPath):
                print("文件夹存在，进入下一步检测")
                if os.path.isdir(CaseFolderPath):
                    print("文件夹路径无误，进入下一步检测")
                    if os.listdir(CaseFolderPath) != []:
                        self._CaseFolderPath = CaseFolderPath
                        print("案件文件所在文件夹路径设定成功")
                    else:
                        print("文件夹为空，请重新输入")
                else:
                    print("文件夹路径错误，请重新输入")
            else:
                print("文件夹不存在，请重新输入")

        else:
            print("该输入对象的类型与属性不匹配,案件文件所在文件夹路径输入值为字符串")
    
    # 备注设定方法
    def SetCommentText(self,Comment):
        if isinstance(Comment,str):
            self._Comment = Comment
        else:
            print("该输入对象的类型与属性不匹配,备注输入值为字符串")
    # 调解意愿设定方法
    def SetMediationIntention(self,MediationIntention):
        if isinstance(MediationIntention,bool):
            self._MediationIntention = MediationIntention
        else:
            print("该输入对象的类型与属性不匹配,调解意向输入值为布尔值")
    # 拒绝理由设定方法
    def SetRejectMediationReasonText(self,RejectReason):
        if isinstance(RejectReason,str):
            self._RejectReason = RejectReason
        else:
            print("该输入对象的类型与属性不匹配,拒绝理由输入值为字符串")
    # 案件代理阶段设定方法
    def SetCaseAgentStage(self,CaseAgentStage):
        if isinstance(CaseAgentStage,list):
            # 对比新列表的数字是否与现有的列表重复
            for i in CaseAgentStage:
                if i not in self._CaseAgentStage and i in [1,2,3,4,5]:
                    self._CaseAgentStage.append(i)
        elif isinstance(CaseAgentStage,int):
            if CaseAgentStage not in self._CaseAgentStage and CaseAgentStage in [1,2,3,4,5]:
                self._CaseAgentStage.append(CaseAgentStage)
        else:
            print("SetCaseAgentStage报错：该输入对象的类型与属性不匹配,案件代理阶段输入值为列表或1-5的整数")

    # 定义一个检查函数，确保Case对象里面的所有属性都是符合输入到网页的规范的，避免在填表单的时候报错
    # 无误返回True，否则返回False
    # 后续如果每个函数的set方法里面都自带写好了检测的话，该方法可以废弃
    def CaseAttributeIsCorrect(self) -> bool:
        # 避免所有属性存在空值
        for v in self.__dict__.values():
            if v is None:
                print("有属性存在空值")
                return False
        # 避免案件类型错误,案件类型只能为1 2 3  
        if (self.CaseType != 1  and 
            self.CaseType != 2  and
            self.CaseType != 3):
            print("案件类型错误")
            return False
        # 避免诉讼标的额为负数
        if self.LitigationAmount < 0 :
            print("诉讼标的额只能为正数或等于零")
            return False
        # 要写一个案由筛选，从一个txt里面进行读取，对案由进行比较
        with open(file="CaseOfAction.txt",mode='r',encoding="utf-8") as f:
            # CaseOfActionArray是所有合法案由的列表
            CaseOfActionArray = f.read().split("\n")
        for CaseOfAction in CaseOfActionArray:
            # 如果找到与案由列表相等的案由，就终止循环
            if self.CaseOfAction == CaseOfAction:
                break   
        #  如果找遍了整个案由列表都没有找到的话，就视为该案由是有问题的，返回False
        else:
            print("案由内容错误")
            return False
        # 检测上传文件列表里面的文件有效性，判断是否为一个存在的文件
        for FilePath in self.UploadFilesList:
            if os.path.isfile(FilePath) == False:
                print("%s路径无法读取或路径存在错误" % (FilePath))
                return False
        # 检测诉讼请求不得为空
        if self.ClaimText == "":
            print("诉讼请求为空")
            return False
        # 检测事实和理由不得为空
        if self.FactAndReasonText == "":
            print("事实和理由为空")
            return False
        # 当选择拒绝调解的时候，自动给拒绝理由赋值，避免出错
        if self.Mediation == False:
            if self.RejectMediationReasonText == "":
                self.RejectMediationReasonText = "对方拒绝调解"

        # 经过所有检验都没问题后最终返回 True
        return True

    # 下面的方法是用于增加诉讼参与人的，和直接通过列表的方式列表添加的方法并存
    # 后面可能主要使用该方法来添加
    def AppendLitigant(self,ALitigant) -> bool:
        # 先判断添加进来的东西是什么
        if isinstance(ALitigant,Litigant):
            # 判断诉讼地位是原告、被告还是第三人
            # 原告1  被告2  第三人3
            if ALitigant.GetLitigantPosition() == 1:
                print("该诉讼参与人为原告")
                ALitigant.PrintInfo()
                self._PlaintiffList.append(ALitigant)
                print("添加原告成功")
                return True
            elif ALitigant.GetLitigantPosition()  == 2:
                print("该诉讼参与人为被告")
                ALitigant.PrintInfo()
                self._DefendantList.append(ALitigant)
                print("添加被告成功")
                return True
            elif ALitigant.GetLitigantPosition() == 3:
                print("该诉讼参与人为第三人")
                ALitigant.PrintInfo()
                self._LegalThirdPartyList.append(ALitigant)
                print("添加第三人成功")
                return True
            else:
                print("当前添加的诉讼参与人缺失诉讼地位参数LitigantPosition，无法添加到列表之中")
                return False

    # 定义一些测试函数方便打印信息的
    # 打印案件代理阶段
    def PrintCaseAgentStage(self):
        CaseAgentStageOutputString = "本案涉及的案件代理阶段有："
        if self._CaseAgentStage == []:
            return "无案件代理阶段信息"
        for i in self._CaseAgentStage:
            if i == 1:
                CaseAgentStageOutputString += "一审立案阶段、"
            elif i == 2:
                CaseAgentStageOutputString += "一审开庭阶段、"
            elif i == 3:
                CaseAgentStageOutputString += "二审阶段、"
            elif i == 4:
                CaseAgentStageOutputString += "执行阶段、"
            elif i == 5:
                CaseAgentStageOutputString += "再审阶段、"
        # 去掉最后一个顿号
        CaseAgentStageOutputString = CaseAgentStageOutputString[:-1]
        return CaseAgentStageOutputString
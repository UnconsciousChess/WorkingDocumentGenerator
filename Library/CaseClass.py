import os,sys

# 将当前工作目录添加到系统路径中
sys.path.append(os.getcwd())

from library.LitigantClass import *

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
        self._JurisdictionDict = {
            "一审": "",
            "二审": "",
            "再审": "",
            "执行": "",
            "仲裁": "",
        }        
        # 上传文件列表
        self._UploadFilesList = {}
        # 诉讼请求（上诉请求）
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
        self._MediationIntention = False
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
        # 非风险代理的固定费用(是一个列表，第一个元素对应第一个阶段的费用，第二个元素对应第二个阶段的费用...)
        self._AgentFixedFeeList = []
        # 案号
        self._CaseCourtCode = ""

    # 下面是案件类的外部方法,包括:
    # a.获取各属性的方法（Get-xxxx)
    # b.设定各属性的方法(Set-xxxx、Append-xxx)
    # c.输入案件信息的方法(Input-xxx)
    # d.输出案件信息的方法(Output-xxx)

    # ==================Get方法：下面定义外部直接获取各属性的方法====================

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
    def GetJurisdictionDict(self):
        return self._JurisdictionDict
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
    # 被告主体列表
    def GetDefendantList(self):
        return self._DefendantList
    # 第三人主体列表
    def GetLegalThirdPartyList(self):
        return self._LegalThirdPartyList
    # 调解意愿
    def GetMediationIntention(self):
        return self._MediationIntention
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
    # 法院案号
    def GetCaseCourtCode(self):
        return self._CaseCourtCode
    

    # ===== Get方法：下面定义外部获取各属性的一些进阶方法（主要涉及输出一些常用字符串）=====

    # 返回所有原告的名称字符串的函数
    def GetAllPlaintiffNames(self) -> str:
        Plaintiffs = ""
        for litigant in self._PlaintiffList:
            Plaintiffs += litigant.GetName() + "、"
        Plaintiffs = Plaintiffs[:-1]
        return Plaintiffs
    
    # 返回所有被告的名称字符串的函数
    def GetAllDefendantNames(self) -> str:
        Defendants = ""
        for litigant in self._DefendantList:
            Defendants += litigant.GetName() + "、"
        Defendants = Defendants[:-1]
        return Defendants
    
    # 返回代理阶段代码对应的中文字符串
    def GetCaseAgentStageStr(self) -> str:
        CaseAgentStageOutputString = ""
        if self._CaseAgentStage == []:
            return CaseAgentStageOutputString
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
    
    # 返回我方当事人列表及代理方向
    def GetOurClientListAndSide(self) -> list:
        OurClientList = []
        OurClientSide = ""
        for plaintiff in self.GetPlaintiffList():
            if plaintiff.IsOurClient():
                OurClientList.append(plaintiff)
                OurClientSide = "p"
        # 如果我方不是代理原告，则为代理被告
        if OurClientSide != "p" :
            for defendant in self.GetDefendantList():
                if defendant.IsOurClient():
                    OurClientList.append(defendant)
                    OurClientSide = "d"

        return OurClientList,OurClientSide

    def GetOurClientNames(self) -> str:
        OurClientList,OurClientSide = self.GetOurClientListAndSide()
        OurClientNames = ""
        for litigant in OurClientList:
            OurClientNames += litigant.GetName() + "、"
        OurClientNames = OurClientNames[:-1]
        return OurClientNames

    # ============Set和Append方法：下面定义设定各属性的方法（含输入值校验）=============

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
        with open(r"Data\PublicInfomationList\CauseOfActionList.txt","r",encoding="utf-8") as f:
            CaseOfActionList = f.readlines()
        # 去除每个案由的换行符
        CaseOfActionList = [i.strip() for i in CaseOfActionList]
        if (CaseOfAction in CaseOfActionList):
            self._CaseOfAction = CaseOfAction
            print("输入的案由【%s】添加成功" % CaseOfAction)
        else:
            print("输入的【%s】名称不符合现有民事、行政、执行案由规定,请重新输入" % CaseOfAction)
    
    # 管辖法院设定方法
    def SetJurisdictionDict(self,InputJurisdictionDict,debugmode=False):
        # 准备所有合法法院名称的列表，方便进行对比，以防止输入的法院名称有误
        with open(r"Data\PublicInfomationList\CourtNameList.txt","r",encoding="utf-8") as f:
            StandardJurisdictionList = f.readlines()
        # 去除每个法院名称的换行符
        StandardJurisdictionList = [i.strip() for i in StandardJurisdictionList]

        for stage,jurisdictionname in InputJurisdictionDict.items():
             #如果输入的键名（阶段）在现有的字典的键名（阶段）中,则进一步判断输入的键值是否合法  
            if stage in self._JurisdictionDict.keys():      
                    # 判断输入的键名（法院名称）是否在Standard法院列表中，即是否合法  
                    if (jurisdictionname in StandardJurisdictionList):
                        self._JurisdictionDict[stage] = jurisdictionname
                        if debugmode:
                            print("添加【%s】管辖法院【%s】成功" % (stage,jurisdictionname))
                    else:
                        if debugmode:
                            print("输入的【%s】名称不符合现有法院名称。" % jurisdictionname)
            else:
                if debugmode:
                    print("输入的【%s】键名不符合规范" % stage)

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

    # 调解意愿设定方法
    def SetMediationIntention(self,MediationIntention):
        if isinstance(MediationIntention,bool):
            self._MediationIntention = MediationIntention

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

    # 风险代理情况设定方法
    def SetRiskAgentStatus(self,RiskAgentStatus,DebugMode=False):
        if isinstance(RiskAgentStatus,bool):
            self._RiskAgentStatus = RiskAgentStatus
        else:
            if DebugMode:
                print("该输入对象的类型与属性不匹配,风险代理情况输入值为布尔值")
    
    # 风险代理前期费用设定方法
    def SetRiskAgentUpfrontFee(self,RiskAgentUpfrontFee,DebugMode=False):
        # 尝试将输入值转换为浮点数
        try:
            RiskAgentUpfrontFee = float(RiskAgentUpfrontFee)
        except:
            if DebugMode:
                print("输入值并非浮点数")
            return
        # 诉讼标的额不能小于零
        if RiskAgentUpfrontFee >= 0:
            self._RiskAgentUpfrontFee = RiskAgentUpfrontFee
        else:
            if DebugMode:
                print("风险代理前期费用不能小于零")
            return
    
    # 风险代理后期比例设定方法
    def SetRiskAgentPostFeeRate(self,RiskAgentPostFeeRate,DebugMode=False):
        # 尝试将输入值转换为浮点数
        try:
            RiskAgentPostFeeRate = float(RiskAgentPostFeeRate)
        except:
            if DebugMode:
                print("输入值并非浮点数")
            return
        # 诉讼标的额不能小于零
        if RiskAgentPostFeeRate >= 0:
            self._RiskAgentPostFeeRate = RiskAgentPostFeeRate
        else:
            if DebugMode:
                print("风险代理后期比例不能小于零")
            return

    # 非风险代理的固定费用设定方法（方法一直接输入列表）
    def SetAgentFixedFeeByList(self,AgentFixedFeeList,DebugMode=False):
        # 判断是否原本列表式否非空
        if self._AgentFixedFeeList == []:
            # 判断输入值是否为列表
            if isinstance(AgentFixedFeeList,list):
                # 再次判断列表的数量是否小于等于代理阶段的数量
                if len(AgentFixedFeeList) <= len(self.GetCaseAgentStage()):
                    self._AgentFixedFeeList = AgentFixedFeeList
                else:
                    if DebugMode:
                        print("SetAgentFixedFee报错：输入的固定费用列表数量超出已有的代理阶段数量")
            else:
                if DebugMode:
                    print("SetAgentFixedFee报错：该输入对象的类型与属性不匹配,非风险代理的固定费用输入值为列表或整数")
        else:
            if DebugMode:
                print("SetAgentFixedFee报错：非风险代理的固定费用列表已经存在，无法再次设定")
    
    # 非风险代理的固定费用设定方法（方法二直接输入代理费用和代理阶段）
    def SetAgentFixedFeeByAdd(self,AgentFixedFee,Stage,DebugMode=False):
        # 判断输入值是否为整数
        if isinstance(AgentFixedFee,float) and isinstance(Stage,int):
            if Stage <= len(self.GetCaseAgentStage()-1):
                self._AgentFixedFeeList[Stage] = AgentFixedFee
            else:
                if DebugMode:
                    print("SetAgentFixedFee报错：输入的阶段序号超出已有的阶段序号")
        else:
            if DebugMode:
                print("SetAgentFixedFee报错：输入对象的类型与属性不匹配,非风险代理的固定费用输入值为列表或整数")
        
    # 法院案号设定方法
    def SetCaseCourtCode(self,CaseCourtCode):
        if isinstance(CaseCourtCode,str):
            self._CaseCourtCode = CaseCourtCode
        else:
            print("SetCaseCourtCode方法报错：该输入对象的类型与属性不匹配,法院案号输入值为字符串")


     # 将诉讼参与人添加到案件中
    

    # 添加诉讼参与人的方法
    def AppendLitigant(self,ALitigant,PrintLogMode=False) -> bool:
        # 先判断添加进来的东西是什么
        if isinstance(ALitigant,Litigant):
            # 判断诉讼地位是原告、被告还是第三人
            # 原告1  被告2  第三人3
            if ALitigant.GetLitigantPosition() == 1:
                self._PlaintiffList.append(ALitigant)
                if PrintLogMode:
                    print("添加原告【%s】成功" % ALitigant.GetName())   
                return True
            elif ALitigant.GetLitigantPosition()  == 2:
                self._DefendantList.append(ALitigant)
                if PrintLogMode:
                    print("添加被告【%s】成功" % ALitigant.GetName())
                return True
            elif ALitigant.GetLitigantPosition() == 3:
                self._LegalThirdPartyList.append(ALitigant)
                if PrintLogMode:
                    print("添加第三人【%s】成功" % ALitigant.GetName()) 
                return True
            else:
                if PrintLogMode:
                    print("当前添加的诉讼参与人【%s】缺失诉讼地位参数LitigantPosition，无法添加到列表之中" % ALitigant.GetName())
                return False
   
    # ===========Input方法：下面定义批量输入案件信息的方法=============

    # 设定一个类的内部方法，对于参数键名和键值，分别进行处理
    def SetCaseInfoWithKeyAndValue(self,Key,Value):
        # 根据Key的不同，调用不同的设定方法
        if Key == '案件类型':
            self.SetCaseType(int(Value))

        elif Key == '诉讼标的额':
            self.SetLitigationAmount(float(Value))

        elif Key == '案由':
            self.SetCauseOfAction(str(Value))

        elif Key == '管辖法院':
            # 将Value转换为字典，以便SetJurisdictionDict方法处理

            # 以逗号分割字符串,分割出Stage:Court的字符串列表
            StageAndCourtList = Value.split(",")
            for stageandcourt in StageAndCourtList: 
                # 去掉阶段和法院名称的空格
                stageandcourt = stageandcourt.strip()
                # 去掉“阶段”两个字
                stageandcourt = stageandcourt.replace("阶段","")
                # 以冒号分割字符串,中文冒号或英文冒号
                if "：" in stageandcourt:
                    Stage,Court = stageandcourt.split("：")
                elif ":" in stageandcourt:
                    Stage,Court = stageandcourt.split(":")
                # 调用设定管辖法院的方法
                self.SetJurisdictionDict({Stage:Court})

        elif Key == '诉讼请求':
            self.SetClaimText(str(Value))

        elif Key == '事实与理由':
            self.SetFactAndReasonText(str(Value))

        elif Key == '案件文件所在文件夹路径':
            self.SetCaseFolderPath(Value)

        elif Key == '调解意愿':
            if Value == "True" or Value == "true" or Value == "TRUE" or Value == "1":
                Value = True
            elif Value == "False" or Value == "false" or Value == "FALSE" or Value == "0":
                Value = False
            self.SetMediationIntention(Value)
            
        elif Key == '拒绝调解理由':
            self.SetRejectMediationReasonText(str(Value))

        elif Key == '案件代理阶段':
            # 将Value转换为数字，以便SetCaseAgentStage方法处理
            # 以逗号分割字符串,分割出各阶段的字符串列表
            StageList = Value.split(",")
            for stagestr in StageList:
                if "一审" in stagestr:
                    self.SetCaseAgentStage([1,2])

                elif "二审" in stagestr:
                    self.SetCaseAgentStage(3)
                elif "执行" in stagestr:
                    self.SetCaseAgentStage(4)
                elif "再审" in stagestr:
                    self.SetCaseAgentStage(5)

        elif Key == '风险代理情况':
            if Value == "True" or Value == "true" or Value == "TRUE" or Value == "1":
                Value = True
            elif Value == "False" or Value == "false" or Value == "FALSE" or Value == "0":
                Value = False
            self.SetRiskAgentStatus(Value)

        elif Key == '风险代理前期费用':
            self.SetRiskAgentUpfrontFee(float(Value))

        elif Key == '风险代理后期比例':
            self.SetRiskAgentPostFeeRate(float(Value))

        elif Key == '非风险代理的固定费用':
            # 将Value转换为列表
            # 以逗号分割字符串,分割出各阶段的字符串列表
            FixedFeeList = Value.split(",")
            # 将字符串列表转换为浮点数列表
            FixedFeeList = [float(i) for i in FixedFeeList]
            self.SetAgentFixedFeeByList(FixedFeeList)
            

        elif Key == '法院案号':
            self.SetCaseCourtCode(Value)

    # 读取一个txt文档的路径来输入上述案件信息
    def InputCaseInfoFromTxt(self,CaseInfoFilePath,DebugMode=False):
        # 判断路径是否存在
        if not os.path.exists(CaseInfoFilePath):
            print("文件路径不存在")
            return
        
        # 路径存在，则读取文件
        with open(CaseInfoFilePath,"r",encoding="utf-8") as f:
            CaseInfoLines = f.readlines()
        # 去除每个案由的换行符
        CaseInfoLines = [i.strip() for i in CaseInfoLines]
        # 逐行读取文件
        for line in CaseInfoLines:
            # 判断是否为空行，是则跳过
            if line == "":
                continue
            # 判断是否为以#开头的注释行，是则跳过
            if line[0] == "#":
                continue
            # 判断是否有等于号，没有则跳过
            if "=" not in line:
                continue
            # 以等于号分割字符串
            Key,Value = line.split("=")
            # 对上述分割出来的键值对进行处理
            self.SetCaseInfoWithKeyAndValue(Key,Value)

    # 读取一个excel文档的路径来输入上述案件信息
    def InputCaseInfoFromExcel(self,CaseInfoFilePath,DebugMode=False):
        pass
    
    # 从应用前端中输入案件信息
    def InputCaseInfoFromFrontEnd(self,CaseInfoDict,DebugMode=False):
        if isinstance(CaseInfoDict,dict):
            # 对于字典中的逐个键值对读取
            for Key,Value in CaseInfoDict.items():
                self.SetCaseInfoWithKeyAndValue(Key,Value)


    # ===========Output方法：下面定义输出案件信息的方法=============

    # 输出案件信息到txt文件
    def OutputCaseInfoToTxt(self,OutputFilePath,DebugMode=False):
        with open(file=OutputFilePath,mode="w",encoding="utf-8") as f:
            # 逐个输出案件信息
            f.write("案件类型=%s\n" % self.GetCaseType())
            f.write("诉讼标的=%s元\n" % self.GetLitigationAmount())
            f.write("案由=%s\n" % self.GetCauseOfAction())
            f.write("管辖法院=")
            for stage,court in self.GetJurisdictionDict().items():
                f.write("%s:%s," % (stage,court))
            f.write("\n")
            f.write("诉讼请求=%s\n" % self.GetClaimText())
            f.write("事实与理由=%s\n" % self.GetFactAndReasonText())
            f.write("案件文件所在文件夹路径=%s\n" % self.GetCaseFolderPath())
            f.write("原告主体列表=")
            for plaintiff in self.GetPlaintiffList():
                f.write("%s," % plaintiff.GetName())
            f.write("\n")
            f.write("被告主体列表=")
            for defendant in self.GetDefendantList():
                f.write("%s," % defendant.GetName())
            f.write("\n")
            f.write("第三人主体列表=")
            for thirdparty in self.GetLegalThirdPartyList():
                f.write("%s," % thirdparty.GetName())
            f.write("\n")
            f.write("调解意愿=%s\n" % self.GetMediationIntention())
            f.write("拒绝调解理由=%s\n" % self.GetRejectMediationReasonText())
            f.write("案件代理的阶段:%s\n" % self.GetCaseAgentStageStr())
            if self.GetRiskAgentStatus() == True:
                f.write("本案为风险代理。\n")
                f.write("风险代理前期费用=%s\n" % self.GetRiskAgentUpfrontFee())
                f.write("风险代理后期比例=%s\n" % self.GetRiskAgentPostFeeRate())
            else:
                f.write("非风险代理的固定费用=")
                for fee in self.GetAgentFixedFee():
                    f.write("%s," % fee)
            f.write("法院案号是：%s\n" % self.GetCaseCourtCode())
    
    # 输出案件信息到excel文件
    def OutputCaseInfoToExcel(self,OutputFilePath,DebugMode=False):
        pass

    # 输出案件信息到前端(输出为json格式)
    def OutputCaseInfoToFrontEnd(self,DebugMode=False):
        pass
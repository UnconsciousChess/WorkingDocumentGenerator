## Case

### 概述

    案件，每一个实例对应的是现实中每一个单独的案子

#### 对应源文件

    CaseClass.py

#### 导入代码

```python
from library.CaseClass import Case
```

#### 属性

| 属性名                     | 含义                   | 数据类型 |
| -------------------------- | ---------------------- | -------- |
| _CaseType                  | 案件类型               | int      |
| _LitigationAmount          | 诉讼标的额             | float    |
| _CaseOfAction              | 案由                   | str      |
| _JurisdictionDict          | 管辖法院（各诉讼阶段） | dict     |
| _UploadFilesList           | 上传文件列表           | list     |
| _ClaimText                 | 诉讼请求               | str      |
| _FactAndReasonText         | 事实和理由             | str      |
| _CaseFolderPath            | 案件文件夹绝对路径     | str      |
| _PlaintiffList             | 原告列表               | list     |
| _DefendantList             | 被告列表               | list     |
| _LegalThirdPartyList       | 第三人列表             | list     |
| _MediationIntention        | 调解意愿               | bool     |
| _RejectMediationReasonText | 拒绝调解的理由         | str      |
| _CaseAgentStage            | 律师代理阶段           | list     |
| _RiskAgentStatus           | 是否采取风险收费的方式 | bool     |
| _RiskAgentUpfrontFee       | 风险收费前期费用       | float    |
| _RiskAgentPostFeeRate      | 风险收费后期提成比例   | float    |
| _AgentFixedFeeList         | 各阶段固定收费列表     | list     |
| _CaseCourtCode             | 案号                   | str      |
| _CaseId                    | 案件生成的id           | str      |

#### 方法

##### Getter方法

###### 简单的Getter方法

| 方法名           | 参数 | 返回值数据类型       | 作用             |
| ---------------- | ---- | -------------------- | ---------------- |
| **Get** + 属性名 | N/A  | 对应属性 的 数据类型 | 外部访问实例属性 |

###### 进阶的Getter方法

| 方法名                  | 参数 | 返回值数据类型 | 作用                                               |
| ----------------------- | ---- | -------------- | -------------------------------------------------- |
| GetAllPlaintiffNames    | N/A  | str            | 以中文顿号间隔，返回所有原告的名称                 |
| GetAllDefendantNames    | N/A  | str            | 以中文顿号间隔，返回所有被告的名称                 |
| GetCaseAgentStageStr    | N/A  | str            | 以中文顿号间隔，返回所有代理阶段的名称             |
| GetOurClientListAndSide | N/A  | list，str      | 返回我方当事人的列表，以及代理的方向               |
| GetOurClientNames       | N/A  | str            | 以中文顿号间隔，返回所有我方当事人的名称           |
| GetCourtNameStr         | N/A  | str            | 以中文顿号间隔，返回格式为[诉讼阶段：管辖法院名称] |

##### Setter方法
| 方法名      | 返回值数据类型 | 作用             |
| ----------- | -------------- | ---------------- |
| SetCaseType |  None           | 改变案件类型属性 |

参数

1 CaseType

* 类型：int
* 含义：传入的案件类型
* 取值范围：1、2、3
* 默认值：n/a
  
2 debugmode

* 类型：bool
* 含义：是否打开调试模式，如果打开则在命令行后台print对应输出结果
* 默认值：false


| 方法名              | 返回值数据类型 | 作用               |
| ------------------- | -------------- | ------------------ |
| SetLitigationAmount |  None           | 改变案件标的额属性 |

参数

1 LitigationAmount

* 类型：float
* 含义：传入的案件标的额数值
* 取值范围：n/a
* 默认值：n/a
  
2 debugmode

* 类型：bool
* 含义：是否打开调试模式，如果打开则在命令行后台print对应输出结果
* 默认值：false

| 方法名           | 返回值数据类型 | 作用         |
| ---------------- | -------------- | ------------ |
| SetCauseOfAction |  None           | 改变案由属性 |

参数

1 CauseOfAction

* 类型：str
* 含义：传入的案由字符串
* 取值范围：n/a
* 默认值：n/a
  
2 debugmode

* 类型：bool
* 含义：是否打开调试模式，如果打开则在命令行后台print对应输出结果
* 默认值：false

| 方法名              | 返回值数据类型 | 作用                 |
| ------------------- | -------------- | -------------------- |
| SetJurisdictionDict |  None           | 改变案件管辖法院属性 |

参数

1 InputJurisdictionDict

* 类型：dict
* 含义：传入的受理管辖法院字典
* 字典格式：{stage：JurisdictionName}，
* 默认值：n/a
  
2 debugmode

* 类型：bool
* 含义：是否打开调试模式，如果打开则在命令行后台print对应输出结果
* 默认值：false
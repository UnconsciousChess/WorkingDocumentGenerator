<script setup>
// 局部注册LitigantForm组件
import LitigantForm from "./LitigantForm.vue";

// 导入法院数据和案由数据
import courtData from "../../../data/public/Courts-China.json";
import causeOfActionData from "../../../data/public/CauseOfActions-China.json";

// 当事人表单实例（原告）
const litigantFormPlaintiff = ref(null);
// 当事人表单实例（被告）
const litigantFormDefendant = ref(null);

// 定义表单数据
const caseForm = ref({});

const componentsConfig = ref({
	inputInfoByFile: true,
	inputCaseInfoByFilePathDisabled: false,
	inputInfoByFileSwitchStatus: true,
});

// 表单引用
const caseFormRef = ref(null);
// 通过前端输入案件信息的输入框是否启用的状态，初始为false，即采用文件导入模式
const inputInfoByFrontEndStatus = ref(false);

// 决根据编辑模式，去决定是否显示描述列表，传递给子组件
const showDescriptionList = ref(false);

// 设定阶段的选择
const stageOptions = ref([
	{
		value: "一审",
		label: "一审阶段",
	},
	{
		value: "二审",
		label: "二审阶段",
	},
	{
		value: "再审",
		label: "再审阶段",
	},
	{
		value: "执行",
		label: "执行阶段",
	},
	{
		value: "仲裁",
		label: "仲裁阶段",
	},
]);

const caseAgentStageCheckboxOptions = ref([
	"一审立案",
	"一审庭审",
	"二审",
	"执行",
	"再审",
]);

const causeOfActionsOptions = ref(
	causeOfActionData.map((item) => {
		return {
			value: item,
			label: item,
		};
	})
);

const courtsOptions = ref(
	courtData.map((item) => {
		return {
			value: item,
			label: item,
		};
	})
);

// 设定表单的校验规则
const caseFormRules = ref({
	causeOfAction: [{required: true, message: "请选择案由", trigger: "blur"}],

	caseType: [{required: true, message: "请选择案件类型", trigger: "change"}],

	claimText: [{required: true, message: "请输入诉讼请求", trigger: "blur"}],
	factAndReason: [
		{required: true, message: "请输入事实与理由", trigger: "blur"},
	],
	rejectMediationReasonText: [
		{required: true, message: "请输入拒绝调解理由", trigger: "blur"},
	],
});

const caseFormRulesError = ref(null);

// 接收父组件传递的方法
const propData = defineProps({
	propCaseData: Object,
	propMode: String,
});

// 向父组件传递数据的事件
const emit = defineEmits(["updateCaseData"]);

// 监听案件信息的输入方式是否发生变化，文件/前端输入
function ChangeInputStatus() {
	if (componentsConfig.value.inputInfoByFile == true) {
		inputInfoByFrontEndStatus.value = false;
		console.log("关闭前端输入信息模式，开启文件读入模式");
		// 重置文本框状态
		componentsConfig.value.inputCaseInfoByFilePathDisabled = false;
		caseForm.value.inputCaseInfoByFilePath = "";
		componentsConfig.value.inputInfoByFile = true;
	} else {
		// 启用其他输入框
		inputInfoByFrontEndStatus.value = true;
		console.log("关闭文件读入模式，开启前端输入信息模式");
		componentsConfig.value.inputInfoByFile = false;
	}
}

// ====== 下面是和子组件【案件当事人信息表单】相关的方法 ======

// 新增原告方法
function onAddPlaintiff() {
	caseForm.value.plaintiffs.push({
		litigantName: "",
		litigantIdCode: "",
		litigantPhoneNumber: "",
		litigantPosition: "plaintiff",
		id: Date.now(),
	});
	console.log("新增了一个原告");
}

// 新增被告方法
function onAddDefendant() {
	caseForm.value.defendants.push({
		litigantName: "",
		litigantIdCode: "",
		litigantPhoneNumber: "",
		litigantPosition: "defendant",
		id: Date.now(),
	});
	console.log("新增了一个被告");
}

// 删除原告方法
function reducePlaintiff(id) {
	console.log("当前原告的id为" + id);
	// 在原告列表中找到该原告的位置
	var index = caseForm.value.plaintiffs.findIndex(
		(plaintiff) => plaintiff.id === id
	);
	caseForm.value.plaintiffs.splice(index, 1);
}

// 删除被告方法
function reduceDefendant(id) {
	console.log("当前被告的id为" + id);
	// 在被告列表中找到该被告的位置
	var index = caseForm.value.defendants.findIndex(
		(defendant) => defendant.id === id
	);
	caseForm.value.defendants.splice(index, 1);
}

const getCurrentplaintiffData = (plaintiffData, id) => {
	// 在原告列表中找到该原告的序号，并保存到index中
	var index = caseForm.value.plaintiffs.findIndex(
		(plaintiff) => plaintiff.id === id
	);
	// 赋值
	caseForm.value.plaintiffs[index] = plaintiffData;
};

const getCurrentDefendantData = (defendantData, id) => {
	// 在被告列表中找到该被告的位置
	var index = caseForm.value.defendants.findIndex(
		(defendant) => defendant.id === id
	);
	// 赋值
	caseForm.value.defendants[index] = defendantData;
};

// 将该方法提供给子组件
provide("reducePlaintiff", reducePlaintiff);
provide("reduceDefendant", reduceDefendant);
provide("getCurrentplaintiffData", getCurrentplaintiffData);
provide("getCurrentDefendantData", getCurrentDefendantData);

// ====== 下面是和webview的交互部分的方法 ======

// 选中“选择文件按钮”,调用后端python来弹出文件选择框
async function promptFileSelection() {
	// 判断是否有pywebview对象
	if (typeof pywebview === "undefined") {
		console.log("未链接到后端");
		return;
	}
	// 调用后端的方法，弹出文件选择框
	else {
		caseForm.value.inputCaseInfoByFilePath = await pywebview.api.GetFilepath();
		// 读取完毕以后禁用文本框
		componentsConfig.value.inputCaseInfoByFilePathDisabled = true;
	}
}

// 提交案件信息到后端的方法
async function onSubmit() {
	// 先判断目前是采取何种形式提交信息

	// 如果采取的是文件上传
	if (componentsConfig.value.inputInfoByFile == true) {
		// // 将案件信息传递给父组件
		// emit("updateCaseData", caseForm.value);

		// 判断是否有pywebview对象，如果有则将案件信息的字典传递给后端，如果没有就提示未链接到后端
		if (typeof pywebview === "undefined") {
			console.log("onSubmit()：未链接到后端");
			return;
		} else {
			// 如果是文件路径输入模式，则将文件的路径以及文件夹生成路径传递给后端
			pywebview.api.inputSingleCaseFromJson(
				caseForm.value.inputCaseInfoByFilePath
			); //关于pywebview的部分在组合前后端的时候再使用
			return;
		}
	}

	// 如果采取的是前端输入
	else {
		// 先校验表单
		await caseFormRef.value.validate((valid) => {
			if (!valid) {
				// 如果表单校验不通过;
				ElMessage({
					message: "表单校验不通过",
					type: "error",
				});
				caseFormRulesError.value = true;
			} else {
				// 如果表单校验通过
				// ElMessage({
				// 	message: "表单校验通过",
				// 	type: "success",
				// });
				caseFormRulesError.value = false;
			}
		});

		// 如果表单校验不通过，则不提交
		if (caseFormRulesError.value == true) {
			console.log("表单校验不通过，不提交");
			return;
		} else {
			console.log("表单校验通过，提交");
			// 判断是否有pywebview对象，如果有则将案件信息的字典传递给后端
			// 如果没有就提示未链接到后端
			if (typeof pywebview === "undefined") {
				console.log("onSubmit()：未链接到后端");
				return;
			} else {
				if (propData.propMode == "create") {
					// 将案件信息的字典传递给后端
					const result = await pywebview.api.inputSingleCaseFromFrontEndForm(
						caseForm.value
					);
					console.log(result);
					if (result == "Success") {
						ElMessage({
							message: "案件已经新建完毕",
							type: "success",
						});
						// 触发父组件的事件，让其从后端更新案件信息
						emit("updateCaseData");
					}
				} else if (propData.propMode == "edit") {
					// 将案件信息的字典传递给后端,更新案件信息
					const result = await pywebview.api.updateSingleCaseFromFrontEndForm(
						caseForm.value
					);
					console.log(result);
					if (result == "Success") {
						ElMessage({
							message: "案件信息已经更新成功",
							type: "success",
						});
						// 触发父组件的事件，让其从后端更新案件信息
						emit("updateCaseData");
					}
				}
			}
		}
	}
}

function caseFormInfoInitiation(propData) {
	// 已有案件内容以后的编辑模式
	if (propData.propMode == "edit") {
		console.log("当前CaseInfoform为编辑模式");

		if (propData.propCaseData == null) {
			console.log("没有传递过来案件信息");
			return;
		}
		// 如果有传递过来的案件信息，则将其赋值给表单
		caseForm.value = propData.propCaseData;

		// 编辑模式，对应进行下面的设置

		// 不显示文件导入模式的开关
		componentsConfig.value.inputInfoByFileSwitchStatus = false;
		// 打开前端输入状态
		inputInfoByFrontEndStatus.value = true;
		// 不需要文件导入
		componentsConfig.value.inputInfoByFile = false;

		// 默认显示描述列表
		showDescriptionList.value = true;
	}

	// 新建案件的创建模式
	else if (propData.propMode == "create") {
		console.log("当前CaseInfoform为新建案件模式");

		// 所有信息回归初始值
		caseForm.value.agentCondition = {
			agentFixedFee: null,
			riskAgentStatus: false,
			riskAgentUpfrontFee: "",
			riskAgentPostFeeRate: "",
			agentStage: [],
		};

		caseForm.value.caseId = "";
		caseForm.value.causeOfAction = "";
		caseForm.value.litigationAmount = "";
		caseForm.value.stages = [
			{
				stageName: "",
				courtName: "",
				caseNumber: "",
			},
		];

		caseForm.value.caseType = "";
		caseForm.value.mediationIntention = true;
		caseForm.value.caseFolderGeneratedPath = "";

		caseForm.value.factAndReason = "";
		caseForm.value.claimText = "";
		caseForm.value.rejectMediationReasonText = "";

		caseForm.value.startTime = new Date();

		caseForm.value.plaintiffs = [];
		caseForm.value.defendants = [];

		// 因为是新建模式，对应进行设置

		// 显示文件导入模式的开关
		componentsConfig.value.inputInfoByFileSwitchStatus = true;
		// 关闭前端输入状态，
		inputInfoByFrontEndStatus.value = false;
		// 默认需要文件导入
		componentsConfig.value.inputInfoByFile = true;
		// 不显示描述列表
		showDescriptionList.value = false;
	}
}

const testOutput = () => {
	console.log(caseForm.value.caseType);
};

// ====== 下面是在挂载时调用的方法 ======
onMounted(() => {
	caseFormInfoInitiation(propData);
});

// ====== 下面是在更新时调用的方法 ======
watchEffect(() => {
	console.log("案件信息表单已经更新");
	caseFormInfoInitiation(propData);
});
</script>

<template>
	<el-form
		v-bind:model="caseForm"
		v-bind:rules="caseFormRules"
		label-width="150"
		style="max-width: 900px"
		ref="caseFormRef"
	>
		<el-form-item>
			<el-button type="primary" plain @click="onAddPlaintiff"
				>原告<el-icon style="margin-left: 5px"><CirclePlusFilled /></el-icon
			></el-button>
			<el-button type="warning" plain @click="onAddDefendant"
				>被告<el-icon style="margin-left: 5px"><CirclePlusFilled /></el-icon
			></el-button>
			<el-button
				type="success"
				plain
				@click="onSubmit(ruleFormRef)"
				style="margin-left: 190px"
				>确认提交<el-icon style="margin-left: 5px"><Finished /></el-icon
			></el-button>
		</el-form-item>

		<el-form-item v-if="componentsConfig.inputInfoByFileSwitchStatus">
			<el-switch
				@change="ChangeInputStatus"
				v-model="componentsConfig.inputInfoByFile"
				style="--el-switch-on-color: #13ce76; --el-switch-off-color: #ff4949"
				active-text="文件导入模式"
				inactive-text="前端输入模式"
			/>
		</el-form-item>

		<!-- 文件导入模式 -->
		<div v-if="!inputInfoByFrontEndStatus">
			<el-form-item label="案件信息文件路径">
				<el-input
					v-model="caseForm.inputCaseInfoByFilePath"
					:disabled="componentsConfig.inputCaseInfoByFilePathDisabled"
					placeholder="仅支持txt文件和xlsx文件"
					style="max-width: 300px"
				/>
				<el-button @click="promptFileSelection">选择文件 </el-button>
			</el-form-item>
		</div>

		<!-- 前端输入模式 -->
		<div v-if="inputInfoByFrontEndStatus">
			<!-- 第1行 -->
			<el-row>
				<el-form-item label="案由">
					<el-select-v2
						v-model="caseForm.causeOfAction"
						filterable
						placeholder="请选择案由"
						style="width: 240px"
						:options="causeOfActionsOptions"
						:value="causeOfActionsOptions.value"
						margin-right
						prop="causeOfAction"
					/>
				</el-form-item>

				<el-form-item label="案件开始时间">
					<el-date-picker
						v-model="caseForm.startTime"
						type="date"
						placeholder="choose"
						value-format="YYYY-MM-DD"
						style="width: 240px"
						margin-right
					/>
				</el-form-item>
			</el-row>

			<!-- 第2行 -->
			<el-row>
				<el-form-item label="标的额" prop="litigationAmount">
					<el-input
						v-model.number="caseForm.litigationAmount"
						placeholder="计价单位：人民币元"
						style="width: 240px"
						margin-right
					/>
				</el-form-item>

				<el-form-item label="风险收费">
					<el-switch
						v-model="caseForm.agentCondition.riskAgentStatus"
						margin-right
					/>
				</el-form-item>

				<el-form-item label="愿意调解">
					<el-switch v-model="caseForm.mediationIntention" margin-right />
				</el-form-item>
			</el-row>

			<!-- 第3行 -->
			<el-row>
				<el-form-item>
					<el-button
						type="info"
						@click="
							caseForm.stages.push({
								stageName: '',
								courtName: '',
								caseNumber: '',
							})
						"
						>案件阶段<el-icon style="margin-left: 5px"><Plus /></el-icon
					></el-button>
				</el-form-item>

				<el-form-item>
					案件类型：
					<el-radio-group v-model="caseForm.caseType" @change="testOutput">
						<el-radio label="民事案件" :value="1"></el-radio>
						<el-radio label="行政案件" :value="2"></el-radio>
						<el-radio label="执行案件" :value="3"></el-radio>
					</el-radio-group>
				</el-form-item>
			</el-row>

			<!-- 案件阶段信息【不是委托阶段！】 -->
			<template v-for="stage in caseForm.stages">
				<el-form-item>
					<el-row>
						<el-select
							v-model="stage.stageName"
							placeholder="请选择案件各阶段信息"
							style="width: 100px; margin-right: 15px"
						>
							<el-option
								v-for="item in stageOptions"
								:key="item.value"
								:label="item.label"
								:value="item.value"
							></el-option>
						</el-select>

						<el-select-v2
							v-model="stage.courtName"
							filterable
							placeholder="请选择管辖法院"
							style="width: 200px; margin-right: 10px"
							:options="courtsOptions"
							:value="courtsOptions.value"
						/>

						<el-input
							v-model="stage.caseNumber"
							placeholder="请输入案号"
							style="width: 250px"
						/>

						<el-button
							type="danger"
							:icon="Delete"
							@click="caseForm.stages.splice(caseForm.stages.indexOf(stage), 1)"
							style="margin-left: 10px"
						>
							<el-icon><Delete /></el-icon>
						</el-button>
					</el-row>
				</el-form-item>
			</template>

			<!-- 第5行 -->
			<el-row v-if="caseForm.agentCondition.riskAgentStatus == true">
				<el-form-item label="前期收费金额">
					<el-input
						v-model="caseForm.agentCondition.riskAgentUpfrontFee"
						style="width: 100px"
						margin-right
					/>
				</el-form-item>

				<el-form-item label="风险收费比例">
					<el-input
						v-model="caseForm.agentCondition.riskAgentPostFeeRate"
						style="width: 100px"
						margin-right
					/>
				</el-form-item>
			</el-row>

			<!-- 第6行 -->
			<el-row>
				<el-form-item>
					委托阶段：
					<el-checkbox-group
						v-model="caseForm.agentCondition.agentStage"
						@change="console.log(caseForm.agentCondition.agentStage)"
					>
						<el-checkbox
							v-for="(stage, index) in caseAgentStageCheckboxOptions"
							:value="index + 1"
						>
							{{ stage }}
						</el-checkbox>
					</el-checkbox-group>
				</el-form-item>
			</el-row>

			<el-form-item label="诉讼请求" prop="claimText">
				<el-input
					v-model="caseForm.claimText"
					type="textarea"
					style="width: 650px"
					:rows="4"
				/>
			</el-form-item>

			<el-form-item label="事实与理由" prop="factAndReason">
				<el-input
					v-model="caseForm.factAndReason"
					type="textarea"
					style="width: 650px"
					:rows="8"
				/>
			</el-form-item>

			<el-form-item
				v-if="caseForm.mediationIntention == false"
				label="拒绝调解理由"
			>
				<el-input
					v-model="caseForm.rejectMediationReasonText"
					type="textarea"
					style="width: 650px"
					:rows="2"
				/>
			</el-form-item>

			<el-form-item label="案件文件夹生成路径" prop="caseFolderGeneratedPath">
				<el-input
					v-model="caseForm.caseFolderGeneratedPath"
					style="width: 650px"
				/>
			</el-form-item>
		</div>
	</el-form>

	<!-- 当事人表格组件 -->

	<!-- 原告部分 -->
	<div v-for="plaintiff in caseForm.plaintiffs" :key="plaintiff.id">
		<LitigantForm
			ref="litigantFormPlaintiff"
			:litigant="plaintiff"
			:show-description-list="showDescriptionList"
		/>
	</div>

	<!-- 被告部分 -->
	<div v-for="defendant in caseForm.defendants" :key="defendant.id">
		<LitigantForm
			ref="litigantFormDefendant"
			:litigant="defendant"
			:show-description-list="showDescriptionList"
		/>
	</div>
</template>

<style>
.margin-right {
	margin-right: 10px;
}
</style>

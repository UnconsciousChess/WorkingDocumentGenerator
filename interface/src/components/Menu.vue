<script setup>
const activeIndex = ref("1");
// 默认不显示About的dialog
const aboutDialogVisible = ref(false);

function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

async function init() {
	// 等待1000ms，等待后端的服务启动，避免前端调用后端的函数失败
	await sleep(1000);

	// 检测是否连接了后端服务，如果未连接，则在前端提示仅是测试前端
	if (typeof pywebview === "undefined") {
		ElNotification({
			title: "程序初始化",
			message: "未检测到后端服务，仅测试前端内容",
		});
		return;
	}

	// 调用后端的函数appStartInit，初始化后端的数据（如果后端已经初始化，后端会识别）
	let result = await pywebview.api.appStartInit();
	if (
		result.caseResult == "Success" &&
		result.templateFileResult == "Success"
	) {
		// 初始化成功
		ElNotification({
			title: "程序初始化",
			message: "已成功加载后台数据！",
			duration: 3500,
		});
	} else {
		// 初始化失败
		ElNotification({
			title: "程序初始化",
			message: "后台数据加载失败！",
		});
	}
}

onMounted(() => {
	init();
});
</script>

<template>
	<el-menu
		:default-active="activeIndex"
		:router="true"
		class="el-menu-demo"
		mode="horizontal"
	>
		<el-menu-item index="/">律师小只工具箱</el-menu-item>

		<el-sub-menu index="2">
			<template #title>数据管理</template>
			<el-menu-item index="/case-info-table">案件列表</el-menu-item>
			<el-menu-item index="/template-file">模板列表</el-menu-item>
			<!-- <el-menu-item index="/test" disabled>测试</el-menu-item> -->
		</el-sub-menu>

		<el-sub-menu index="3">
			<template #title>常用工具</template>

			<el-sub-menu index="">
				<template #title>各类计算器</template>
				<el-menu-item index="/caculator">诉讼费用计算器</el-menu-item>
				<el-menu-item index="" disabled>人身损害计算器</el-menu-item>
				<el-menu-item index="" disabled>劳动案件计算器</el-menu-item>
			</el-sub-menu>

			<el-menu-item index="" disabled>还没有想好的功能</el-menu-item>
		</el-sub-menu>

		<el-menu-item index="" @click="aboutDialogVisible = true"
			>关于</el-menu-item
		>
	</el-menu>

	<el-dialog
		v-model="aboutDialogVisible"
		title="关于本程序"
		width="300"
		draggable
	>
		<p>Version:0.3</p>
		<p>一只肥猫开发ing.....ZZzzzz</p>
	</el-dialog>
</template>

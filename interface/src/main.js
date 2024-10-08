// 导入App.vue
import App from "./App.vue";
// 导入router
import {createMemoryHistory, createRouter} from "vue-router";

import * as ElementPlusIconsVue from "@element-plus/icons-vue";

// 导入组件
import Caculator from "./components/Caculator.vue";
import Blank from "./components/Blank.vue";
import CaseInfoShowNew from "./components/CaseInfoShowTable2.vue";
import TemplateFileTable from "./components/TemplateFileTable.vue";

// 设置路由
const routes = [
	{path: "/", component: Blank},
	{path: "/caculator", component: Caculator},
	{path: "/case-info-table", component: CaseInfoShowNew},
	{path: "/template-file", component: TemplateFileTable},
];

// 创建router的实例
const router = createRouter({
	history: createMemoryHistory(),
	routes,
});

// 创建Vue实例app
const app = createApp(App);

// 注册ElementPlusIconsVue
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
	app.component(key, component);
}

// app使用router
app.use(router);

// 将app挂载到id为vueapp的dom上
app.mount("#vueapp");

# Heap Snapshot Analysis Guide

## 抓取步骤

### 1. 启动应用
```bash
cd /home/yua/suw/lwg-gui-tauri
npm run tauri:dev
```

### 2. 打开 DevTools
- 按 `F12` 或 `Ctrl+Shift+I`
- 切换到 **Memory** 标签页

### 3. 抓取时间表

| 时间点 | 操作 | 标记名称 |
|--------|------|----------|
| T+0 | Take Snapshot | Baseline |
| T+5min | Take Snapshot | After_5min |
| T+10min | Take Snapshot | After_10min |

### 4. 分析视图设置
1. 选择 **After_10min** 快照
2. 右上角下拉选择 **Comparison**
3. 对比对象选 **Baseline**
4. 按 **# Delta** 降序排序

## 预期泄漏对象分析

### 如果看到 `SVGPathElement` 增长
- **含义**: Recharts 每次渲染创建新 SVG 路径节点
- **证据**: Delta > 1000, Constructor = SVGPathElement
- **解决**: 需要缓存图表组件或使用 Canvas 替代

### 如果看到 `ResizeObserver` 增长  
- **含义**: ResponsiveContainer 的 observer 未清理
- **证据**: Delta = 10-20 (图表数量), Constructor = ResizeObserver
- **解决**: 必须替换 ResponsiveContainer

### 如果看到 `Array` 或 `Object` 增长
- **含义**: 数据数组或状态对象累积
- **证据**: Delta 很大, 可能是 cpuHistory/memHistory 数组
- **解决**: 检查 useSystemStats 中的数据转换逻辑

### 如果看到 `Detached HTMLElement`
- **含义**: DOM 节点已移除但 JS 仍持有引用
- **证据**: 任何数量都说明泄漏
- **解决**: 检查 useEffect cleanup 函数

### 如果以上都没有明显增长
- **含义**: 泄漏在 WebKitGTK 层（C++ 层），不在 JS 层
- **解决**: 需要升级 WebKitGTK 版本

## 截图模板

请提供以下截图：

1. **快照列表** - 显示 Baseline、After_5min、After_10min
2. **Comparison 视图前10行** - 按 # Delta 排序
3. **展开增长最多的对象详情** - 点击 Constructor 名称查看 retained size

## 数据记录表

| Constructor | Baseline Count | After_10min Count | # Delta | Size Delta | 分析结论 |
|-------------|----------------|-------------------|---------|------------|----------|
| (示例) SVGPathElement | 120 | 3120 | +3000 | 15MB | 确认泄漏源 |
| | | | | | |
| | | | | | |

请在表格中填入实际数据。

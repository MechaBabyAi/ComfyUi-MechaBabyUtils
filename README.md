# ComfyUi-MechaBabyUtils

ComfyUI custom nodes collection by MechaBaby - A set of utility nodes for ComfyUI workflow enhancement.

MechaBaby 的 ComfyUI 自定义节点集合。包含以下实用节点：

## 节点列表

### 文本处理节点 (MechBabyUtils/Text)

- **StringLineCounter（字符串行数统计）**：统计输入字符串的行数。

- **StringListMerger（文本列表合并器）**：将两个文本列表中的项进行合并。
  - 输入1：文本列表（按顺序从上到下选择），每行一项
  - 输入2：文本列表（可顺序或随机选择），每行一项，自动去除空白行
  - 选择模式：顺序选择或随机选择（不重复）
  - 补充文本：当输入2列表项数量小于输入1时，可使用补充文本
  - 输出：所有组合结果，每行一个（输入1项+输入2项的组合）
  - 支持多种输入格式：字符串、列表、元组等

- **StringToStringList（字符串转字符串列表）**：将字符串按分隔符分割为字符串列表（StringListToString 的反向操作）。
  - 输入：字符串（可通过输入连接）
  - 分隔符：用于分割字符串的分隔符（默认：`\n` 表示换行符）
  - 移除空项：是否自动移除分割后的空项（默认：是）
  - 去除空白：是否去除每项的前后空白字符（默认：是）
  - 输出：字符串列表（列表格式，类似 Switch(Any) 的输出，下游节点会对每个字符串执行一次）

### 音频处理节点 (MechBabyUtils/Audio)

- **MechBabyAudioCollector（IndexTTS 音频收集器）**：采集并保存 IndexTTS 音频。

### 图像处理节点 (MechBabyUtils/Image)

- **SimpAiMetadataReader（SimpAi 元数据读取）**：读取 SimpAi 图片内嵌的 JSON 元数据。

### 模型处理节点 (MechBabyUtils/Model)

- **ConditionalModelSelector（条件模型选择器）**：根据整数比较条件选择两个模型中的一个。
  - 模型1：第一个模型输入
  - 模型2：第二个模型输入
  - 输入值：输入的整数值（INT 类型）
  - 匹配值：节点上的整数值（INT 类型），用于比较
  - 输出：选中的模型
  - 逻辑：如果 `输入值 == 匹配值`，输出模型1；否则输出模型2

### 控制节点 (MechBabyUtils/Control)

- **BypassSwitch（绕过开关）**：在两个输入之间切换，并输出开关值。
  - 输入1：第一个输入（任意类型，可选）
  - 输入2：第二个输入（任意类型，可选）
  - 启用：开关（BOOLEAN 类型）
  - 输出：根据开关状态输出输入1或输入2
  - 开关值：输出开关的当前状态（BOOLEAN 类型）
  - 逻辑：如果 `启用 = True`，输出输入1；如果 `启用 = False`，输出输入2

## 安装

将项目放入 `ComfyUI/custom_nodes/` 目录，重启 ComfyUI 即可加载节点。

### 安装方法

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MechaBabyAi/ComfyUi-MechaBabyUtils.git
```

然后重启 ComfyUI 即可。

## 使用示例

### StringListMerger 使用示例

**输入1（文本框）**：
```
提示词1
提示词2
提示词3
```

**输入2（文本框）**：
```
风格A
风格B
```

**顺序模式输出**：
```
提示词1风格A
提示词2风格B
提示词3[补充文本]
```

**随机模式输出**：
```
提示词1风格B
提示词2风格A
提示词3[补充文本]
```

### StringToStringList 使用示例

**输入（字符串）**：
```
苹果,香蕉,橙子,葡萄
```

**分隔符**：`,`

**输出（字符串列表，每行一项）**：
```
苹果
香蕉
橙子
葡萄
```

**输入（字符串，使用换行符分隔）**：
```
第一项
第二项
第三项
```

**分隔符**：`\n`（默认）

**输出（字符串列表，列表格式）**：
- 输出为列表格式，包含 3 个字符串：`["第一项", "第二项", "第三项"]`
- 下游节点会对每个字符串执行一次，类似 Switch(Any) 的输出方式

### ConditionalModelSelector 使用示例

**场景**：根据条件选择不同的模型

**设置**：
- 模型1：连接到模型A
- 模型2：连接到模型B
- 输入值：5（从上游节点输入）
- 匹配值：5（节点上的值）

**结果**：
- 因为 `输入值(5) == 匹配值(5)`，所以输出模型1（模型A）

**如果输入值改为 3**：
- 因为 `输入值(3) != 匹配值(5)`，所以输出模型2（模型B）

### BypassSwitch 使用示例

**场景1：在两个模型之间切换**
- 输入1：连接到模型A
- 输入2：连接到模型B
- 启用 = True：输出模型A
- 启用 = False：输出模型B
- 开关值：始终输出开关的当前状态（True 或 False）

**场景2：在两个图像之间切换**
- 输入1：连接到图像A
- 输入2：连接到图像B
- 启用 = True：输出图像A
- 启用 = False：输出图像B
- 开关值：可用于下游节点判断当前使用的是哪个输入

## 许可证

本项目基于 MIT License 发布。

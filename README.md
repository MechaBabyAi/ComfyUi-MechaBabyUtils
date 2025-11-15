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

### 音频处理节点 (MechBabyUtils/Audio)

- **MechBabyAudioCollector（IndexTTS 音频收集器）**：采集并保存 IndexTTS 音频。

### 图像处理节点 (MechBabyUtils/Image)

- **SimpAiMetadataReader（SimpAi 元数据读取）**：读取 SimpAi 图片内嵌的 JSON 元数据。

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

## 许可证

本项目基于 MIT License 发布。

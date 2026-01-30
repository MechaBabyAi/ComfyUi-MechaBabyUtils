# ComfyUi-MechaBabyUtils

ComfyUI custom nodes collection by MechaBaby — a set of utility nodes for ComfyUI workflow enhancement.

**English | [中文](README.md)**

---

## Node List

### Text (MechBabyUtils/Text)

- **StringLineCounter** — Counts lines in the input string.

- **SaveText** — Saves text to the ComfyUI output directory (same behavior as Save Image).
  - Saves under ComfyUI’s output directory; subfolders can be specified via the filename prefix.
  - Input: single text (`text`) or a text list (`text_list`; when wired, items are joined with the list line separator before saving).
  - List line separator: delimiter between list items (default `\n`; can use `\r\n`, `,`, etc.; escape sequences supported).
  - Filename prefix: same format as Save Image, e.g. `%date:yyyy-MM-dd%/Result`, `%year%`, `%month%`, `%day%`; can include subpaths.
  - File extension: e.g. `.txt`, `.json`, `.log`, `.csv`, `.md`.
  - Output: absolute path of the saved file (empty string on failure).

- **StringListMerger** — Merges items from two text lists.
  - List 1: one item per line, selected in order top to bottom.
  - List 2: one item per line, selected in order or at random; blank lines removed.
  - Mode: sequential or random (no duplicates).
  - Supplement text: used when list 2 has fewer items than list 1.
  - Output: one merged line per pair (list1 item + list2 item).
  - Accepts string, list, tuple, etc.

- **StringToStringList** — Splits a string by a delimiter into a string list (inverse of list-to-string).
  - Input: string (can be wired).
  - Delimiter: e.g. `\n` for newline (default).
  - Remove empty: drop empty segments (default: yes).
  - Strip items: trim each segment (default: yes).
  - Output: string list (downstream runs once per string, like Switch(Any)).

### Audio (MechBabyUtils/Audio)

- **MechBabyAudioCollector** — Captures and saves IndexTTS audio.

### Image (MechBabyUtils/Image)

- **SimpAiMetadataReader** — Reads SimpAi JSON metadata embedded in images.

### Model (MechBabyUtils/Model)

- **ConditionalModelSelector** — Picks one of two models by an integer comparison.
  - Model 1 / Model 2: the two model inputs.
  - Input value: integer from upstream (INT).
  - Match value: integer on the node (INT) used for comparison.
  - Output: selected model.
  - Logic: if `input_value == match_value` then model 1, else model 2.

### Control (MechBabyUtils/Control)

- **BypassSwitch** — Switches between two inputs and outputs the switch value.
  - Input 1 / Input 2: any type (optional).
  - Enabled: BOOLEAN.
  - Output: input 1 or input 2 depending on switch.
  - Switch value: current BOOLEAN state.
  - Logic: enabled → input 1; disabled → input 2.

- **SelectByIndex** — Multiple same-type inputs plus an index; outputs the selected input and the index (any type).
  - Index (selected_index): 1–16 (clamped if out of range).
  - Inputs: input_1 … input_16 (any type, optional), up to 16 channels.
  - Output: the selected channel (same type as inputs).
  - Selected index: INT 1–16 actually used.
  - Logic: index N → output input_N; unconnected inputs are None.

- **OutputPathSelector** — Chooses one of two output paths; the other path is blocked from executing.
  - Input: any type (optional).
  - Enabled: BOOLEAN.
  - Output 1: receives input when enabled, else execution blocked.
  - Output 2: receives input when disabled, else execution blocked.
  - Uses ExecutionBlocker so the unused path does not run (no None passed).

- **OutputPathSelectorAdvanced** — One input, 16 output ports; only the selected port outputs, others blocked.
  - Input: any type (optional).
  - Port number: 1–16 (manual or wired).
  - Block if input None: when enabled, all ports block when input is None.
  - Outputs: output1 … output16; only the selected port has data.
  - Selected port number: INT output.
  - Logic: selected port gets input; others use ExecutionBlocker.
  - Supports wired port index and optional blocking on None.

---

## Installation

Place the repo under `ComfyUI/custom_nodes/`, then restart ComfyUI.

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MechaBabyAi/ComfyUi-MechaBabyUtils.git
```

Restart ComfyUI after cloning.

---

## Examples

### SaveText

- **Single text:** Set filename prefix (e.g. `Result` or `%date:yyyy-MM-dd%/Result`), extension (e.g. `.txt`), and `text`. File is written under the output directory (e.g. `output/Result_00001_.txt` or `output/2025-01-29/Result_00001_.txt`).
- **Text list:** Wire a string list to `text_list`, set list line separator (default `\n`). Content is joined with that separator and saved.
- **Date subfolder:** e.g. prefix `%date:yyyy-MM-dd%/logs`, extension `.log` → file under `output/2025-01-29/logs_00001_.log`.

### StringListMerger

- List 1: one item per line (e.g. prompt1, prompt2, prompt3). List 2: e.g. styleA, styleB. Sequential → prompt1+styleA, prompt2+styleB, prompt3+supplement. Random → pairs chosen without repetition.

### StringToStringList

- Input e.g. `apple,banana,orange`, delimiter `,` → list of three strings. With newline delimiter `\n`, multi-line input becomes a list; downstream runs once per item.

### ConditionalModelSelector

- Wire model A to model 1, model B to model 2. Input value 5, match value 5 → output model A. Input value 3 → output model B.

### BypassSwitch

- Wire model A to input 1, model B to input 2. Enabled → output A; disabled → output B. Switch value output reflects current state.

### SelectByIndex

- Wire models A–D to input_1 … input_4, index 3 → output model C, selected_index 3.
- Wire 8 images to input_1 … input_8, index 5 → output 5th image, selected_index 5.
- Index 20 → clamped to 16; output input_16, selected_index 16.

### OutputPathSelector

- One input, two paths. Enabled → path 1 runs; disabled → path 2 runs. Unused path is blocked (no None).

### OutputPathSelectorAdvanced

- One input, 16 ports. Set port 1–16 (or wire an INT). Only that port outputs; others blocked. Optional: block all when input is None.

---

## License

MIT License.

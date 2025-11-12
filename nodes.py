import json
import os
from datetime import datetime
from typing import List

import folder_paths
import torch
import torchaudio
from PIL import Image


class StringLineCounter:
    """统计字符串行数的自定义节点。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("line_count",)
    FUNCTION = "count_lines"
    CATEGORY = "MechBabyUtils/Text"

    def count_lines(self, text: str):
        if not text:
            return (0,)

        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        line_count = normalized.count("\n") + 1
        return (line_count,)


class MechBabyAudioCollector:
    """收集 IndexTTS 音频并按需保存的自定义节点。"""

    def __init__(self):
        self._display_entries: List[str] = []
        self._saved_paths: List[str] = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "auto_save": ("BOOLEAN", {"default": True, "label_on": "开启", "label_off": "关闭"}),
                "output_subdir": ("STRING", {"default": "", "multiline": False, "placeholder": "可选：相对 output 的子目录"}),
                "filename_prefix": ("STRING", {"default": "MechBabyAudio", "multiline": False, "placeholder": "文件名前缀"}),
                "file_format": ("STRING", {"default": "wav", "choices": ["wav", "flac"]}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_paths",)
    FUNCTION = "collect"
    CATEGORY = "MechBabyUtils/Audio"

    def collect(self, audio, auto_save: bool, output_subdir: str, filename_prefix: str, file_format: str):
        saved_path = None
        display_entry = "未保存音频"

        waveform = audio.get("waveform")
        sample_rate = int(audio.get("sample_rate", 44100))

        if not isinstance(filename_prefix, str) or not filename_prefix.strip():
            filename_prefix = "MechBabyAudio"
        filename_prefix = filename_prefix.strip()

        if not isinstance(output_subdir, str):
            output_subdir = ""
        output_subdir = output_subdir.strip().replace("\\", "/")

        file_format = (file_format or "wav").lower()
        if file_format not in {"wav", "flac"}:
            file_format = "wav"

        if auto_save:
            base_dir = folder_paths.get_output_directory()
            target_dir = os.path.join(base_dir, output_subdir) if output_subdir else base_dir
            os.makedirs(target_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{filename_prefix}_{timestamp}.{file_format}"
            saved_path = os.path.join(target_dir, filename)

            try:
                if isinstance(waveform, torch.Tensor):
                    tensor = waveform.detach().cpu()
                else:
                    tensor = torch.tensor(waveform)

                if tensor.dim() == 3:
                    tensor = tensor[0]
                if tensor.dim() == 1:
                    tensor = tensor.unsqueeze(0)

                tensor = tensor.to(torch.float32).clamp(-1.0, 1.0)
                torchaudio.save(saved_path, tensor, sample_rate, format=file_format)
                saved_path = os.path.abspath(saved_path)
                display_entry = saved_path
                self._saved_paths.append(saved_path)
            except Exception as exc:
                display_entry = f"保存失败: {exc}"
                saved_path = None
        else:
            display_entry = "未保存音频"

        self._display_entries.append(display_entry)
        ui_lines = [f"{idx + 1}. {entry}" for idx, entry in enumerate(self._display_entries)]
        output_string = "\n".join(self._saved_paths)

        return {"ui": {"text": ui_lines}, "result": (output_string,)}


class SimpAiMetadataReader:
    """读取 SimpAi 图片内嵌 JSON 元数据的自定义节点。"""

    _FIELD_SCHEMAS = [
        {
            "output_name": "metadata_scheme",
            "json_key": "Metadata Scheme",
            "type": "STRING",
            "default": "",
            "label": "Metadata Scheme",
        },
        {
            "output_name": "version",
            "json_key": "Version",
            "type": "STRING",
            "default": "",
            "label": "Version",
        },
        {
            "output_name": "backend_engine",
            "json_key": "Backend Engine",
            "type": "STRING",
            "default": "",
            "label": "Backend Engine",
        },
        {
            "output_name": "base_model",
            "json_key": "Base Model",
            "type": "STRING",
            "default": "",
            "label": "Base Model",
        },
        {
            "output_name": "base_model_hash",
            "json_key": "Base Model Hash",
            "type": "STRING",
            "default": "",
            "label": "Base Model Hash",
        },
        {
            "output_name": "vae",
            "json_key": "VAE",
            "type": "STRING",
            "default": "",
            "label": "VAE",
        },
        {
            "output_name": "sampler",
            "json_key": "Sampler",
            "type": "STRING",
            "default": "",
            "label": "Sampler",
        },
        {
            "output_name": "scheduler",
            "json_key": "Scheduler",
            "type": "STRING",
            "default": "",
            "label": "Scheduler",
        },
        {
            "output_name": "performance",
            "json_key": "Performance",
            "type": "STRING",
            "default": "",
            "label": "Performance",
        },
        {
            "output_name": "image2image",
            "json_key": "Image2Image",
            "type": "STRING",
            "default": "",
            "label": "Image2Image",
        },
        {
            "output_name": "resolution",
            "json_key": "Resolution",
            "type": "STRING",
            "default": "",
            "label": "Resolution",
        },
        {
            "output_name": "prompt",
            "json_key": "Prompt",
            "type": "STRING",
            "default": "",
            "label": "Prompt",
            "value_kind": "maybe_list",
        },
        {
            "output_name": "negative_prompt",
            "json_key": "Negative Prompt",
            "type": "STRING",
            "default": "",
            "label": "Negative Prompt",
        },
        {
            "output_name": "full_prompt",
            "json_key": "Full Prompt",
            "type": "STRING",
            "default": "",
            "label": "Full Prompt",
            "value_kind": "list",
        },
        {
            "output_name": "full_negative_prompt",
            "json_key": "Full Negative Prompt",
            "type": "STRING",
            "default": "",
            "label": "Full Negative Prompt",
            "value_kind": "list",
        },
        {
            "output_name": "styles",
            "json_key": "Styles",
            "type": "STRING",
            "default": "",
            "label": "Styles",
        },
        {
            "output_name": "styles_definition",
            "json_key": "styles_definition",
            "type": "STRING",
            "default": "",
            "label": "styles_definition",
        },
        {
            "output_name": "fooocus_v2_expansion",
            "json_key": "Fooocus V2 Expansion",
            "type": "STRING",
            "default": "",
            "label": "Fooocus V2 Expansion",
        },
        {
            "output_name": "adm_guidance",
            "json_key": "ADM Guidance",
            "type": "STRING",
            "default": "",
            "label": "ADM Guidance",
        },
        {
            "output_name": "guidance_scale",
            "json_key": "Guidance Scale",
            "type": "FLOAT",
            "default": 0.0,
            "label": "Guidance Scale",
        },
        {
            "output_name": "refiner_model",
            "json_key": "Refiner Model",
            "type": "STRING",
            "default": "",
            "label": "Refiner Model",
        },
        {
            "output_name": "refiner_switch",
            "json_key": "Refiner Switch",
            "type": "FLOAT",
            "default": 0.0,
            "label": "Refiner Switch",
        },
        {
            "output_name": "sharpness",
            "json_key": "Sharpness",
            "type": "FLOAT",
            "default": 0.0,
            "label": "Sharpness",
        },
        {
            "output_name": "steps",
            "json_key": "Steps",
            "type": "INT",
            "default": 0,
            "label": "Steps",
        },
        {
            "output_name": "seed",
            "json_key": "Seed",
            "type": "STRING",
            "default": "",
            "label": "Seed",
        },
        {
            "output_name": "lora_1",
            "json_key": "LoRA 1",
            "type": "STRING",
            "default": "",
            "label": "LoRA 1",
        },
        {
            "output_name": "lora_2",
            "json_key": "LoRA 2",
            "type": "STRING",
            "default": "",
            "label": "LoRA 2",
        },
        {
            "output_name": "loras",
            "json_key": "LoRAs",
            "type": "STRING",
            "default": "",
            "label": "LoRAs",
            "value_kind": "list",
        },
        {
            "output_name": "user",
            "json_key": "User",
            "type": "STRING",
            "default": "",
            "label": "User",
        },
    ]

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        files = folder_paths.filter_files_content_types(files, ["image"])
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
            },
            "optional": {
                "join_lists": ("BOOLEAN", {"default": True, "label_on": "拼接列表", "label_off": "保持JSON"}),
                "list_separator": ("STRING", {"default": "\\n", "multiline": False, "placeholder": "\\n"}),
            },
        }

    RETURN_TYPES = ("STRING",) + tuple(field["type"] for field in _FIELD_SCHEMAS)
    RETURN_NAMES = ("metadata_json",) + tuple(
        field["output_name"] for field in _FIELD_SCHEMAS
    )
    FUNCTION = "extract"
    CATEGORY = "MechBabyUtils/Image"

    def extract(self, image, join_lists=True, list_separator="\\n"):
        image_path = folder_paths.get_annotated_filepath(image)
        metadata = self._load_metadata(image_path)
        separator = self._build_separator(list_separator)

        json_text = json.dumps(metadata, ensure_ascii=False, indent=2)
        outputs = [json_text]
        ui_lines = []

        for field in self._FIELD_SCHEMAS:
            raw_value = metadata.get(field["json_key"], field["default"])
            converted = self._convert_value(
                raw_value,
                field["type"],
                field.get("value_kind"),
                join_lists,
                separator,
                field["default"],
            )
            outputs.append(converted)
            ui_lines.append(f"{field['label']}: {self._format_for_display(converted)}")

        return {"ui": {"text": ui_lines}, "result": tuple(outputs)}

    @staticmethod
    def _build_separator(user_input: str) -> str:
        if not isinstance(user_input, str):
            return "\n"
        try:
            return bytes(user_input, "utf-8").decode("unicode_escape")
        except Exception:
            return "\n"

    @classmethod
    def _convert_value(cls, value, target_type, value_kind, join_lists, separator, default):
        if target_type == "INT":
            return cls._to_int(value, default)
        if target_type == "FLOAT":
            return cls._to_float(value, default)
        return cls._to_string(value, value_kind, join_lists, separator, default)

    @staticmethod
    def _to_int(value, default):
        try:
            if value is None or value == "":
                return int(default)
            if isinstance(value, bool):
                return int(value)
            return int(float(value))
        except Exception:
            return int(default)

    @staticmethod
    def _to_float(value, default):
        try:
            if value is None or value == "":
                return float(default)
            if isinstance(value, bool):
                return float(int(value))
            return float(value)
        except Exception:
            return float(default)

    @classmethod
    def _to_string(cls, value, value_kind, join_lists, separator, default):
        if value is None:
            return str(default)
        if isinstance(value, (int, float, bool)):
            return str(value)
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            if not value:
                return ""
            if join_lists or value_kind == "maybe_list":
                flattened = []
                for item in value:
                    if isinstance(item, list):
                        flattened.append(
                            ", ".join(cls._stringify_element(i) for i in item)
                        )
                    else:
                        flattened.append(cls._stringify_element(item))
                return separator.join(flattened)
            return json.dumps(value, ensure_ascii=False)
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    @staticmethod
    def _stringify_element(item):
        if isinstance(item, (dict, list)):
            return json.dumps(item, ensure_ascii=False)
        return str(item)

    @staticmethod
    def _format_for_display(value):
        if isinstance(value, float):
            return f"{value:.6g}"
        if isinstance(value, (int, str)):
            return str(value)
        return json.dumps(value, ensure_ascii=False)

    @staticmethod
    def _load_metadata(image_path: str):
        with Image.open(image_path) as img:
            json_candidate = SimpAiMetadataReader._extract_json_from_image(img)
        if json_candidate is None:
            raise RuntimeError("未在图片元数据中找到 SimpAi JSON 信息")
        return json_candidate

    @staticmethod
    def _extract_json_from_image(img: Image.Image):
        # 优先在 EXIF 中查找
        exif = img.getexif()
        if exif:
            for tag_id, raw_value in exif.items():
                value = raw_value
                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8")
                    except Exception:
                        value = value.decode("utf-8", errors="ignore")
                if isinstance(value, str):
                    parsed = SimpAiMetadataReader._try_parse_json(value)
                    if parsed is not None:
                        return parsed

        # 其次检查 info 字段
        for value in img.info.values():
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8")
                except Exception:
                    value = value.decode("utf-8", errors="ignore")
            if isinstance(value, str):
                parsed = SimpAiMetadataReader._try_parse_json(value)
                if parsed is not None:
                    return parsed
        return None

    @staticmethod
    def _try_parse_json(value: str):
        text = value.strip()
        if not (text.startswith("{") and text.endswith("}")):
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None


NODE_CLASS_MAPPINGS = {
    "StringLineCounter": StringLineCounter,
    "MechBabyAudioCollector": MechBabyAudioCollector,
    "SimpAiMetadataReader": SimpAiMetadataReader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringLineCounter": "字符串行数统计",
    "MechBabyAudioCollector": "IndexTTS 音频收集器",
    "SimpAiMetadataReader": "SimpAi 元数据读取",
}


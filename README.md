# ChatGPT × 逢坂大河启动动画

Windows 桌面版 ChatGPT/Codex 的自定义启动动画工程。播放横屏角色视频后，用 Windows DWM 实时画面把**官方应用窗口**接入动画，再把操作交还给官方应用。不会复制或修改官方安装包。

启动器基于 [Dragon Codex Boot](https://github.com/yushua0808-cpu/dragon-codex-boot)（MIT）制作，保留了原项目的许可证和署名。本仓库增加大河主题的视频生成脚本与匹配的 10 秒交接配置。

**本仓库只开源代码和配置。** 用户插画、原动画配音及完整视频没有公开分发；软件的 MIT 许可证不授予这些素材的使用权。项目与 OpenAI、《龙与虎》及其权利方无关联。

## 本地制作

需要 Windows 10/11 x64、.NET Framework 4.8、Python 3、Pillow、FFmpeg，以及已安装的官方 ChatGPT/Codex 桌面版。

```powershell
python -m pip install Pillow
python .\scripts\render-taiga.py --image "C:\path\to\your-image.jpg" --audio "C:\path\to\your-audio.mp3"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build.ps1
Copy-Item .\build\DragonCodexBoot\DragonCodexBoot.exe .\dist\TaigaBoot\
Copy-Item .\build\DragonCodexBoot\scripts .\dist\TaigaBoot\ -Recurse
```

生成的 `dist/TaigaBoot` 中会有 `media/startup.mp4` 和 `launcher.json`。保持这些文件与 `DragonCodexBoot.exe` 在同一目录下，然后运行 EXE。动画生成脚本会在音频开始前留 3.2 秒，并于 8–9.6 秒展开真实应用窗口；更换视频节奏时需同步修改配置。

默认关闭 `AutoReplaceEntrypoints` 和 `ScanAllLocalDrives`。如需桌面入口，请手动创建指向该 EXE 的快捷方式。**固定在任务栏的官方应用图标及运行中的应用按钮不会自动改道**；此 Windows 入口限制同样适用于参考项目。

## 检查

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

测试覆盖配置、画面几何、入口替换和恢复逻辑，不代表已经目视验证每台电脑的视频播放与 DWM 交接。实际运行日志写在 `logs/launcher.log`。

## 项目来源与许可

启动器原项目：[yushua0808-cpu/dragon-codex-boot](https://github.com/yushua0808-cpu/dragon-codex-boot)。代码采用 [MIT 许可证](LICENSE)，第三方说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

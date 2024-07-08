# Edition Manager for Plex <a name="edition-manager-for-plex-zh"></a>
<a href="#edition-manager-for-plex-en">Switch to English</a>

在 Plex 中有两个 “版本” 的概念，一个是 “[Edition](https://support.plex.tv/articles/multiple-editions/)”，一个是 “[Version](https://support.plex.tv/articles/200381043-multi-version-movies/)”，目前他们都被翻译为了 “版本”，似乎也找不到更恰当的词汇来区分这两个概念，但它们的用处却大相径庭。

Edition 的设计初衷是用来区分不同的剪辑版本的，例如院线版、导演剪辑版、加长版、未分级版等。如果你拥有同一部影片的不同剪辑版本，在 Plex 内，你可以通过编辑 Edition 来对它们进行标注和区分，这些不同的版本将会作为独立的项目在媒体库内进行展示，并且拥有独立的观看状态、观看进度和评分记录，互不影响。

Version 的设计初衷是用来整合相同剪辑版本的多个文件版本的，主要是指分辨率、编码格式或动态范围的版本，例如 1080P、4K、SDR、HDR 等。如果你拥有同一部影片的不同文件版本，在匹配成功后它们会在媒体库内自动合并为同一个项目，你可以在观看时通过 “播放版本” 来选择你想要观看的版本（若不选择则会播放默认版本），它们将共享观看状态、观看进度和评分记录。

其中，Edition 会显示在标题的下方，年份的后面，也会在 “更多观看方式/在这些地方观看” 这个部分显示，并且支持自定义显示名称；而 Version 只会在电影的详情页面显示，而且不支持自定义显示名称。由于真正需要标注剪辑版本的使用场景并不多，而 Edition 的显示位置又比较显眼，其实除了用来标注剪辑版本，我们完全可以利用这个功能来对电影的其他信息进行标注。

例如，目前的 Plex 移动端和电视端都不会显示杜比视界（DoVi）这个信息，我们可以通过把动态范围写入 Edition 来实现在移动端和电视端显示杜比视界信息，这样我们就可以区分哪些影片是杜比视界的版本了。再如，Plex 的资料库排序目前仅支持单一排序，你无法在使用标题、观众评分排序的同时显示电影的分辨率或码率等信息，同样我们也可以通过 Edition 来显示这些额外信息。

使用 Edition Manager for Plex（下文简称 EMP）可以自动获取电影和电影文件的信息，并将指定的信息写入 Edition 字段，从而丰富电影信息的展示功能。你可以通过 EMP 将电影的剪辑版本、发行版本、片源版本、分辨率、动态范围、视频编码、帧率、音频编码、比特率、大小、国家、内容分级、评分或时长写入电影的 Edition 字段，而且还支持自选模块和自定义排序。

这一切都将通过 EMP 自动实现，无需编辑或修改文件名。这意味着你不需要在文件名中按照 `{edition-Edition Title}` 这样的格式添加版本信息，EMP 会通过文件名或电影的元数据自动查找相关的信息，然后将需要的信息写入 Edition 字段，对文件的命名没有特殊要求。

你可以通过 EMP 按照自己的需求和喜好为你的电影增加额外的展示信息，我们提供了写入 Edition 和移除 Edition 的功能，你可以随性尝试任何组合方式，也可以随时一键移除所有的 Edition 信息。虽然 Edition 是 Plex Pass 的专属功能，但是通过 EMP，无需 Pass 订阅即可使用 Edition 功能。

## 示例
配置 `order = 剪辑版本；发行版本` 的效果：

![剪辑版本 发行版本](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/6c903e94-8bd1-4b24-bcf7-6a845dd20266)

配置 `order = 评分；国家` 的效果：

![评分 国家](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/82cda04e-db2f-4024-b6e7-1e48bc80d86d)

配置 `order = 帧率；比特率` 的效果：

![帧率 比特率](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/3e81088b-cf4b-44c9-8bae-546b4beeb9a7)

配置 `order = 分辨率；音频编码` 的效果：

![分辨率 音频编码](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/5e2da4cc-66fb-4111-bb33-5bb039497fc5)

配置 `order = 片源版本；动态范围` 的效果：

![片源版本 动态范围](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/2876cef3-9b3a-4cd7-a2d7-761fe1874a7e)

配置 `order = 内容分级；时长` 的效果：

![内容分级 时长](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/5d4c1917-b79c-4ec3-98f9-7e8553aa13f8)

配置 `order = 发行版本；片源版本；分辨率；动态范围；视频编码；帧率；音频编码；比特率；大小；国家` 的效果：

![多模块](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/d58815eb-c943-4b47-8783-ab7a993122f5)

## 模块
目前 EMP 共有 14 个模块可供选择，分别是剪辑版本、发行版本、片源版本、分辨率、动态范围、视频编码、帧率、音频编码、比特率、大小、国家、内容分级、评分和时长，你可以选择任意数量的模块，并按照任意顺序进行排序，若个别模块获取不到信息，其他模块也会正常显示，按照需要选配即可。

### 剪辑版本
剪辑版本模块目前支持 12 种剪辑版本，该模块会优先使用电影的文件名匹配剪辑版本信息，若存在多个视频文件，则会使用文件大小最大的视频文件进行匹配，若找不到剪辑版本信息，则会通过文件内嵌的视频标题进行匹配，若依然找不到剪辑版本信息，则不会写入剪辑版本信息。支持的剪辑版本如下：

- **院线版**：这是在电影院上映的版本，通常是最广为人知的版本。这个版本经过制片人和发行方的最终审核，以便适合大规模公映。
- **导演剪辑版**：这是导演本人认为最能体现他创作意图的版本。这个版本可能包含被删减的镜头或不同的叙事结构，通常在影院上映后发行。
- **制片人剪辑版**：由制片人主导剪辑的版本，通常与导演的意图有所不同。制片人剪辑版有时会为了商业考虑而对影片进行修改。
- **加长版**：包含了在院线版中被删减的场景或扩展了某些片段的版本。加长版通常在影片的家庭影音版中发行，提供更多内容给观众。
- **未分级版**：未经过电影分级机构审核的版本，通常包含更激烈或更有争议的内容。未分级版一般在家庭娱乐市场上发布。
- **最终剪辑版**：这是影片的最终定版，通常包含了所有创作团队的意见。最终剪辑版可能是为了庆祝电影的重要周年纪念而发布的。
- **电视版**：为电视播出而特别剪辑的版本，通常会删除或修改一些不适合电视观众观看的内容，以符合电视台的规定。
- **国际版**：针对国际市场进行调整的版本，可能会添加字幕或配音，并修改一些文化差异较大的内容。
- **家庭录像版**：为家庭观看而发布的版本，包括 VHS、DVD、蓝光等格式。家庭录像版有时会包含院线版没有的额外内容或特别花絮。
- **初剪版**：这是影片在正式剪辑完成前的初步版本，包含了拍摄的所有素材，通常是内部使用的，方便后期修改。
- **工作版**：接近最终版的工作版本，主要用于内部审查或测试放映。工作版可能还未进行最终的音效、配乐和视觉特效处理。
- **粉丝剪辑版**：由影迷基于原片素材重新剪辑的版本，可能会有不同的故事线，可能会删减片段或增加内容，以满足特定粉丝群体的喜好。

### 发行版本
发行版本模块目前支持 14 种发行版本，该模块会优先使用电影的文件名匹配发行版本信息，若存在多个视频文件，则会使用文件大小最大的视频文件进行匹配，若找不到发行版本信息，则会通过文件内嵌的视频标题进行匹配，若匹配到多个发行版本，则会依次写入发行版本信息，若依然找不到发行版本信息，则不会写入发行版本信息。支持的发行版本如下：

- **特别版**：包含了院线版没有的额外内容，如幕后花絮、删减场景、制作特辑等。特别版通常为影迷提供了更多的观看内容。
- **数字修复版**：对老旧影片进行数字修复的版本。此版本通常用于经典影片的再发行，确保影片的视觉和听觉效果达到现代标准。
- **3D 版**：通过 3D 技术处理后的版本，提供立体视觉效果。观众需要佩戴 3D 眼镜观看，以获得沉浸式体验。
- **IMAX 版**：为 IMAX 影院格式优化的版本，具有更好的画质和音效，提供更大、更清晰的屏幕显示和更震撼的观影体验。
- **收藏版**：通常包含豪华包装和独家附加内容，如艺术画册、模型或其他收藏品，针对电影爱好者和收藏家设计。
- **周年纪念版**：为庆祝影片上映的重要周年纪念而发行的特别版本，通常包含额外内容和纪念性附加物品。
- **终极版**：最全面和完整的版本，包含所有可能的附加内容，如导演评论、幕后花絮、删减场景等，提供最丰富的观看体验。
- **蓝光版**：以蓝光光盘格式发行的版本，拥有高画质和高音质，通常包含额外内容和特别花絮。
- **DVD 版**：以 DVD 格式发行的版本，适用于家庭播放设备。DVD 版通常也包含一些额外内容和花絮。
- **限量版**：限量发行的版本，通常具有独特的包装和附加内容，针对特定市场或收藏家设计。
- **纪念版**：为纪念某个特定事件或周年而发行的版本，包含特别设计的包装和纪念性附加内容。
- **豪华版**：包含了丰富的附加内容和豪华包装，通常提供比标准版更多的特辑和幕后花絮。
- **导演签名版**：导演亲自签名和认可的版本，通常包含导演的独家评论和特别花絮，具有较高的收藏价值。
- **标准收藏版**：由 Criterion Collection 发行的版本，专注于高品质的电影修复和特别附加内容，以电影爱好者和收藏家为目标受众。

### 片源版本
片源版本模块目前支持 25 种片源版本，该模块会优先使用电影的文件名匹配片源版本信息，若存在多个视频文件，则会使用文件大小最大的视频文件进行匹配，若找不到片源版本信息，则会通过文件内嵌的视频标题进行匹配，若依然找不到片源版本信息，则不会写入片源版本信息。支持的片源版本如下：

- **REMUX**：从蓝光光盘中提取的无损版本，没有经过压缩处理，保持了原始的画质和音质。
- **BD**：从蓝光光盘中提取的版本，经过了一些压缩处理，但画质和音质都非常好。
- **BDRIP**：从蓝光光盘压缩而来的版本，体积较小，质量比蓝光版稍差。
- **WEB-DL**：从网络流媒体服务下载的版本，画质和音质较好。
- **VODRIP**：从视频点播服务录制的版本，画质和音质较好，接近 WEB-DL。
- **WEBRIP**：从网络流媒体服务录制的版本，画质和音质不及 WEB-DL。
- **HDRIP**：从高清来源提取后压缩而来的版本，画质和音质较好。
- **HR-HDTV**：高分辨率的 HDTV 版本，经过了一些压缩处理，质量优于普通的 HDTV。
- **HDTV**：从电视广播录制的高清版本，画质较好，但可能包含电视台的水印和广告。
- **PDTV**：从数字电视录制的版本，质量比 SDTV 好，接近 HDTV。
- **DVD**：从 DVD 光盘中提取的版本，画质和音质较好。
- **DVDRIP**：从 DVD 光盘压缩而来的版本，画质和音质不及 DVD。
- **DVDSCR**：发行给奖项评审或影评人的版本，画质和音质相对较好，但可能包含水印和版权信息。
- **R5**：俄罗斯发行的 DVD 版本，画质较好，但音质可能略差。
- **LDRIP**：从激光光盘中提取的版本，画质和音质较好，但略低于 DVD。
- **PPVRIP**：从付费点播服务录制的版本，质量一般不错。
- **SDTV**：从标清电视录制的版本，分辨率较低，质量适中。
- **TVRIP**：从电视广播录制的版本，质量一般，可能包含电视台的水印和广告。
- **VHSRIP**：从 VHS 录影带中提取的版本，画质和音质略差。
- **HDTC**：从电影院胶片转录而来的高清版本，可能包含电影院现场的背景噪音。
- **TC**：从电影院胶片转录而来的标清版本，画质和音质相对较差。
- **HDCAM**：使用高清摄像设备在电影院内录制的版本，质量介于 HDTC 和普通 CAM 之间。
- **HQCAM**：使用高清摄像设备在电影院内录制的版本，画质和音质较差。
- **TS**：使用专业摄像设备在电影院内录制的版本，音质相对较好，但画质较差。
- **CAM**：使用普通摄像设备在电影院内录制的版本，画质和音质很差。

### 分辨率
分辨率模块支持 Plex 可识别的所有分辨率，该模块会从电影元数据的媒体信息中获取视频文件的分辨率信息，若存在多个视频文件，则会获取文件大小最大的视频文件的分辨率信息，若找不到分辨率信息，则不会写入分辨率信息。支持的分辨率包括但不限于：

- **8K**：包括 7680 x 4320（8K UHD）和 8192 x 4320（8K DCI）等。
- **4K**：包括 3840 x 2160（4K UHD）、3996 x 2160、4096 x 1716 和 4096 x 2160（4K DCI）等。
- **2.7K**：包括 2704 x 1520 和 3440 x 1440 等。
- **2K**：包括 1998 x 1080、2048 x 858 和 2048 x 1080（2K DCI）等。
- **1080P**：包括 1920 x 800、1920 x 818、1920 x 1034 和 1920 x 1080（FHD）等。
- **720P**：包括 1280 x 540、1280 x 640、1280 x 692 和 1280 x 720（HD）等。
- **576P**：包括 720 x 576（PAL）、768 x 576、960 x 576 和 1024 x 576 等。
- **480P**：包括 640 x 480（NTSC）、848 x 480 和 854 x 480 等。
- **SD**：包括 480P 以下的分辨率，如 360 x 240、426 x 240、480 x 360 和 640 x 360 等。

### 动态范围
动态范围模块支持 Plex 可识别的所有动态范围，该模块会从电影元数据的媒体信息中获取视频文件的动态范围信息，若存在多个视频文件，则会获取文件大小最大的视频文件的动态范围信息，若找不到动态范围信息，则不会写入动态范围信息。支持的动态范围包括但不限于：

- **DV P8**：杜比视界 P8 为流媒体提供高效色彩编码，与 HDR10 兼容，确保广泛设备支持，但色彩表现不及 P5。
- **DV P7**：杜比视界 P7 是专为蓝光原盘设计的双层格式，提供卓越的色彩深度和细节，但需要播放硬件支持。
- **DV P5**：杜比视界 P5 是针对流媒体的单层格式，色彩编码优于 P8，最适合展示杜比视界原生内容的细腻色彩。
- **HDR**：高动态范围扩展了显示设备的亮度和颜色范围，使图像更加丰富和真实，提升了观影的沉浸感。
- **SDR**：标准动态范围是传统视频格式，虽然亮度和颜色范围有限，但因其高兼容性而广泛应用于各种设备。

注：HDR10、HDR10+、HLG 等高动态范围技术都将被视作 HDR。若视频文件同时支持 HDR 和 DV，那么它们都会被写入版本信息。

### 视频编码
视频编码模块支持 Plex 可识别的所有视频编码，该模块会从电影元数据的媒体信息中获取视频文件的视频编码信息，若存在多个视频文件，则会获取文件大小最大的视频文件的视频编码信息，若找不到视频编码信息，则不会写入视频编码信息。支持的视频编码包括但不限于：

- **AV1**：全称 AOMedia Video 1，由开放媒体联盟开发的开源编码格式，具有极高的压缩效率和优秀的视频质量。
- **HEVC**：也叫 H.265，高效视频编码，提供较高的压缩效率和良好的视频质量。
- **VP9**：由 Google 开发的开源编码格式，压缩效率高，多用于 YouTube 等网络视频平台。
- **H264**：也叫 H.264 或 AVC，常见的高清视频编码格式，压缩效率较高，广泛应用于流媒体和视频存储。
- **VC1**：也叫 SMPTE 421M，微软开发的视频编码格式，压缩效率较好，多用于蓝光光盘和网络视频。
- **MPEG4**：全称 MPEG-4 Part 2，广泛应用于视频流和光盘的视频编码格式，压缩效率较好。
- **SVQ3**：全称 Sorenson Video 3，早期的视频压缩格式，压缩效率较低。
- **WMV3**：也叫 Windows Media Video 9，微软的视频编码格式，压缩效率一般。
- **WMV2**：也叫 Windows Media Video 8，较早期的微软视频编码格式，压缩效率较低。
- **WMV1**：也叫 Windows Media Video 7，最早期的微软视频编码格式，压缩效率较低。
- **MPEG2**：也叫 H.262，标准的 DVD 和部分电视广播的视频编码格式，压缩效率较低。
- **MPEG1**：早期的视频压缩格式，多用于 VCD，压缩效率很低。
- **RV40**：全称 RealVideo 4.0，RealNetworks 开发的编码格式，压缩效率较低。

### 帧率
帧率模块支持 Plex 可识别的所有帧率，该模块会从电影元数据的媒体信息中获取视频文件的帧率信息，若存在多个视频文件，则会获取文件大小最大的视频文件的帧率信息，若找不到帧率信息，则不会写入帧率信息。支持的帧率包括但不限于：

- **240P**：每秒显示 240 帧画面，用于超级慢动作视频拍摄，捕捉快速运动的细节。
- **120P**：每秒显示 120 帧画面，用于高帧率视频拍摄和播放，常见于高端电视和虚拟现实内容，提供极为流畅的视觉体验。
- **100P**：每秒显示 100 帧画面，主要用于某些高帧率的电视广播。
- **72P**：每秒显示 72 帧画面，虽不常见，但可用于某些特殊的电影放映。
- **60P**：每秒显示 60 帧画面，常用于高速运动视频、体育赛事和视频游戏，提供极其流畅的运动表现。
- **50P**：每秒显示 50 帧画面，多用于欧洲的高清电视标准以及一些高帧率的视频内容。
- **48P**：每秒显示 48 帧画面，曾用于部分电影，如《霍比特人》系列，提供比 24 帧更流畅的画面。
- **30P**：每秒显示 30 帧画面，适用于 NTSC 制式的视频标准，广泛应用于北美和日本的电视广播。
- **25P**：每秒显示 25 帧画面，适用于 PAL 制式的视频标准，主要用于欧洲、中国、澳大利亚和其他采用 PAL 制式的地区的电视和视频内容。
- **24P**：每秒显示 24 帧画面，传统的电影帧率，常用于电影制作，带来独特的电影质感。
- **15P**：每秒显示 15 帧画面，多用于低带宽的视频流和某些网络摄像头。
- **12P**：每秒显示 12 帧画面，曾用于早期的动画和低带宽的视频传输。
- **10P**：每秒显示 10 帧画面，主要用于非常低带宽的视频传输和某些监控摄像头。
- **5P**：每秒显示 5 帧画面，用于极低带宽的监控和视频传输。

### 音频编码
音频编码模块支持 Plex 可识别的所有音频编码，该模块会从电影元数据的媒体信息中获取视频文件的音频编码信息，若存在多个视频文件，则会获取文件大小最大的视频文件的音频编码信息，若存在多个音频流，则会获取比特率最高的音频流的音频编码信息（多声道优先），若找不到音频编码信息，则不会写入音频编码信息。支持的音频编码包括但不限于：

- **DTS-HD MA**：全称 DTS-HD Master Audio，是无损编码，提供电影院级的音质，常用于蓝光光盘。
- **TRUEHD**：全称 Dolby TrueHD，是杜比无损编码，提供高保真音质，也常用于蓝光光盘。
- **FLAC**：全称 Free Lossless Audio Codec，是开源无损编码，广泛用于音乐存档和高保真音轨。
- **PCM**：全称 Pulse Code Modulation，是无损编码，提供原始音质，常用于 CD 和 DVD。
- **DTS-HD HRA**：全称 DTS-HD High Resolution Audio，是高分辨率音频，有损编码，音质优于标准 DTS。
- **DTS-ES**：全称 DTS Extended Surround，是扩展环绕声，为 DTS 的扩展版本，增加了一个后置中央声道。
- **EAC3**：全称 Enhanced AC-3，也叫 Dolby Digital Plus，杜比数字的加强版，提供更高的压缩比和更好的音质。
- **DTS**：全称 Digital Theater Systems，数字影院系统编码，广泛用于电影和 DVD。
- **AC3**：也叫 Dolby Digital，杜比数字编码，常用于 DVD 和数字电视广播。
- **HE-AAC**：全称 High-Efficiency Advanced Audio Codec，高效率高级音频编码，相比 AAC 提供了更高的数据压缩率。
- **AAC**：全称 Advanced Audio Codec，高级音频编码，是 MP3 的继任者，广泛用于流媒体。
- **MP3**：全称 MPEG-1 Audio Layer 3，是最常见的有损音频编码，广泛用于音乐播放。
- **VORBIS**：全称 Ogg Vorbis，是开源有损编码，常用于游戏和网络音频。
- **WMAPRO**：全称 Windows Media Audio Professional，是微软开发的有损编码，提供较高音质。
- **COOK**：全称 RealAudio COOK，是 RealNetworks 开发的有损编码，主要用于早期的流媒体。
- **MP2**：全称 MPEG-1 Audio Layer 2，是早期的有损编码，常用于广播和 VCD。
- **WMAV2**：全称 Windows Media Audio Version 2，是 WMA 的一个变体，提供较高的音频压缩率和较低的音质。
- **WMA**：全称 Windows Media Audio，是微软开发的有损编码，广泛用于 Windows 平台。

注：在写入版本信息时，音频编码后方会显示对应音频流的声道信息，如 TRUEHD 7.1、AC3 5.1、AAC 立体声等等。

### 比特率
比特率模块会从电影元数据的媒体信息中获取视频文件的比特率（码率）信息，若存在多个视频文件，则会获取文件大小最大的视频文件的比特率信息，若找不到比特率信息，则不会写入比特率信息（比特率的单位为 Kbps、Mbps）。

### 大小
大小模块会从电影元数据的媒体信息中获取视频文件的（文件）大小信息，若存在多个视频文件，则会获取文件大小最大的视频文件的大小信息（大小的单位为 B、KB、MB、GB）。

### 国家
国家模块会从电影元数据中获取电影的（制片）国家（或地区）信息，若存在多个国家，则会依次写入国家信息，若找不到国家信息，则不会写入国家信息。

### 内容分级
内容分级模块会从电影元数据中获取电影的内容分级信息，若找不到内容分级信息，则不会写入内容分级信息。支持的内容分级包括但不限于：

#### 电影分级（MPAA）
- **G**：全称 General Audiences，适合所有年龄段观众，不包含任何不适合儿童观看的内容。
- **PG**：全称 Parental Guidance Suggested，建议家长给予指导，可能包含一些不适合儿童的内容。
- **PG-13**：也叫 Parents Strongly Cautioned，强烈建议家长给予指导，部分内容可能不适合 13 岁以下的儿童。
- **R**：全称 Restricted，17 岁以下观众需由家长或成年监护人陪同观看，包含激烈的语言、暴力或性内容。
- **NC-17**：也叫 Adults Only，仅限 17 岁及以上观众观看，包含非常明确的暴力或性内容。
- **NR**：全称 Not Rated，影片未经过 MPAA 的审查和评级。
- **Unrated**：未经官方评级机构如 MPAA 评级的版本，可能包含原始评级版本中删减的内容。

#### 电视节目分级（TV Parental Guidelines）
- **TV-Y**：全称 Television for All Children，适合所有儿童观看，通常适合 2-6 岁的儿童。
- **TV-Y7**：全称 Television for Children 7 and Above，适合 7 岁及以上儿童观看，可能包含轻微暴力或复杂的情节。
- **TV-Y7-FV**：全称 Television for Children 7 and Above - Fantasy Violence，适合 7 岁及以上儿童观看，包含幻想暴力元素。
- **TV-G**：全称 Television General Audience，适合所有年龄段观众，节目中不包含任何不适合儿童观看的内容。
- **TV-PG**：全称 Television Parental Guidance Suggested，建议家长给予指导，可能包含一些不适合儿童的内容。
- **TV-14**：全称 Television Parents Strongly Cautioned，强烈建议家长给予指导，部分内容可能不适合 14 岁以下的儿童。
- **TV-MA**：全称 Television Mature Audience Only，仅限成年观众观看，可能包含激烈的语言、暴力或性内容。

#### 其他分级标准
- **Approved**：电影获得电影协会的认可，适合公众观看，具体内容依据发行年代不同而有所变化。
- **18+**：仅限 18 岁及以上观众观看，内容非常成人化。
- **AO**：全称 Adults Only，用于视频游戏的评级，仅限成人观看。

注：上述分级为美国的分级制度说明，其它地区的分级制度可能存在差异，以实际情况为准。由于中国大陆地区没有内容分级制度，建议将 “认证国家/地区” 设置为 “美国”，以获取内容分级信息。

### 评分
评分模块会从电影元数据中获取电影的（观众）评分信息（使用资料库设置的评分来源），若找不到评分信息，则不会写入评分信息（评分将转换为十分制）。

### 时长
时长模块会从电影元数据的媒体信息中获取视频文件的时长信息，若存在多个视频文件，则会获取文件大小最大的视频文件的时长信息，若找不到时长信息，则不会写入时长信息（时长的单位为分钟）。

## 功能
EMP 共有 `为所有电影添加版本信息（all）`、`为新增电影添加版本信息（new）` 和 `为所有电影重置版本信息（reset）` 三种运行模式：

- 为所有电影添加版本信息：根据用户配置，在排除掉需要跳过的资料库后为其余库中的所有电影添加版本信息，已经存在版本信息的电影会被跳过。
- 为新增电影添加版本信息：通过 Webhooks 功能监听服务器事件，实时获取新增项目的元数据，根据用户配置，仅为新增电影（不含需要跳过的资料库中的新增电影）添加版本信息。
- 为所有电影重置版本信息：根据用户配置，在排除掉需要跳过的资料库后为其余库中的所有电影重置（移除）版本信息。

注：`为新增电影添加版本信息` 模式需要服务器的管理员账号订阅了 Plex Pass 才能使用。

## 配置说明
在使用 EMP 前，请先参考以下提示（示例）对 `/config/config.ini` 进行配置。
```
[server]
# Plex 服务器的地址，格式为 http://服务器 IP 地址:32400 或 http(s)://域名:端口号
address = http://127.0.0.1:32400
# Plex 服务器的 token，用于身份验证
token = xxxxxxxxxxxxxxxxxxxx
# 指定需要跳过的资料库，格式为库名1；库名2；库名3，若没有需要跳过的资料库，可以留空
skip_libraries = 云电影；演唱会
# 语言设置，zh 代表中文，en 代表英文
language = zh

[modules]
# 指定需要写入的模块及其排序，格式为模块1；模块2；模块3，可选模块包括剪辑版本、发行版本、片源版本、分辨率、动态范围、视频编码、帧率、音频编码、比特率、大小、国家、内容分级、评分、时长
order = 片源版本；动态范围
```
由于 EMP 只会对电影类型的资料库进行处理，所以在指定需要跳过的资料库时，指定需要跳过的电影类型的资料库即可。写入版本信息的模块没有数量限制，可以根据需要自行选配。

在 `为新增电影添加版本信息` 模式下运行时，EMP 会使用 Flask 创建一个 Web 服务器，通过监听 `8089` 端口来接收 Plex 服务器发送的 `library.new` 事件，从而获取新增项目的信息并对其进行处理。

假如你的 `8089` 端口已经被其他服务占用，你可能需要通过修改 `edition-manager-for-plex.py` 倒数第九行的 `port=8089`（通过 Python 脚本运行时）或者通过修改端口映射（通过 Docker 容器运行时）来更换监听端口。

## 运行方式
你可以通过 Docker 容器或者 Python 脚本来运行 EMP，推荐使用 Docker 容器运行，具体使用方法可参考下文。

### 通过 Docker 容器运行

#### 运行条件
- 安装了 Docker 和 Docker Compose。

#### Docker Compose
- edition-manager-for-plex（Plex Pass 订阅用户）
  
   ```
   version: "2"
   services:
     emp-all:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-all
       command: python edition-manager-for-plex.py --all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /自定义目录/edition-manager-for-plex/config:/app/config
     emp-new:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-new
       command: python edition-manager-for-plex.py --new
       ports:
         - 8089:8089
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /自定义目录/edition-manager-for-plex/config:/app/config
       restart: unless-stopped
   networks: {}
   ```
- edition-manager-for-plex（非 Plex Pass 订阅用户）
  
   ```
   version: "2"
   services:
     emp-scheduler:
       image: mcuadros/ofelia:latest
       container_name: emp-scheduler
       depends_on:
         - emp-all
       command: daemon --docker -f label=com.docker.compose.project=${COMPOSE_PROJECT_NAME}
       labels:
         ofelia.job-run.emp-all.schedule: 0 30 22 * * *
         ofelia.job-run.emp-all.container: emp-all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
       restart: unless-stopped
     emp-all:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-all
       command: python edition-manager-for-plex.py --all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /自定义目录/edition-manager-for-plex/config:/app/config
   networks: {}
   ```
- edition-manager-for-plex-reset
  
   ```
   version: "2"
   services:
     emp-reset:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-reset
       command: python edition-manager-for-plex.py --reset
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /自定义目录/edition-manager-for-plex/config:/app/config
   networks: {}
   ```

#### 使用方法
使用 EMP 可以写入版本信息，也可以移除版本信息。由于 Docker 会在启动堆栈时自动启动堆栈内的所有容器，所以写入和移除的功能需要分开部署。请先部署 `edition-manager-for-plex` 用于写入版本信息，然后在有需要时部署 `edition-manager-for-plex-reset` 用于移除版本信息（部署后会立刻执行一次 `为所有电影重置版本信息`。你也可以使用 `docker-compose up --no-start` 来部署这个容器，这样部署后不会立刻运行，在有需要时再启动容器即可）。

- edition-manager-for-plex

  1. 在 Plex 服务器的设置选项中找到 `Webhooks`，点击 `添加 Webhook`，填写你的 Flask 服务器地址 `http://Docker 所在设备的 IP 地址:8089` 并 `保存修改`。（非 Plex Pass 订阅用户无需填写）
  2. 下载仓库中的 `/compose/edition-manager-for-plex/compose.yaml` 文件（Plex Pass 订阅用户可删除 `emp-scheduler` 的部分，非 Plex Pass 订阅用户可删除 `emp-new` 的部分），将其保存在一个名为 `edition-manager-for-plex` 的文件夹内。
  3. 用记事本或文本编辑打开 `compose.yaml`，将 `/自定义目录/edition-manager-for-plex/config` 替换为宿主机上的一个目录，这个目录将用于保存配置文件。（`emp-all` 与 `emp-new` 使用相同的目录即可）
  4. 打开终端或命令行工具，使用 `cd` 命令切换到 `compose.yaml` 所在的目录。
  5. 使用命令 `docker-compose up -d` 部署并启动 edition-manager-for-plex 堆栈。
  6. 用记事本或文本编辑打开 `/自定义目录/edition-manager-for-plex/config/config.ini` 文件，填写你的 Plex 服务器地址（`address`）和 [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)（`token`），设置需要写入版本信息的模块及其排序（`order`），按照需要选填其他配置选项。
  7. 重启 edition-manager-for-plex 堆栈即可正常运行。

- edition-manager-for-plex-reset

  1. 下载仓库中的 `/compose/edition-manager-for-plex-reset/compose.yaml` 文件，将其保存在一个名为 `edition-manager-for-plex-reset` 的文件夹内。
  2. 用记事本或文本编辑打开 `compose.yaml`，将 `/自定义目录/edition-manager-for-plex/config` 替换为宿主机上的一个目录，这个目录将用于保存配置文件。（与 `emp-all` 和 `emp-new` 使用相同的目录即可）
  3. 打开终端或命令行工具，使用 `cd` 命令切换到 `compose.yaml` 所在的目录。
  4. 使用命令 `docker-compose up -d` 部署并启动 edition-manager-for-plex-reset 堆栈。（若 `/自定义目录/edition-manager-for-plex/config/config.ini` 文件已经正确配置，堆栈会正常运行；若未配置，请先填写配置信息，然后重启堆栈，即可正常运行）

#### 运行说明
EMP 共有 `emp-all`、`emp-new`、`emp-scheduler` 和 `emp-reset` 四个容器，分别用于处理不同的任务。启动堆栈后，这四个容器的运行状态也略有差异。

- 容器 `emp-all` 是用来运行 `为所有电影添加版本信息` 任务的，它会在启动后运行一次 `为所有电影添加版本信息` 任务，对设置范围内的所有电影进行处理（添加版本信息），并在终端或日志内显示资料库的信息和处理结果，处理完毕后会停止运行。你可以随时启动它来运行 `为所有电影添加版本信息` 任务，它将在每次处理完毕后停止运行。如果你配置了 `emp-scheduler`，`emp-all` 也会在每次到达你设置的任务时间时自动运行一次。
- 容器 `emp-new` 是用来运行 `为新增电影添加版本信息` 任务的，它会在启动后创建一个 Flask 服务器来监听 Plex 服务器的事件，当 Plex 服务器上有新增电影时，它将自动对新增电影进行处理（添加版本信息），并在终端或日志内显示处理结果，处理完毕后会继续监听 Plex 服务器的事件，并在每次有新增电影时对其进行处理，然后继续监听。
- 容器 `emp-scheduler` 是用来给 `为所有电影添加版本信息` 设置/触发计划任务的，它会在启动后创建一个定时运行 `emp-all` 的计划任务，默认设置为 `0 30 22 * * *`，表示每天晚上 10 点半（22:30）运行一次。你可以通过修改时间表达式来自定义运行频率，例如 `"@every 3h"` 表示每 3 小时运行一次，`"@every 30m"` 表示每 30 分钟运行一次等。它将在设置的任务时间启动 `emp-all` 容器，并在终端或日志内同步显示 `emp-all` 的日志信息，然后继续运行。
- 容器 `emp-reset` 是用来运行 `为所有电影重置版本信息` 任务的，它会在启动后运行一次 `为所有电影重置版本信息` 任务，对设置范围内的所有电影进行处理（重置/移除版本信息），并在终端或日志内显示资料库的信息和处理结果，处理完毕后会停止运行。你可以随时启动它来运行 `为所有电影重置版本信息` 任务，它将在每次处理完毕后停止运行。

你可以根据需要选配这四个容器，若存在不需要的功能，直接在 Compose 中删除对应的部分再部署即可。

### 通过 Python 脚本运行

#### 运行条件
- 安装了 Python 3.0 或更高版本。
- 使用命令 `pip3 install -r requirements.txt` 安装了必要的第三方库。

#### 使用方法
1. 通过 [Releases](https://github.com/x1ao4/edition-manager-for-plex/releases) 下载最新版本的压缩包并解压到本地目录中。
2. 用记事本或文本编辑打开目录中的 `/config/config.ini` 文件，填写你的 Plex 服务器地址（`address`）和 [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)（`token`），设置需要写入版本信息的模块及其排序（`order`），按照需要选填其他配置选项。
3. 在 Plex 服务器的设置选项中找到 `Webhooks`，点击 `添加 Webhook`，填写你的 Flask 服务器地址 `http://脚本所在设备的 IP 地址:8089` 并 `保存修改`。（非 Plex Pass 订阅用户无需填写）
4. 打开终端或命令行工具，使用 `cd` 命令切换到脚本所在的目录。
5. 使用命令 `python3 edition-manager-for-plex.py --all` 可运行 `为所有电影添加版本信息` 任务，脚本将对设置范围内的所有电影进行处理（添加版本信息），并在控制台显示资料库的信息和处理结果，处理完毕后会结束运行。
6. 使用命令 `python3 edition-manager-for-plex.py --new` 可运行 `为新增电影添加版本信息` 任务，脚本将创建一个 Flask 服务器来监听 Plex 服务器的事件，当 Plex 服务器上有新增电影时，脚本将自动对新增电影进行处理（添加版本信息），并在控制台显示处理结果，处理完毕后会继续监听 Plex 服务器的事件，并在每次有新增电影时对其进行处理，然后继续监听。
7. 使用命令 `python3 edition-manager-for-plex.py --reset` 可运行 `为所有电影重置版本信息` 任务，脚本将对设置范围内的所有电影进行处理（重置/移除版本信息），并在控制台显示资料库的信息和处理结果，处理完毕后会结束运行。

#### 快速启动
PC 用户也可以通过提供的快速启动脚本来执行任务：

- 双击 `emp-all.bat (Win)` 或 `emp-all.command (Mac)` 脚本快速启动 `为所有电影添加版本信息` 任务。
- 双击 `emp-new.bat (Win)` 或 `emp-new.command (Mac)` 脚本快速启动 `为新增电影添加版本信息` 任务。
- 双击 `emp-reset.bat (Win)` 或 `emp-reset.command (Mac)` 脚本快速启动 `为所有电影重置版本信息` 任务。

#### 自动运行
为了便于使用，你也可以通过 crontab 或其他任务工具，为 EMP 添加定时或开机任务，实现自动运行。

- 为所有电影添加版本信息（Mac）
  
  1. 在终端使用命令 `crontab -e` 打开 crontab 文件。
  2. 按 `i` 进入插入模式，添加行 `30 22 * * * /path/to/emp-all.command > /dev/null 2>&1`。（请把 `/path/to/emp-all.command` 替换为脚本的实际路径）
  3. 按 `Esc` 退出插入模式，输入 `:wq`，按 `Enter` 保存更改并退出编辑器。

  这样就为 `为所有电影添加版本信息` 添加了一个每天晚上 10 点半（22:30）运行一次的定时任务。你可以通过修改时间表达式来自定义运行频率，例如 `0 */3 * * *` 表示每 3 小时运行一次，`*/30 * * * *` 表示每 30 分钟运行一次等。（脚本将在后台运行）

- 为新增电影添加版本信息（Mac）
  
  1. 用文本编辑打开 `emp-new.command` 文件，在第二行输入 `sleep 10` 保存更改并关闭文件。
  2. 在终端使用命令 `crontab -e` 打开 crontab 文件。
  3. 按 `i` 进入插入模式，添加行 `@reboot /path/to/emp-new.command`。（请把 `/path/to/emp-new.command` 替换为脚本的实际路径）
  4. 按 `Esc` 退出插入模式，输入 `:wq`，按 `Enter` 保存更改并退出编辑器。

  这样我们就将 `为新增电影添加版本信息` 设置为了 Mac 的开机启动任务，任务会在开机 10 秒后运行，延迟 10 秒是为了保证 Plex 服务器比脚本先启动，否则脚本将无法连接到 Plex 服务器。（脚本将在后台运行）

- 为所有电影添加版本信息（Nas）
  
  通过自带的任务计划功能为 `为所有电影添加版本信息` 添加定时任务（计划的任务）。添加任务后在 `任务设置 - 运行命令 - 用户自定义脚本` 中输入 `python3 /path/to/edition-manager-for-plex.py --all`，然后按需要设置运行时间即可。（请把 `/path/to/edition-manager-for-plex.py` 替换为脚本的实际路径）
  
- 为新增电影添加版本信息（Nas）
  
  通过自带的任务计划功能将 `为新增电影添加版本信息` 设置为开机启动任务（触发的任务）。添加任务后在 `任务设置 - 运行命令 - 用户自定义脚本` 中输入 `sleep 10 && python3 /path/to/edition-manager-for-plex.py --new`，这样脚本会在 Nas 启动 10 秒后再运行，延迟 10 秒是为了保证 Plex 服务器比脚本先启动，否则脚本将无法连接到 Plex 服务器。（请把 `/path/to/edition-manager-for-plex.py` 替换为脚本的实际路径）

若设置为定时或开机任务后脚本运行失败，你可能需要将 command 脚本或用户自定义脚本中的 `python3` 替换为 `python3` 的实际路径。你可以在 Mac 终端或 Nas 的 SSH 内通过命令 `which python3` 找到 `python3` 的实际路径。

## 注意事项
- 请确保你提供了正确的 Plex 服务器地址和正确的 X-Plex-Token。
- 请确保你提供了正确的库名，并按要求进行了填写。
- 请确保你按照要求设置了正确的语言和模块信息。
- 如果无法连接到 Plex 服务器，请检查你的网络连接，并确保服务器可以访问。如果你是通过 Docker 容器运行的，也可以尝试使用 `host` 模式重新部署容器运行。
- 请使用服务器管理员账号的 X-Plex-Token，以确保你拥有足够的权限进行操作。
- 版本信息将在添加后被锁定，若有修改需求，Plex Pass 订阅用户可以手动解锁版本信息，然后进行修改；非 Plex Pass 订阅用户不支持手动修改版本信息。若要为所有电影修改版本信息的模块或排序，请先重置版本信息，然后修改配置文件，再重新写入版本信息。
- 修改配置文件后，需要重启容器，新的配置信息才会生效。
- Windows 用户运行 Python 脚本后，若没有任何反应，请将运行命令或启动脚本中的 `python3` 替换为 `python` 再运行。
- 如需使用 `为新增电影添加版本信息` 模式，请确保你在服务器的 `设置 - 网络` 中勾选了 `Webhooks` 选项。

## 赞赏
如果你觉得这个项目对你有用，可以请我喝杯咖啡。如果你喜欢这个项目，可以给我一个⭐️。谢谢你的支持！

<img width="399" alt="赞赏" src="https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/b9e79a88-f2af-4c3a-8278-479454c6393a">
<br><br>
<a href="#edition-manager-for-plex-zh">回到顶部</a>
<br>
<br>
<br>

# Edition Manager for Plex <a name="edition-manager-for-plex-en"></a>
<a href="#edition-manager-for-plex-zh">切换至中文</a>

In Plex, there are two concepts of "version": "[Edition](https://support.plex.tv/articles/multiple-editions/)" and "[Version](https://support.plex.tv/articles/200381043-multi-version-movies/)", but their uses are quite different.

The primary design of Edition is to differentiate between various cut versions of a film, such as Theatrical Cut, Director's Cut, Extended Cut, Unrated Cut, etc. If you have different cut versions of the same movie, you can label and distinguish them by editing the Edition in Plex. These different versions will be displayed as separate entries in the media library, each with its own viewing status, progress, and rating records, independent of each other.

The primary design of Version is to integrate multiple file versions of the same cut, mainly referring to different resolutions, encoding formats, or dynamic ranges, such as 1080P, 4K, SDR, HDR, etc. If you have different file versions of the same movie, they will automatically merge into a single entry in the media library after successful matching. You can choose which version to watch through "Play Version" during playback (if not selected, the default version will be played). They will share the same viewing status, progress, and rating records.

The Edition is displayed below the title, after the year, and also in the "More Ways to Watch/Watch From These Locations" section, and it supports custom display names. In contrast, the Version is only shown on the movie's detail page and does not support custom display names. Since the actual use cases for marking different cut versions are not frequent and the Edition's display position is quite prominent, we can fully utilize this feature to mark other information about the movie beyond just different cuts.

For instance, currently, Plex's mobile and TV apps do not display Dolby Vision information. We can achieve this by writing the dynamic range into the Edition, allowing Dolby Vision information to be displayed on mobile and TV apps. This way, we can distinguish which movies are Dolby Vision versions. Additionally, Plex's library sorting currently only supports single sorting criteria. You cannot display the movie's resolution or bitrate information while sorting by title or audience rating. Similarly, we can display this extra information through Edition.

Using Edition Manager for Plex (hereinafter referred to as EMP), you can automatically retrieve information about movies and movie files and write the specified information into the Edition field, enriching the display functionality of movie information. With EMP, you can write the movie's Cut Version, Release Version, Source Version, Resolution, Dynamic Range, Video Codec, Frame Rate, Audio Codec, Bitrate, Size, Country, Content Rating, Audience Rating, or Duration into the Edition field. It also supports custom modules and custom sorting. 

All of this will be automatically handled by EMP, without the need to edit or modify filenames. This means you don't need to add Edition information to the filename in the format `{edition-Edition Title}`. EMP will automatically search for relevant information through filenames or the movie's metadata, and then write the required details into the Edition field. There are no specific requirements for naming files.

You can use EMP to add extra display information to your movies according to your needs and preferences. We provide features for writing and removing Editions, allowing you to try any combination freely and remove all Edition information with one click at any time. Although Edition is an exclusive feature for Plex Pass, EMP allows you to use the Edition feature without a Pass subscription.

## Examples
Configuration `order = Cut;Release` looks like this:

![Cut Release](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/28047dfe-a058-4cf3-8a32-ca8882edae15)

Configuration `order = Rating;Country` looks like this:

![Rating Country](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/05214007-f2ed-423e-82a3-188712933446)

Configuration `order = FrameRate;Bitrate` looks like this:

![FrameRate Bitrate](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/b843c042-b9cb-43d8-92c0-8d74c7847ffa)

Configuration `order = Resolution;AudioCodec` looks like this:

![Resolution AudioCodec](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/97606ea4-e5e0-45e4-8633-08f77181ef96)

Configuration `order = Source;DynamicRange` looks like this:

![Source DynamicRange](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/a0d845cd-39e8-45b1-bb4f-3950c51b65e1)

Configuration `order = ContentRating;Duration` looks like this:

![ContentRating Duration](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/15805123-de56-4e68-871a-cccd6bf09f9d)

Configuration `order = Release;Source;Resolution;DynamicRange;VideoCodec;FrameRate;AudioCodec;Bitrate;Size;Country` looks like this:

![Multi-module](https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/11ca5070-1757-4790-a896-5da97ce976a9)

## Modules
Currently, EMP offers a total of 14 modules for selection. These include Cut, Release, Source, Resolution, DynamicRange, VideoCodec, FrameRate, AudioCodec, Bitrate, Size, Country, ContentRating, Rating, and Duration. You can choose any number of modules and arrange them in any order. If certain modules cannot retrieve information, the others will still display correctly. Customize as needed.

### Cut
The Cut module currently supports 13 types of cut versions. This module prioritizes matching cut version information based on the movie's filename. If multiple video files exist, it will use the largest file by size for matching. If cut version information cannot be found through filename, it will attempt to match using embedded video titles within the file. If cut version information still cannot be found, it will not write cut version information. The supported cut versions are:

- **Theatrical Cut**: This version is shown in theaters and is typically the most widely recognized version. It undergoes final review by producers and distributors for large-scale release.
- **Director's Cut**: This version is considered by the director to best reflect their creative intent. It may include deleted scenes or have a different narrative structure, often released after the theatrical run.
- **Producer's Cut**: Edited under the supervision of producers, this version may differ from the director's intent. Producer's cuts sometimes modify the film for commercial reasons.
- **Extended Cut**: Includes scenes cut from the theatrical release or extends certain segments. Extended editions are usually released in home video formats to provide more content to viewers.
- **Unrated Cut**: A version not reviewed by film rating boards, often containing more intense or controversial content. Unrated versions are generally released in the home entertainment market.
- **Final Cut**: This is the definitive version of the film, incorporating input from all creative teams. Final cuts may be released to commemorate important anniversaries of the film.
- **Television Cut**: Specifically edited for television broadcast, often removing or modifying content unsuitable for television audiences to comply with broadcasting standards.
- **International Cut**: Adjusted for international markets, which may include subtitles or dubbing, and modifications to address significant cultural differences.
- **Home Video Cut**: Released for home viewing, including formats like VHS, DVD, Blu-ray, etc. Home video versions may include additional content or special features not present in theatrical releases.
- **Rough Cut**: A preliminary version of the film before final editing, containing all filmed material. Rough cuts are typically for internal use, facilitating later modifications.
- **Workprint Cut**: A near-final version used for internal review or test screenings. Workprints may not yet have finalized sound, music, and visual effects.
- **Fan Edit**: A version re-edited by fans based on original film material, possibly featuring different storylines, deleted scenes, or added content to cater to specific fan preferences.
- **Redux**: A version of the film that typically extends or revises the original by restoring scenes, altering edits, or adding content to offer a different viewing experience from the original release.

### Release
The Release module currently supports 14 types of release versions. This module prioritizes matching release version information based on the movie's filename. If multiple video files exist, it will use the largest file by size for matching. If release version information cannot be found through filename, it will attempt to match using embedded video titles within the file. If multiple release versions are matched, they will be sequentially written into the release version information. If release version information still cannot be found, it will not write release version information. The supported release versions are:

- **Special Edition**: Includes additional content not present in the theatrical version, such as behind-the-scenes footage, deleted scenes, or featurettes. Special editions typically offer more viewing content for fans.
- **Restored Edition**: A version of old films digitally restored to modern visual and audio standards. This version is often used for re-releasing classic films.
- **3D Edition**: Version processed using 3D technology to provide a stereoscopic visual experience. Viewers need to wear 3D glasses for an immersive experience.
- **IMAX Edition**: Optimized for IMAX theater format, offering enhanced picture and sound quality with larger, clearer screen displays for a more impactful viewing experience.
- **Collector's Edition**: Typically includes deluxe packaging and exclusive additional content such as art books, models, or other collectibles, designed for movie enthusiasts and collectors.
- **Anniversary Edition**: A special version released to celebrate significant anniversaries of the film's release, often containing extra content and commemorative items.
- **Ultimate Edition**: The most comprehensive and complete version, containing all possible additional content such as director's commentaries, behind-the-scenes footage, deleted scenes, etc., offering the richest viewing experience.
- **Blu-ray Edition**: Released in Blu-ray disc format, providing high-definition video and audio quality, often including extra content and special features.
- **DVD Edition**: Released in DVD format, suitable for home playback devices. DVD editions typically include additional content and bonus features.
- **Limited Edition**: Released in limited quantities with unique packaging and additional content, designed for specific markets or collectors.
- **Commemorative Edition**: Released to commemorate a specific event or anniversary, featuring specially designed packaging and commemorative additional content.
- **Deluxe Edition**: Includes extensive additional content and deluxe packaging, usually offering more featurettes and behind-the-scenes footage than standard editions.
- **Director's Signature Edition**: Endorsed and personally signed by the director, often including exclusive director's commentaries and special features, with high collectible value.
- **Criterion Collection**: Distributed by Criterion Collection, focusing on high-quality film restoration and special additional content, targeting film enthusiasts and collectors.

### Source
The Source module currently supports 25 types of source versions. This module prioritizes matching source version information based on the movie's filename. If multiple video files exist, it will use the largest file by size for matching. If source version information cannot be found through filename, it will attempt to match using embedded video titles within the file. If source version information still cannot be found, it will not write source version information. The supported source versions are:

- **REMUX**: Lossless version extracted from a Blu-ray disc, without compression, maintaining the original video and audio quality.
- **BD**: Version extracted from a Blu-ray disc, with some compression applied, but offering very good video and audio quality.
- **BDRIP**: Compressed version derived from a Blu-ray disc, smaller in size but slightly lower quality compared to the Blu-ray version.
- **WEB-DL**: Version downloaded from online streaming services, offering good video and audio quality.
- **VODRIP**: Version recorded from video-on-demand services, with good video and audio quality similar to WEB-DL.
- **WEBRIP**: Version recorded from online streaming services, with lower video and audio quality compared to WEB-DL.
- **HDRIP**: Compressed version extracted from a high-definition source, offering good video and audio quality.
- **HR-HDTV**: High-resolution HDTV version, with some compression applied, better quality than regular HDTV.
- **HDTV**: High-definition version recorded from television broadcasts, good video quality but may include station watermarks and advertisements.
- **PDTV**: Version recorded from digital television broadcasts, better quality than SDTV and similar to HDTV.
- **DVD**: Version extracted from a DVD disc, offering good video and audio quality.
- **DVDRIP**: Compressed version derived from a DVD disc, with lower video and audio quality compared to DVD.
- **DVDSCR**: Version distributed to award judges or critics, relatively good video and audio quality but may include watermarks and copyright information.
- **R5**: DVD version released in Russia, good video quality but slightly inferior audio quality.
- **LDRIP**: Version extracted from LaserDisc, good video and audio quality but slightly lower than DVD.
- **PPVRIP**: Version recorded from pay-per-view services, generally good quality.
- **SDTV**: Standard-definition version recorded from television broadcasts, lower resolution but moderate quality.
- **TVRIP**: Version recorded from television broadcasts, average quality, may include station watermarks and advertisements.
- **VHSRIP**: Version extracted from VHS tapes, slightly lower video and audio quality.
- **HDTC**: High-definition version recorded from a movie theater film print, may include background noise from the theater.
- **TC**: Standard-definition version recorded from a movie theater film print, relatively lower video and audio quality.
- **HDCAM**: Version recorded using high-definition cameras in a movie theater, quality between HDTC and regular CAM.
- **HQCAM**: Version recorded using high-definition cameras in a movie theater, lower video and audio quality.
- **TS**: Version recorded using professional cameras in a movie theater, relatively good audio quality but lower video quality.
- **CAM**: Version recorded using standard cameras in a movie theater, very poor video and audio quality.

### Resolution
The Resolution module supports all resolutions recognized by Plex. This module retrieves video resolution information from the media metadata. If multiple video files exist, it retrieves resolution information from the largest file by size. If resolution information cannot be found, it will not write any resolution information. Supported resolutions include but are not limited to:

- **8K**: Including 7680 x 4320 (8K UHD) and 8192 x 4320 (8K DCI), among others.
- **4K**: Including 3840 x 2160 (4K UHD), 3996 x 2160, 4096 x 1716, and 4096 x 2160 (4K DCI), among others.
- **2.7K**: Including 2704 x 1520 and 3440 x 1440, among others.
- **2K**: Including 1998 x 1080, 2048 x 858, and 2048 x 1080 (2K DCI), among others.
- **1080P**: Including 1920 x 800, 1920 x 818, 1920 x 1034, and 1920 x 1080 (FHD), among others.
- **720P**: Including 1280 x 540, 1280 x 640, 1280 x 692, and 1280 x 720 (HD), among others.
- **576P**: Including 720 x 576 (PAL), 768 x 576, 960 x 576, and 1024 x 576, among others.
- **480P**: Including 640 x 480 (NTSC), 848 x 480, and 854 x 480, among others.
- **SD**: Including resolutions below 480P, such as 360 x 240, 426 x 240, 480 x 360, and 640 x 360, among others.

### DynamicRange
The DynamicRange module supports all dynamic ranges recognized by Plex. It retrieves dynamic range information from the movie's media metadata. When multiple video files are present, it retrieves information from the largest file by size. If dynamic range information cannot be found, it will not include any dynamic range details. Supported dynamic ranges include but are not limited to:

- **DV P8**: Dolby Vision Profile 8 offers efficient color encoding for streaming, compatible with HDR10 for broad device support, but with slightly less color performance than P5.
- **DV P7**: Dolby Vision Profile 7 is a dual-layer format designed for Blu-ray discs, providing excellent color depth and detail, requiring hardware support for playback.
- **DV P5**: Dolby Vision Profile 5 is a single-layer format optimized for streaming, offering superior color encoding compared to P8, ideal for showcasing intricate colors in Dolby Vision-native content.
- **HDR**: High Dynamic Range enhances brightness and color range of display devices, making images richer and more lifelike, enhancing immersion in viewing.
- **SDR**: Standard Dynamic Range is the traditional video format, offering limited brightness and color range but widely compatible with various devices.

Note: HDR10, HDR10+, HLG, and similar high dynamic range technologies are categorized under HDR. If a video file supports both HDR and DV, both will be included in the Edition.

### VideoCodec
The VideoCodec module supports all video codecs recognized by Plex. This module retrieves video codec information from the media metadata. If multiple video files exist, it retrieves codec information from the largest file by size. If codec information cannot be found, it will not write any codec information. Supported video codecs include but are not limited to:

- **AV1**: AOMedia Video 1, an open-source codec developed by the Alliance for Open Media, known for high compression efficiency and excellent video quality.
- **HEVC**: Also known as H.265, High Efficiency Video Coding, providing high compression efficiency and good video quality.
- **VP9**: Developed by Google, an open-source codec with high compression efficiency, commonly used on platforms like YouTube.
- **H264**: Also known as H.264 or AVC, a common codec for high-definition video encoding, with high compression efficiency widely used in streaming and video storage.
- **VC1**: Also known as SMPTE 421M, a video codec developed by Microsoft, offering good compression efficiency, commonly used in Blu-ray discs and online video.
- **MPEG4**: MPEG-4 Part 2, widely used for video streaming and discs, providing good compression efficiency.
- **SVQ3**: Sorenson Video 3, an early video compression format known for lower compression efficiency.
- **WMV3**: Also known as Windows Media Video 9, Microsoft's video codec with moderate compression efficiency.
- **WMV2**: Also known as Windows Media Video 8, an earlier Microsoft video codec with lower compression efficiency.
- **WMV1**: Also known as Windows Media Video 7, the earliest Microsoft video codec with lower compression efficiency.
- **MPEG2**: Also known as H.262, a standard codec for DVDs and some TV broadcasts, known for lower compression efficiency.
- **MPEG1**: An early video compression format, commonly used for VCDs, known for very low compression efficiency.
- **RV40**: RealVideo 4.0, a codec developed by RealNetworks, known for lower compression efficiency.

### FrameRate
The FrameRate module supports all frame rates recognized by Plex. This module retrieves frame rate information from the media metadata. If multiple video files exist, it retrieves frame rate information from the largest file by size. If frame rate information cannot be found, it will not write any frame rate information. Supported frame rates include but are not limited to:

- **240P**: Displays 240 frames per second, used for super slow-motion video capture to capture details of fast-moving subjects.
- **120P**: Displays 120 frames per second, used for high frame rate video capture and playback, common in high-end TVs and virtual reality content, providing an extremely smooth visual experience.
- **100P**: Displays 100 frames per second, primarily used for certain high frame rate TV broadcasts.
- **72P**: Displays 72 frames per second, uncommon but used in certain special movie screenings.
- **60P**: Displays 60 frames per second, commonly used for high-speed motion video, sports events, and video games, offering extremely smooth motion performance.
- **50P**: Displays 50 frames per second, used in European HD TV standards and some high frame rate video content.
- **48P**: Displays 48 frames per second, previously used in some movies like "The Hobbit" series, providing smoother motion than 24 frames per second.
- **30P**: Displays 30 frames per second, suitable for NTSC video standard, widely used in TV broadcasts in North America and Japan.
- **25P**: Displays 25 frames per second, suitable for PAL video standard, primarily used in Europe, China, Australia, and other PAL regions for TV and video content.
- **24P**: Displays 24 frames per second, traditional film frame rate commonly used in movie production, providing a unique cinematic feel.
- **15P**: Displays 15 frames per second, used for low-bandwidth video streaming and some webcams.
- **12P**: Displays 12 frames per second, previously used in early animations and low-bandwidth video transmissions.
- **10P**: Displays 10 frames per second, primarily used for very low-bandwidth video transmission and some surveillance cameras.
- **5P**: Displays 5 frames per second, used for extremely low-bandwidth surveillance and video transmission.

### AudioCodec
The AudioCodec module supports all audio codecs recognized by Plex. This module retrieves audio codec information from the media metadata. If multiple video files exist, it retrieves audio codec information from the largest file by size. If multiple audio streams exist, it retrieves the audio codec information from the stream with the highest bitrate (preferring multichannel streams). If audio codec information cannot be found, it will not write any audio codec information. Supported audio codecs include but are not limited to:

- **DTS-HD MA**: DTS-HD Master Audio, lossless encoding providing cinematic sound quality, commonly used in Blu-ray discs.
- **TRUEHD**: Dolby TrueHD, Dolby's lossless encoding offering high-fidelity sound quality, also common in Blu-ray discs.
- **FLAC**: Free Lossless Audio Codec, open-source lossless encoding widely used for music archiving and high-fidelity audio tracks.
- **PCM**: Pulse Code Modulation, lossless encoding offering original sound quality, commonly used in CDs and DVDs.
- **DTS-HD HRA**: DTS-HD High Resolution Audio, lossy encoding with sound quality superior to standard DTS.
- **DTS-ES**: DTS Extended Surround, an extension of DTS that adds a rear center channel.
- **EAC3**: Enhanced AC-3, also known as Dolby Digital Plus, enhanced version of Dolby Digital offering higher compression ratio and better audio quality.
- **DTS**: Digital Theater Systems, digital cinema system encoding widely used in movies and DVDs.
- **AC3**: Also known as Dolby Digital, Dolby's digital encoding format commonly used in DVDs and digital TV broadcasts.
- **HE-AAC**: High-Efficiency Advanced Audio Codec, advanced audio encoding with higher data compression rate compared to AAC, widely used in streaming.
- **AAC**: Advanced Audio Codec, successor to MP3 for high-quality audio encoding, widely used in streaming.
- **MP3**: MPEG-1 Audio Layer 3, the most common lossy audio codec widely used for music playback.
- **VORBIS**: Ogg Vorbis, open-source lossy encoding format commonly used in gaming and network audio.
- **WMAPRO**: Windows Media Audio Professional, Microsoft's lossy encoding offering higher audio quality.
- **COOK**: RealAudio COOK, RealNetworks' lossy encoding primarily used in early streaming.
- **MP2**: MPEG-1 Audio Layer 2, early lossy encoding format commonly used in broadcasting and VCD.
- **WMAV2**: Windows Media Audio Version 2, a variant of WMA offering higher audio compression rate and lower audio quality.
- **WMA**: Windows Media Audio, Microsoft's lossy encoding widely used on Windows platforms.

Note: When writing Edition, the audio codec will display the corresponding channel information of the audio stream, such as TRUEHD 7.1, AC3 5.1, AAC Stereo, etc.

### Bitrate
The Bitrate module retrieves the bitrate information of video files from the media metadata recognized by Plex. If multiple video files exist, it retrieves the bitrate information from the largest file by size. If bitrate information cannot be found, it will not write any bitrate information (bitrate units are in Kbps, Mbps).

### Size
The Size module retrieves the size information of video files from the media metadata. If multiple video files exist, it retrieves the size information from the largest file by size (size units are in B, KB, MB, GB).

### Country
The Country module retrieves the country (or region) information of movies from the movie metadata. If multiple countries exist, it sequentially writes the country information. If country information cannot be found, it will not write any country information.

### ContentRating
The ContentRating module retrieves the content rating information of movies from the movie metadata. If content rating information cannot be found, it will not write any content rating information. Supported content ratings include but are not limited to:

#### Movie Ratings (MPAA)
- **G**: General Audiences – Suitable for all ages. Contains nothing that would offend parents for viewing by children.
- **PG**: Parental Guidance Suggested – Some material may not be suitable for children. Parents are urged to give "parental guidance."
- **PG-13**: Parents Strongly Cautioned – Some material may be inappropriate for children under 13. Parents are urged to be cautious.
- **R**: Restricted – Restricted to viewers over the age of 17 or accompanied by a parent or adult guardian. Contains strong language, violence, or sexual content.
- **NC-17**: Adults Only – No one 17 and under admitted. Contains explicit sexual or violent content.
- **NR**: Not Rated – The film has not been submitted for rating to the MPAA.
- **Unrated**: A version not officially rated by organizations like the MPAA, may contain content not included in the original rating.

#### TV Show Ratings (TV Parental Guidelines)
- **TV-Y**: Television for All Children – Suitable for all children. Typically suitable for ages 2-6.
- **TV-Y7**: Directed to Older Children – Suitable for children age 7 and above. May contain mild fantasy violence or infrequent use of mild language.
- **TV-Y7-FV**: Directed to Older Children - Fantasy Violence – Suitable for children age 7 and above. Contains fantasy violence.
- **TV-G**: General Audience – Suitable for all ages. Contains little or no violence, no strong language, and little or no sexual dialogue or situations.
- **TV-PG**: Parental Guidance Suggested – Some material may not be suitable for children. Parents are urged to provide "parental guidance."
- **TV-14**: Parents Strongly Cautioned – Contains some material that many parents would find unsuitable for children under 14.
- **TV-MA**: Mature Audience Only – This program is specifically designed to be viewed by adults and may be unsuitable for children under 17. May contain crude indecent language, explicit sexual activity, or graphic violence.

#### Other Rating Standards
- **Approved**: Approved by the Motion Picture Association or other relevant authorities. Suitable for public viewing, specific content may vary depending on release era.
- **18+**: Restricted to viewers 18 years and older. Contains adult-oriented content.
- **AO**: Adults Only – Used for video game ratings, suitable only for adults.

Note: The above ratings are based on the U.S. rating system. Ratings systems in other regions may vary.

### Rating
The Rating module retrieves the audience rating information of movies from the movie metadata (using the configured rating source from the database). If rating information cannot be found, it will not write any rating information (ratings will be converted to a 10-point scale).

### Duration
The Duration module retrieves the duration information of video files from the media metadata of movies. If multiple video files exist, it retrieves the duration information from the largest file by size. If duration information cannot be found, it will not write any duration information (duration is measured in minutes).

## Features
The EMP operates in three modes: `add editions for all movies (all)`, `add editions for new movies (new)`, and `reset editions for all movies (reset)`:

- **add editions for all movies**: Based on user configuration, this mode adds editions for all movies in libraries excluding those configured to be skipped. Movies with existing editions will be skipped.
- **add editions for new movies**: This mode utilizes Webhooks to listen for server events in real-time, capturing metadata for newly added items. It then adds editions only for newly added movies (excluding those in libraries configured to be skipped).
- **reset editions for all movies**: According to user settings, this mode resets (removes) editions for all movies in libraries excluding those configured to be skipped.

Note: The `add editions for new movies` mode requires the server administrator account to be subscribed to Plex Pass in order to use.

## Configuration
Before using EMP, please configure the `/config/config.ini` file according to the following tips (example).
```
[server]
# Address of the Plex server, formatted as http://server IP address:32400 or http(s)://domain:port
address = http://127.0.0.1:32400
# Token of the Plex server for authentication
token = xxxxxxxxxxxxxxxxxxxx
# Specify libraries to skip, format should be LibraryName1;LibraryName2;LibraryName3, leave empty if no libraries need to be skipped
skip_libraries = Cloud Movie;Concert
# Language setting, zh for Chinese, en for English
language = en

[modules]
# Specify modules to write and their order, format should be Module1;Module2;Module3, optional modules include Cut, Release, Source, Resolution, DynamicRange, VideoCodec, FrameRate, AudioCodec, Bitrate, Size, Country, ContentRating, Rating, Duration
order = Source;DynamicRange
```
Since EMP only processes libraries of movie type, specify libraries of movie type to skip when needed. There is no limit to the number of modules for writing editions, so you can choose and configure them according to your needs.

When running in `add editions for new movies` mode, EMP creates a Flask web server that listens on port `8089` to receive `library.new` events sent by the Plex server. This allows it to capture metadata for newly added items and process them accordingly.

If port `8089` is already occupied by another service, you may need to modify the `port=8089` on the ninth last line of `edition-manager-for-plex.py` (when running via Python script) or adjust port mapping (when running via Docker container) to change the listening port.

## How to Run
You can run EMP using Docker containers or Python scripts. Docker containerization is recommended for its ease of use and scalability. Detailed instructions for each method are provided below.

### Running via Docker Container

#### Requirements
- Docker and Docker Compose installed.

#### Docker Compose
- edition-manager-for-plex (Plex Pass subscribers)
  
   ```
   version: "2"
   services:
     emp-all:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-all
       command: python edition-manager-for-plex.py --all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
     emp-new:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-new
       command: python edition-manager-for-plex.py --new
       ports:
         - 8089:8089
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
       restart: unless-stopped
   networks: {}
   ```
- edition-manager-for-plex（Non-Plex Pass subscribers）
  
   ```
   version: "2"
   services:
     emp-scheduler:
       image: mcuadros/ofelia:latest
       container_name: emp-scheduler
       depends_on:
         - emp-all
       command: daemon --docker -f label=com.docker.compose.project=${COMPOSE_PROJECT_NAME}
       labels:
         ofelia.job-run.emp-all.schedule: 0 30 22 * * *
         ofelia.job-run.emp-all.container: emp-all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
       restart: unless-stopped
     emp-all:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-all
       command: python edition-manager-for-plex.py --all
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
   networks: {}
   ```
- edition-manager-for-plex-reset
  
   ```
   version: "2"
   services:
     emp-reset:
       image: x1ao4/edition-manager-for-plex:latest
       container_name: emp-reset
       command: python edition-manager-for-plex.py --reset
       environment:
         - TZ=Asia/Shanghai
       volumes:
         - /custom/directory/edition-manager-for-plex/config:/app/config
   networks: {}
   ```

#### Usage
With EMP, you can write edition information as well as remove it. Since Docker automatically starts all containers within the stack upon stack initialization, the functions for writing and removing need to be deployed separately. First, deploy `edition-manager-for-plex` to write edition information, then deploy `edition-manager-for-plex-reset` when needed to remove edition information (upon deployment, it will immediately execute a `reset editions for all movies` once. You can also use `docker-compose up --no-start` to deploy this container, which will not run immediately after deployment; start the container only when needed).

- edition-manager-for-plex

  1. In the Plex server settings, navigate to `Webhooks`, click on `Add Webhook`, and enter your Flask server address `http://Docker host IP address:8089` and `Save Changes`. (Non-Plex Pass subscribers do not need to fill this.)
  2. Download the `/compose/edition-manager-for-plex/compose.yaml` file from the repository (Plex Pass subscribers should delete the `emp-scheduler` section; non-Plex Pass subscribers should delete the `emp-new` section) and save it in a folder named `edition-manager-for-plex`.
  3. Open `compose.yaml` with a text editor and replace `/custom/directory/edition-manager-for-plex/config` with a directory on your host machine where configuration files will be stored. (Both `emp-all` and `emp-new` should use the same directory.)
  4. Open the terminal or command line tool, use the `cd` command to switch to the directory where `compose.yaml` is located.
  5. Use the command `docker-compose up -d` to deploy and start the edition-manager-for-plex stack.
  6. Open `/custom/directory/edition-manager-for-plex/config/config.ini` with a text editor, fill in your Plex server address (`address`) and [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) (`token`), set the modules to write edition information and their order (`order`), and optionally fill in other configuration options as needed.
  7. Restart the edition-manager-for-plex stack to start running properly.

- edition-manager-for-plex-reset

  1. Download the `/compose/edition-manager-for-plex-reset/compose.yaml` file from the repository and save it in a folder named `edition-manager-for-plex-reset`.
  2. Open `compose.yaml` with a text editor and replace `/custom/directory/edition-manager-for-plex/config` with a directory on your host machine where configuration files will be stored. (Use the same directory as `emp-all` and `emp-new`.)
  3. Open the terminal or command line tool, use the `cd` command to switch to the directory where `compose.yaml` is located.
  4. Use the command `docker-compose up -d` to deploy and start the edition-manager-for-plex-reset stack. (If `/custom/directory/edition-manager-for-plex/config/config.ini` is correctly configured, the stack will operate properly; if not configured, fill in the configuration information first, then restart the stack for proper operation.)

#### Instructions
EMP consists of four containers: `emp-all`, `emp-new`, `emp-scheduler`, and `emp-reset`, each designed to handle different tasks. Upon stack deployment, these containers will have slightly different running states.

- The `emp-all` container is used for the `add editions for all movies` task. It runs this task once after startup, processing all movies within the set scope (adding edition information), and displays the library information and processing results in the terminal or logs. It will stop running after completing the task. You can start it at any time to run the `add editions for all movies` task, and it will stop after each run. If you have configured `emp-scheduler`, `emp-all` will also run once automatically at each scheduled task time.
- The `emp-new` container is used for the `add editions for new movies` task. After startup, it will create a Flask server to listen for events from the Plex server. When there are new movies on the Plex server, it will automatically process the new movies (add edition information) and display the processing results in the terminal or logs. After processing, it will continue to listen for events from the Plex server and handle any new movies as they arrive, then resume listening.
- The `emp-scheduler` container is used to set/trigger scheduled tasks for `add editions for all movies`. After startup, it will create a scheduled task to run `emp-all` at a default setting of `0 30 22 * * *`, which means it will run once daily at 10:30 PM. You can customize the running frequency by modifying the cron expression, such as `"@every 3h"` for every 3 hours or `"@every 30m"` for every 30 minutes. It will start the `emp-all` container at the scheduled task time and synchronize the `emp-all` log information in the terminal or logs, then continue running.
- The `emp-reset` container is used for the `reset editions for all movies` task. It runs this task once after startup, processing all movies within the set scope (resetting/removing edition information), and displays the library information and processing results in the terminal or logs. It will stop running after completing the task. You can start it at any time to run the `reset editions for all movies` task, and it will stop after each run.

You can select and configure these four containers as needed. If certain functions are not required, simply delete the corresponding parts in the Compose file before deployment.

### Running via Python Script

#### Requirements
- Python 3.0 or higher installed.
- Necessary third-party libraries installed using the command `pip3 install -r requirements.txt`.

#### Usage
1. Download the latest release package from [Releases](https://github.com/x1ao4/edition-manager-for-plex/releases) and extract it to a local directory.
2. Open the `/config/config.ini` file in the directory using a text editor, fill in your Plex server address (`address`) and [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) (`token`), set the modules to write edition information and their order (`order`), and optionally fill in other configuration options as needed.
3. In the Plex server settings, navigate to `Webhooks`, click on `Add Webhook`, and enter your Flask server address `http://IP address of the device running the script:8089` and `Save Changes`. (Non-Plex Pass subscribers do not need to fill this.)
4. Open a terminal or command line tool, use the `cd` command to switch to the directory where the script is located.
5. Use the command `python3 edition-manager-for-plex.py --all` to run the `add editions for all movies` task. The script will process all movies within the configured scope (adding edition information) and display library information and processing results in the console. It will stop running after completing the task.
6. Use the command `python3 edition-manager-for-plex.py --new` to run the `add editions for new movies` task. The script will create a Flask server to listen for events from the Plex server. When there are new movies on the Plex server, the script will automatically process the new movies (adding edition information) and display the processing results in the console. After processing, it will continue to listen for events from the Plex server and handle new movies as they arrive, then resume listening.
7. Use the command `python3 edition-manager-for-plex.py --reset` to run the `reset editions for all movies` task. The script will process all movies within the configured scope (resetting/removing edition information) and display library information and processing results in the console. It will stop running after completing the task.

#### Quick Start
PC users can quickly start tasks by double-clicking the provided scripts:

- To run the `add editions for all movies` task, double-click `emp-all.bat (Win)` or `emp-all.command (Mac)`.
- To run the `add editions for new movies` task, double-click `emp-new.bat (Win)` or `emp-new.command (Mac)`.
- To run the `reset editions for all movies` task, double-click `emp-reset.bat (Win)` or `emp-reset.command (Mac)`.

#### Auto-Run Setup
For convenience, you can set up EMP to run automatically using crontab or other task scheduling tools.

- Add Editions for All Movies (Mac)
  
  1. Open the crontab file in the terminal with the command `crontab -e`.
  2. Press `i` to enter insert mode and add the line `30 22 * * * /path/to/emp-all.command > /dev/null 2>&1`. (Replace `/path/to/emp-all.command` with the actual path to your script.)
  3. Press `Esc` to exit insert mode, type `:wq`, and press `Enter` to save changes and exit the editor.

  This sets up a scheduled task to run the `add editions for all movies` script every day at 10:30 PM. You can customize the frequency by modifying the time expression, such as `0 */3 * * *` to run every 3 hours or `*/30 * * * *` to run every 30 minutes. (The script will run in the background.)

- Add Editions for New Movies (Mac)
  
  1. Open the `emp-new.command` file with a text editor, add `sleep 10` on the second line, save the changes, and close the file.
  2. Open the crontab file in the terminal with the command `crontab -e`.
  3. Press `i` to enter insert mode and add the line `@reboot /path/to/emp-new.command`. (Replace `/path/to/emp-new.command` with the actual path to your script.)
  4. Press `Esc` to exit insert mode, type `:wq`, and press `Enter` to save changes and exit the editor.

  This sets the `add editions for new movies` script to run on Mac startup, with a 10-second delay to ensure the Plex server starts before the script. (The script will run in the background.)

- Add Editions for All Movies (NAS)
  
  Use the built-in task scheduler to add a scheduled task for `add editions for all movies`. After adding the task, enter `python3 /path/to/edition-manager-for-plex.py --all` in the `Run Command - User-Defined Script` field, then set the desired run time. (Replace `/path/to/edition-manager-for-plex.py` with the actual path to your script.)
  
- Add Editions for New Movies (NAS)
  
  Use the built-in task scheduler to set `add editions for new movies` to run at startup. After adding the task, enter `sleep 10 && python3 /path/to/edition-manager-for-plex.py --new` in the `Run Command - User-Defined Script` field. This ensures the script runs 10 seconds after NAS startup, giving the Plex server time to start first. (Replace `/path/to/edition-manager-for-plex.py` with the actual path to your script.)

If the scripts fail to run as scheduled or on startup, you may need to replace `python3` with the full path to the Python interpreter. You can find the actual path to `python3` using the `which python3` command in the Mac terminal or NAS SSH.

## Notes
- Ensure you provide the correct Plex server address and the correct X-Plex-Token.
- Ensure you provide the correct library names and fill them in as required.
- Ensure you correctly set the language and module information as required.
- If the script or container cannot connect to the Plex server, please check your network connection and ensure the server is accessible. If you are running it through a Docker container, you can also try redeploying the container using the `host` mode.
- Please use the X-Plex-Token of the server administrator account to ensure you have sufficient permissions to perform operations.
- The edition field will be locked after being added. If modifications are needed, Plex Pass subscribers can manually unlock the edition field and then modify it; non-Plex Pass subscribers do not support manual modification of the edition field. To modify the edition modules or their order for all movies, first reset the editions, then modify the configuration file, and finally rewrite the editions.
- After modifying the configuration file, you need to restart the container for the new configuration to take effect.
- If Windows users see no response after running the Python script, try replacing `python3` with `python` in the run command or start script.
- To use the `add editions for new movies` mode, please ensure you have checked the `Webhooks` option in the server's `Settings - Network` section.

## Support
If you found this helpful, consider buying me a coffee or giving it a ⭐️. Thanks for your support!

<img width="399" alt="Support" src="https://github.com/x1ao4/edition-manager-for-plex/assets/112841659/b9e79a88-f2af-4c3a-8278-479454c6393a">
<br><br>
<a href="#edition-manager-for-plex-en">Back to Top</a>

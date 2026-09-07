# CS224N · Natural Language Processing with Deep Learning

> **非官方学习归档。** 不是斯坦福或 CS224N 课程组的发布。  
> 幻灯片、作业、论文的版权仍归原作者；本仓库只整理了目录和说明。  
> 详见 [NOTICE.md](NOTICE.md)。公开到 GitHub 前请先读该文件：声明**不能**代替授权，**不建议**公开本学期作业包。

斯坦福大学 **Winter 2026** 课程资料镜像（从[课程官网](https://web.stanford.edu/class/cs224n/)公开链接下载）。

- 授课：Diyi Yang、Yejin Choi
- Head TA：Julie Kallini
- 时间：周二 / 周四 16:30–17:50 Pacific Time，NVIDIA Auditorium
- 交叉课号：CS224N / LING 284 / SYMSYS 195N
- 版权与来源：[NOTICE.md](NOTICE.md) · 整理层许可：[LICENSE](LICENSE)


## 目录怎么读

每一讲一个文件夹，命名规则：

`W周.节-星期-月-日-英文标题-中文标题`

例如 `W1.1` 就是第 1 周第 1 讲（周二），`W1.2` 是同周周四，`W1.3` 是周五辅导课。

每讲内部结构固定：

```
Wn.m-.../
  README.md                 # 标题、描述、资料索引
  01-slides-幻灯片/
  02-notes-讲义/
  03-readings-阅读材料/
  04-assignment-作业/        # 仅当本讲发布作业
  05-project-期末项目/       # 仅当本讲发布项目材料
```

课程级材料：

- `00-课程总览/`：主页快照、答疑页、参考书
- `FP-期末项目/`：提案 / 默认 GPT-2 项目 / 中期 / 终稿说明汇总

## 课表

| 编号 | 日期 | 标题 | 类型 |
| --- | --- | --- | --- |
| [W1.1](W1.1-Tue-Jan-06-History-of-NLP-NLP历史/README.md) | Tue Jan 6, 2026 | NLP 历史 / History of NLP | 正课 |
| [W1.2](W1.2-Thu-Jan-08-Word-Vectors-词向量/README.md) | Thu Jan 8, 2026 | 词向量 / Word Vectors | 正课 |
| [W1.3](W1.3-Fri-Jan-09-Python-Review-Python复习课/README.md) | Fri Jan 9, 2026 | Python 复习课 / Python Review Session | 辅导课 |
| [W2.1](W2.1-Tue-Jan-13-Neural-Nets-神经网络基础/README.md) | Tue Jan 13, 2026 | 反向传播与神经网络基础 / Backpropagation and Neural Network Basics | 正课 |
| [W2.2](W2.2-Thu-Jan-15-RNNs-语言模型与RNN/README.md) | Thu Jan 15, 2026 | 语言模型与循环神经网络 / Language Models and RNNs | 正课 |
| [W2.3](W2.3-Fri-Jan-16-PyTorch-Tutorial-PyTorch教程/README.md) | Fri Jan 16, 2026 | PyTorch 教程 / PyTorch Tutorial Session | 辅导课 |
| [W3.1](W3.1-Tue-Jan-20-Transformers-Transformer/README.md) | Tue Jan 20, 2026 | Transformer / Transformers | 正课 |
| [W3.2](W3.2-Thu-Jan-22-Final-Projects-期末项目指导/README.md) | Thu Jan 22, 2026 | 期末项目：默认题 / 自选题与实践建议 / Final Projects: Custom and Default; Practical Tips | 正课 |
| [W4.1](W4.1-Tue-Jan-27-Pretraining-预训练/README.md) | Tue Jan 27, 2026 | 预训练：规模、系统与数据 / Pretraining (Scaling, Systems, Data) | 正课 |
| [W4.2](W4.2-Thu-Jan-29-Post-training-后训练/README.md) | Thu Jan 29, 2026 | 后训练：RLHF、SFT 与 DPO / Post-training (RLHF, SFT, DPO) | 正课 |
| [W5.1](W5.1-Tue-Feb-03-PEFT-高效适配/README.md) | Tue Feb 3, 2026 | 高效适配：提示学习与参数高效微调 / Efficient Adaptation (Prompting + PEFT) | 正课 |
| [W5.2](W5.2-Thu-Feb-05-Agents-RAG-智能体与检索增强/README.md) | Thu Feb 5, 2026 | 智能体、工具使用与检索增强生成 / Agents, Tool Use, and RAG | 正课 |
| [W5.3](W5.3-Fri-Feb-06-HuggingFace-Tutorial-HuggingFace教程/README.md) | Fri Feb 6, 2026 | Hugging Face Transformers 教程 / Hugging Face Transformers Tutorial Session | 辅导课 |
| [W6.1](W6.1-Tue-Feb-10-Evaluation-评测与基准/README.md) | Tue Feb 10, 2026 | 评测与基准 / Benchmarking and Evaluation | 正课 |
| [W6.2](W6.2-Thu-Feb-12-Reasoning-1-推理上/README.md) | Thu Feb 12, 2026 | 推理（上） / Reasoning 1 | 正课 |
| [W7.1](W7.1-Tue-Feb-17-Reasoning-2-推理下/README.md) | Tue Feb 17, 2026 | 推理（下） / Reasoning 2 | 正课 |
| [W7.2](W7.2-Thu-Feb-19-Tokenization-Multilinguality-分词与多语言/README.md) | Thu Feb 19, 2026 | 嘉宾课：分词与多语言（Julie Kallini） / Guest Lecture: Tokenization and Multilinguality (Julie Kallini) | 嘉宾课 |
| [W8.1](W8.1-Tue-Feb-24-Interpretability-可解释性/README.md) | Tue Feb 24, 2026 | 嘉宾课：可解释性（Been Kim） / Guest Lecture: Interpretability (Been Kim) | 嘉宾课 |
| [W8.2](W8.2-Thu-Feb-26-Social-Impacts-社会影响与风险/README.md) | Thu Feb 26, 2026 | NLP 的社会影响与风险 / Social and Broader Impacts of NLP (Risks) | 正课 |
| [W9.1](W9.1-Tue-Mar-03-Multimodality-多模态/README.md) | Tue Mar 3, 2026 | 嘉宾课：多模态（Luke Zettlemoyer） / Guest Lecture: Multimodality (Luke Zettlemoyer) | 嘉宾课 |
| [W9.2](W9.2-Thu-Mar-05-Tinker-LoRA-Tinker与无悔LoRA/README.md) | Thu Mar 5, 2026 | 嘉宾课：Tinker 与无悔 LoRA（John Schulman） / Guest Lecture: Tinker and LoRA Without Regret (John Schulman) | 嘉宾课 |
| [W10.1](W10.1-Tue-Mar-10-Open-Questions-NLP开放问题/README.md) | Tue Mar 10, 2026 | NLP 2026 开放问题 / Open Questions in NLP 2026 | 正课 |
| [W10.2](W10.2-Thu-Mar-12-No-Lecture-无课-项目截止/README.md) | Thu Mar 12, 2026 | 无课（期末项目截止） / No Lecture | 截止日期 |
| [W10.3](W10.3-Mon-Mar-16-Poster-Session-项目海报展示/README.md) | Mon Mar 16, 2026 | 期末项目海报展示 / Final Project Poster Session | 展示 |

## 作业一览

| 作业 | 发布 | 截止 | 内容 | 成绩 |
| --- | --- | --- | --- | --- |
| A1 | W1.1 Tue Jan 6 | W2.1 Tue Jan 13 | 词向量入门 | 6% |
| A2 | W2.1 Tue Jan 13 | W3.2 Thu Jan 22 | 神经网络基础、张量求导、依存句法 | 14% |
| A3 | W3.2 Thu Jan 22 | W5.2 Thu Feb 5 | Self-attention 与 Transformer | 14% |
| A4 | W5.2 Thu Feb 5 | W7.2 Thu Feb 19 | 大语言模型评测 | 14% |

期末项目 49%（提案 8% + 中期 6% + 海报 3% + 终稿 32%），参与 3%。

## 下载情况

课程官网列出的幻灯片、讲义、作业和绝大部分论文都已落到本地。仍无法稳定镜像的主要是：

- 课堂录像（Canvas / 需登录）
- Colab 笔记本（已在对应讲次 README 保留链接）
- 少数 403 页面：Been Kim 的 Medium 文、PNAS AlphaZero 论文 PDF
- 嘉宾课 W8.1 / W9.1 / W9.2 的幻灯片官网尚未放出

替代下载已补上：Manning Daedalus 文的公开转写、InstructGPT arXiv 版、Rumelhart 1986 PDF、Goldberg primer、词嵌入维度论文 arXiv 版。

## 说明

- 公开录像可看 [2024 YouTube playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D)。
- 作业每年会改，官网明确要求不要做往年作业。
- 重新同步可用 `_build_course.py`（已下载的文件会跳过）。
- 版权、第三方材料、AI 生成范围见 [NOTICE.md](NOTICE.md)。


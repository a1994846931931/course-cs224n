#!/usr/bin/env python3
"""Download and organize Stanford CS224N Winter 2026 course materials.

AI-assisted archival script. It does not claim copyright over course PDFs,
assignments, or papers. See NOTICE.md and LICENSE in the repo root.
"""

from __future__ import annotations

import json
import re
import shutil
import ssl
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path("/Users/a1994846931931/workspace/course-cs224n")
BASE = "https://web.stanford.edu/class/cs224n/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def local(url: str) -> str:
    return BASE + url.lstrip("/")


def arxiv(arxiv_id: str) -> str:
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

LECTURES = [
    {
        "id": "W1.1",
        "folder": "W1.1-Tue-Jan-06-History-of-NLP-NLP历史",
        "date": "Tue Jan 6, 2026",
        "title_en": "History of NLP",
        "title_zh": "NLP 历史",
        "kind": "正课",
        "desc": "课程导论与 NLP 发展史。先介绍 CS224N 的目标、作业与项目安排，再梳理 NLP 的范式变迁：从规则系统、统计机器学习，到 2010 年代端到端神经网络，再到 2020 年代大语言模型规模化。核心问题是：每个时代对语言的假设，如何决定了当时能做成什么、做不成什么。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture01-intro.pdf"), "cs224n-2026-lecture01-intro-课程介绍.pdf"),
            (local("slides_w26/cs224n-2026-lecture01-history.pdf"), "cs224n-2026-lecture01-history-NLP历史.pdf"),
        ],
        "notes": [],
        "readings": [
            (
                "https://www.amacad.org/publication/daedalus/human-language-understanding-reasoning",
                "Human-Language-Understanding-and-Reasoning-人类语言理解与推理.html",
                "Human Language Understanding & Reasoning",
                "suggested",
            ),
        ],
        "assignments": [
            (local("assignments_w26/a1.zip"), "a1-code-作业1代码-词向量入门.zip"),
        ],
        "events": ["Assignment 1 发布：词向量入门（占期末 6%）"],
        "deadlines": [],
    },
    {
        "id": "W1.2",
        "folder": "W1.2-Thu-Jan-08-Word-Vectors-词向量",
        "date": "Thu Jan 8, 2026",
        "title_en": "Word Vectors",
        "title_zh": "词向量",
        "kind": "正课",
        "desc": "介绍分布式语义假设与静态词向量：word2vec（Skip-gram / CBOW）、负采样，以及 GloVe。理解如何把词变成可计算的向量，以及这些向量如何编码类比、相似度和多义词结构。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture02-wordvecs.pdf"), "cs224n-2026-lecture02-wordvecs-词向量.pdf"),
        ],
        "notes": [
            (local("readings/cs224n_winter2023_lecture1_notes_draft.pdf"), "cs224n-notes-wordvecs-1-词向量讲义1.pdf"),
            (local("readings/cs224n-2019-notes02-wordvecs2.pdf"), "cs224n-notes-wordvecs-2-词向量讲义2.pdf"),
        ],
        "readings": [
            (arxiv("1301.3781"), "1301.3781-word2vec-词向量空间中的高效表示估计.pdf", "Efficient Estimation of Word Representations in Vector Space (word2vec)", "suggested"),
            ("https://proceedings.neurips.cc/paper_files/paper/2013/file/9aa42b31882ec039965f3c4923ce901b-Paper.pdf", "nips2013-word2vec-negative-sampling-词与短语的分布式表示.pdf", "Distributed Representations of Words and Phrases and their Compositionality", "suggested"),
            ("https://nlp.stanford.edu/pubs/glove.pdf", "glove-全局词向量.pdf", "GloVe: Global Vectors for Word Representation", "suggested"),
            ("https://aclanthology.org/Q15-1016.pdf", "Q15-1016-Improving-Distributional-Similarity-改进分布相似性.pdf", "Improving Distributional Similarity with Lessons Learned from Word Embeddings", "suggested"),
            ("https://aclanthology.org/D15-1036.pdf", "D15-1036-Evaluation-methods-for-unsupervised-word-embeddings-无监督词嵌入评估.pdf", "Evaluation methods for unsupervised word embeddings", "suggested"),
            ("https://aclanthology.org/Q16-1028.pdf", "Q16-1028-PMI-based-Word-Embeddings-基于PMI的词嵌入潜变量模型.pdf", "A Latent Variable Model Approach to PMI-based Word Embeddings", "additional"),
            ("https://aclanthology.org/Q16-1013.pdf", "Q16-1013-Linear-Algebraic-Structure-of-Word-Senses-词义的线性代数结构.pdf", "Linear Algebraic Structure of Word Senses, with Applications to Polysemy", "additional"),
            ("https://proceedings.neurips.cc/paper_files/paper/2018/file/b3ba1471b12382fa4ddca4d277afd544-Paper.pdf", "nips2018-dimensionality-of-word-embedding-词嵌入的维度.pdf", "On the Dimensionality of Word Embedding", "additional"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W1.3",
        "folder": "W1.3-Fri-Jan-09-Python-Review-Python复习课",
        "date": "Fri Jan 9, 2026",
        "title_en": "Python Review Session",
        "title_zh": "Python 复习课",
        "kind": "辅导课",
        "desc": "面向作业的 Python / NumPy 复习。时间 13:30–14:50，地点 NVIDIA Auditorium。另有 Colab 笔记本可边看边练。",
        "slides": [
            (local("slides_w25/2024 CS224N Python Review Session Slides.pptx.pdf"), "2024-CS224N-Python-Review-Python复习课幻灯片.pdf"),
        ],
        "notes": [],
        "readings": [
            ("https://colab.research.google.com/drive/1hxWtr98jXqRDs_rZLZcEmX_hUcpDLq6e?usp=sharing", None, "Python Review Colab", "colab"),
        ],
        "assignments": [],
        "events": ["13:30–14:50 · NVIDIA Auditorium"],
        "deadlines": [],
    },
    {
        "id": "W2.1",
        "folder": "W2.1-Tue-Jan-13-Neural-Nets-神经网络基础",
        "date": "Tue Jan 13, 2026",
        "title_en": "Backpropagation and Neural Network Basics",
        "title_zh": "反向传播与神经网络基础",
        "kind": "正课",
        "desc": "神经网络前向计算、损失函数、矩阵微积分与反向传播。为后面自己推导 Transformer / 依赖句法分析作业打基础。强调：不能只会调库，要能对张量求导。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture03-neuralnets.pdf"), "cs224n-2026-lecture03-neuralnets-神经网络基础.pdf"),
        ],
        "notes": [
            (local("readings/cs224n-2019-notes03-neuralnets.pdf"), "cs224n-notes-neuralnets-神经网络讲义.pdf"),
            (local("readings/gradient-notes.pdf"), "gradient-notes-矩阵微积分笔记.pdf"),
            (local("readings/review-differential-calculus.pdf"), "review-differential-calculus-微分复习.pdf"),
        ],
        "readings": [
            ("https://cs231n.github.io/neural-networks-1/", "CS231n-neural-networks-1-网络结构笔记.html", "CS231n notes on network architectures", "suggested"),
            ("https://cs231n.github.io/optimization-2/", "CS231n-optimization-2-反向传播笔记.html", "CS231n notes on backprop", "suggested"),
            ("https://cs231n.stanford.edu/handouts/derivatives.pdf", "CS231n-derivatives-导数反向传播与向量化.pdf", "Derivatives, Backpropagation, and Vectorization", "suggested"),
            ("https://www.iro.umontreal.ca/~vincentp/ift3395/lectures/backprop_old.pdf", "Rumelhart-1986-backprop-用反向传播学习表示.pdf", "Learning Representations by Backpropagating Errors", "suggested"),
            ("https://medium.com/@karpathy/yes-you-should-understand-backprop-e2f06eab496b", "Karpathy-Yes-you-should-understand-backprop-你应该理解反向传播.html", "Yes you should understand backprop", "additional"),
            ("https://www.jmlr.org/papers/volume12/collobert11a/collobert11a.pdf", "Collobert-2011-NLP-almost-from-scratch-几乎从零开始的NLP.pdf", "Natural Language Processing (Almost) from Scratch", "additional"),
        ],
        "assignments": [
            (local("assignments_w26/a2.zip"), "a2-code-作业2代码-神经网络与依存句法.zip"),
            (local("assignments_w26/a2.pdf"), "a2-handout-作业2说明.pdf"),
            (local("assignments_w26/a2_tex.zip"), "a2-latex-作业2LaTeX模板.zip"),
        ],
        "events": ["Assignment 2 发布：神经网络基础、张量求导、依存句法分析（14%）"],
        "deadlines": ["Assignment 1 截止"],
    },
    {
        "id": "W2.2",
        "folder": "W2.2-Thu-Jan-15-RNNs-语言模型与RNN",
        "date": "Thu Jan 15, 2026",
        "title_en": "Language Models and RNNs",
        "title_zh": "语言模型与循环神经网络",
        "kind": "正课",
        "desc": "从 n-gram 到神经语言模型，介绍 RNN / LSTM 如何对序列建模，以及梯度消失/爆炸为何让长程依赖很难学。Transformer 的注意力机制正是对这一问题的回应。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture04-rnnlm.pdf"), "cs224n-2026-lecture04-rnnlm-语言模型与RNN.pdf"),
        ],
        "notes": [
            (local("readings/cs224n-2019-notes05-LM_RNN.pdf"), "cs224n-notes-LM-RNN-语言模型与RNN讲义.pdf"),
        ],
        "readings": [
            ("https://ieeexplore.ieee.org/document/279181", None, "Learning long-term dependencies with gradient descent is difficult (IEEE, 可能需订阅)", "suggested"),
            (arxiv("1211.5063"), "1211.5063-difficulty-of-training-RNNs-训练RNN的困难.pdf", "On the difficulty of training Recurrent Neural Networks", "suggested"),
            ("https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1174/lectures/vanishing_grad_example.html", "vanishing-grad-example-梯度消失演示.html", "Vanishing Gradients Jupyter Notebook", "suggested"),
            (arxiv("1706.03762"), "1706.03762-Attention-Is-All-You-Need-注意力机制即所需.pdf", "Attention Is All You Need", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W2.3",
        "folder": "W2.3-Fri-Jan-16-PyTorch-Tutorial-PyTorch教程",
        "date": "Fri Jan 16, 2026",
        "title_en": "PyTorch Tutorial Session",
        "title_zh": "PyTorch 教程",
        "kind": "辅导课",
        "desc": "作业与期末项目都用 PyTorch。本辅导课过一遍张量、自动求导、nn.Module 与训练循环。时间 13:30–14:50，NVIDIA Auditorium。",
        "slides": [],
        "notes": [],
        "readings": [
            ("https://colab.research.google.com/drive/1Pz8b_h-W9zIBk1p2e6v-YFYThG1NkYeS?usp=sharing", None, "PyTorch Tutorial Colab", "colab"),
        ],
        "assignments": [],
        "events": ["13:30–14:50 · NVIDIA Auditorium"],
        "deadlines": [],
    },
    {
        "id": "W3.1",
        "folder": "W3.1-Tue-Jan-20-Transformers-Transformer",
        "date": "Tue Jan 20, 2026",
        "title_en": "Transformers",
        "title_zh": "Transformer",
        "kind": "正课",
        "desc": "课程的架构核心：self-attention、多头注意力、位置编码、残差与 LayerNorm、编码器/解码器结构。后续预训练、后训练、Agent 都建立在这一架构上。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture05-transformers.pdf"), "cs224n-2026-lecture05-transformers-Transformer.pdf"),
        ],
        "notes": [
            (local("readings/cs224n-self-attention-transformers-2023_draft.pdf"), "cs224n-notes-self-attention-transformers-自注意力与Transformer讲义.pdf"),
        ],
        "readings": [
            (arxiv("1706.03762"), "1706.03762-Attention-Is-All-You-Need-注意力机制即所需.pdf", "Attention Is All You Need", "suggested"),
            ("https://jalammar.github.io/illustrated-transformer/", "Illustrated-Transformer-图解Transformer.html", "The Illustrated Transformer", "suggested"),
            ("https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html", "Google-AI-blog-Transformer-新型神经网络.html", "Transformer (Google AI blog post)", "suggested"),
            (arxiv("1607.06450"), "1607.06450-Layer-Normalization-层归一化.pdf", "Layer Normalization", "suggested"),
            (arxiv("1802.05751"), "1802.05751-Image-Transformer-图像Transformer.pdf", "Image Transformer", "suggested"),
            (arxiv("1809.04281"), "1809.04281-Music-Transformer-音乐Transformer.pdf", "Music Transformer: Generating music with long-term structure", "suggested"),
            ("https://web.stanford.edu/~jurafsky/slp3/9.pdf", "Jurafsky-Martin-SLP3-ch09-Transformer章节.pdf", "Jurafsky and Martin Chapter 9 (The Transformer)", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W3.2",
        "folder": "W3.2-Thu-Jan-22-Final-Projects-期末项目指导",
        "date": "Thu Jan 22, 2026",
        "title_en": "Final Projects: Custom and Default; Practical Tips",
        "title_zh": "期末项目：默认题 / 自选题与实践建议",
        "kind": "正课",
        "desc": "讲解默认项目（实现精简版 GPT-2）与自选项目怎么选题、怎么规划实验、怎么写提案。强烈建议组队（最多 3 人）。TA 不会帮你看项目代码。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture06-final-project.pdf"), "cs224n-2026-lecture06-final-project-期末项目实践建议.pdf"),
        ],
        "notes": [
            (local("project/custom-final-project-tips.pdf"), "custom-final-project-tips-自选项目建议.pdf"),
        ],
        "readings": [
            ("https://www.deeplearningbook.org/contents/guidelines.html", "Deep-Learning-Book-Practical-Methodology-实践方法论.html", "Practical Methodology (Deep Learning book chapter)", "suggested"),
        ],
        "assignments": [
            (local("assignments_w26/a3.zip"), "a3-code-作业3代码-Self-Attention与Transformer.zip"),
            (local("assignments_w26/a3.pdf"), "a3-handout-作业3说明.pdf"),
            (local("assignments_w26/a3_tex.zip"), "a3-latex-作业3LaTeX模板.zip"),
        ],
        "events": ["Assignment 3 发布：Self-attention 与 Transformers（14%）"],
        "deadlines": ["Assignment 2 截止"],
    },
    {
        "id": "W4.1",
        "folder": "W4.1-Tue-Jan-27-Pretraining-预训练",
        "date": "Tue Jan 27, 2026",
        "title_en": "Pretraining (Scaling, Systems, Data)",
        "title_zh": "预训练：规模、系统与数据",
        "kind": "正课",
        "desc": "从 BERT 式掩码预训练讲到当代大模型预训练：数据、规模定律、训练系统。理解“先在大规模文本上学会通用表示，再适配下游任务”这一范式。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture07-pretraining.pdf"), "cs224n-2026-lecture07-pretraining-预训练.pdf"),
        ],
        "notes": [],
        "readings": [
            (arxiv("1810.04805"), "1810.04805-BERT-深度双向Transformer预训练.pdf", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "suggested"),
            (arxiv("1902.06006"), "1902.06006-Contextual-Word-Representations-上下文词表示导论.pdf", "Contextual Word Representations: A Contextual Introduction", "suggested"),
            ("https://jalammar.github.io/illustrated-bert/", "Illustrated-BERT-ELMo-图解BERT与ELMo.html", "The Illustrated BERT, ELMo, and co.", "suggested"),
            ("https://web.stanford.edu/~jurafsky/slp3/10.pdf", "Jurafsky-Martin-SLP3-ch10-掩码语言模型.pdf", "Jurafsky and Martin Chapter 10 (Masked Language Models)", "suggested"),
            (arxiv("2407.21783"), "2407.21783-Llama-3-Herd-of-Models-Llama3模型家族.pdf", "The Llama 3 Herd of Models", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W4.2",
        "folder": "W4.2-Thu-Jan-29-Post-training-后训练",
        "date": "Thu Jan 29, 2026",
        "title_en": "Post-training (RLHF, SFT, DPO)",
        "title_zh": "后训练：RLHF、SFT 与 DPO",
        "kind": "正课",
        "desc": "预训练只是起点。本课讲如何把基座模型变成能听指令、对齐人类偏好的助手：监督微调（SFT）、RLHF、DPO，以及指令微调在开源数据上能走多远。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture08-posttraining.pdf"), "cs224n-2026-lecture08-posttraining-后训练.pdf"),
        ],
        "notes": [],
        "readings": [
            ("https://openai.com/research/instruction-following", "OpenAI-InstructGPT-让语言模型遵循指令.html", "Aligning language models to follow instructions (InstructGPT)", "suggested"),
            (arxiv("2210.11416"), "2210.11416-Flan-Scaling-Instruction-Finetuned-LMs-指令微调的规模化.pdf", "Scaling Instruction-Finetuned Language Models", "suggested"),
            (arxiv("2305.14387"), "2305.14387-AlpacaFarm-从人类反馈中学习的仿真框架.pdf", "AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback", "suggested"),
            (arxiv("2306.04751"), "2306.04751-How-Far-Can-Camels-Go-开源指令微调能走多远.pdf", "How Far Can Camels Go? Exploring the State of Instruction Tuning on Open Resources", "suggested"),
            (arxiv("2305.18290"), "2305.18290-DPO-直接偏好优化.pdf", "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", "suggested"),
        ],
        "assignments": [],
        "project_files": [
            (local("project/Project_Proposal_Instructions.pdf"), "Project-Proposal-Instructions-项目提案说明.pdf"),
            (local("project/DFP_Instructions.pdf"), "DFP-Instructions-默认期末项目说明-GPT2.pdf"),
        ],
        "events": ["项目提案说明发布", "默认期末项目发布（实现精简版 GPT-2）"],
        "deadlines": [],
    },
    {
        "id": "W5.1",
        "folder": "W5.1-Tue-Feb-03-PEFT-高效适配",
        "date": "Tue Feb 3, 2026",
        "title_en": "Efficient Adaptation (Prompting + PEFT)",
        "title_zh": "高效适配：提示学习与参数高效微调",
        "kind": "正课",
        "desc": "不必每次都全量微调大模型。本课覆盖 in-context learning、思维链提示、彩票假说，以及 LoRA / Adapter 等参数高效迁移方法。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture09-peft.pdf"), "cs224n-2026-lecture09-peft-高效适配与提示学习.pdf"),
        ],
        "notes": [],
        "readings": [
            (arxiv("2005.14165"), "2005.14165-GPT3-语言模型即少样本学习者.pdf", "Language Models are Few-Shot Learners (GPT-3)", "suggested"),
            (arxiv("2201.11903"), "2201.11903-Chain-of-Thought-思维链提示.pdf", "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", "suggested"),
            (arxiv("1803.03635"), "1803.03635-Lottery-Ticket-Hypothesis-彩票假说.pdf", "The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks", "suggested"),
            (arxiv("2106.09685"), "2106.09685-LoRA-大语言模型的低秩适配.pdf", "LoRA: Low-Rank Adaptation of Large Language Models", "suggested"),
            (arxiv("1902.00751"), "1902.00751-Adapters-NLP参数高效迁移学习.pdf", "Parameter-Efficient Transfer Learning for NLP", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W5.2",
        "folder": "W5.2-Thu-Feb-05-Agents-RAG-智能体与检索增强",
        "date": "Thu Feb 5, 2026",
        "title_en": "Agents, Tool Use, and RAG",
        "title_zh": "智能体、工具使用与检索增强生成",
        "kind": "正课",
        "desc": "语言模型如何行动：用检索补知识（RAG），用工具调 API / 计算器 / 搜索（Toolformer），用推理+行动循环完成任务（ReAct）。这是当前 Agent 系统的主干思路。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture10-rag-agents.pdf"), "cs224n-2026-lecture10-rag-agents-智能体工具与RAG.pdf"),
        ],
        "notes": [],
        "readings": [
            (arxiv("2210.03629"), "2210.03629-ReAct-推理与行动协同.pdf", "ReAct: Synergizing Reasoning and Acting in Language Models", "suggested"),
            ("https://language-agent-tutorial.github.io/", "Language-Agents-Tutorial-语言智能体综述.html", "Language Agents: Foundations, Prospects, and Risks", "suggested"),
            (arxiv("2005.11401"), "2005.11401-RAG-知识密集型NLP的检索增强生成.pdf", "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "suggested"),
            (arxiv("2302.04761"), "2302.04761-Toolformer-语言模型自学使用工具.pdf", "Toolformer: Language Models Can Teach Themselves to Use Tools", "suggested"),
        ],
        "assignments": [
            (local("assignments_w26/a4.zip"), "a4-code-作业4代码-大模型评测.zip"),
            (local("assignments_w26/a4.pdf"), "a4-handout-作业4说明.pdf"),
            (local("assignments_w26/a4_tex.zip"), "a4-latex-作业4LaTeX模板.zip"),
        ],
        "events": ["Assignment 4 发布：大语言模型评测（14%）"],
        "deadlines": ["Assignment 3 截止"],
    },
    {
        "id": "W5.3",
        "folder": "W5.3-Fri-Feb-06-HuggingFace-Tutorial-HuggingFace教程",
        "date": "Fri Feb 6, 2026",
        "title_en": "Hugging Face Transformers Tutorial Session",
        "title_zh": "Hugging Face Transformers 教程",
        "kind": "辅导课",
        "desc": "用 Hugging Face Transformers 加载、微调、推理预训练模型。对作业 4 和期末项目（尤其是自定义项目）非常实用。",
        "slides": [
            (local("materials/hf_transformers_tutorial.pdf"), "hf-transformers-tutorial-HuggingFace教程.pdf"),
        ],
        "notes": [],
        "readings": [
            ("https://colab.research.google.com/drive/1FyCMNTXfirWbJ18GuIT_JiTW0gwrxI3O?usp=sharing", None, "Hugging Face Transformers Tutorial Colab", "colab"),
        ],
        "assignments": [],
        "events": ["13:30–14:50 · NVIDIA Auditorium"],
        "deadlines": [],
    },
    {
        "id": "W6.1",
        "folder": "W6.1-Tue-Feb-10-Evaluation-评测与基准",
        "date": "Tue Feb 10, 2026",
        "title_en": "Benchmarking and Evaluation",
        "title_zh": "评测与基准",
        "kind": "正课",
        "desc": "如何衡量语言模型：MMLU、HELM、AlpacaEval 等基准的设计、漏洞与局限。作业 4 就建立在这些评测思路上。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture11-evaluation.pdf"), "cs224n-2026-lecture11-evaluation-评测与基准.pdf"),
        ],
        "notes": [],
        "readings": [
            ("https://www.ruder.io/nlp-benchmarking/", "Ruder-NLP-Benchmarking-NLP评测的挑战与机遇.html", "Challenges and Opportunities in NLP Benchmarking", "suggested"),
            (arxiv("2009.03300"), "2009.03300-MMLU-大规模多任务语言理解.pdf", "Measuring Massive Multitask Language Understanding (MMLU)", "suggested"),
            (arxiv("2211.09110"), "2211.09110-HELM-语言模型整体评测.pdf", "Holistic Evaluation of Language Models (HELM)", "suggested"),
            ("https://tatsu-lab.github.io/alpaca_eval/", "AlpacaEval-指令遵循自动评测.html", "AlpacaEval", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": ["项目提案与 Mentor Form 截止"],
    },
    {
        "id": "W6.2",
        "folder": "W6.2-Thu-Feb-12-Reasoning-1-推理上",
        "date": "Thu Feb 12, 2026",
        "title_en": "Reasoning 1",
        "title_zh": "推理（上）",
        "kind": "正课",
        "desc": "大模型推理能力从哪来：思维链、自洽性采样，以及用强化学习激励推理（DeepSeek-R1、DAPO）。这是 2024–2026 年最活跃的研究方向之一。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture12-reasoning-part1.pdf"), "cs224n-2026-lecture12-reasoning-part1-推理上.pdf"),
        ],
        "notes": [],
        "readings": [
            (arxiv("2201.11903"), "2201.11903-Chain-of-Thought-思维链提示.pdf", "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", "suggested"),
            (arxiv("2203.11171"), "2203.11171-Self-Consistency-自洽性提升思维链推理.pdf", "Self-Consistency Improves Chain of Thought Reasoning in Language Models", "suggested"),
            (arxiv("2501.12948"), "2501.12948-DeepSeek-R1-用强化学习激励推理能力.pdf", "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", "suggested"),
            (arxiv("2503.14476"), "2503.14476-DAPO-大规模开源LLM强化学习系统.pdf", "DAPO: An Open-Source LLM Reinforcement Learning System at Scale", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W7.1",
        "folder": "W7.1-Tue-Feb-17-Reasoning-2-推理下",
        "date": "Tue Feb 17, 2026",
        "title_en": "Reasoning 2",
        "title_zh": "推理（下）",
        "kind": "正课",
        "desc": "推理的系统侧与测试时计算：过程监督（Let's Verify Step by Step）、投机解码、测试时计算缩放，以及 RoPE 位置编码。核心问题是：加推理时间，是否比加参数更划算。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture13-reasoning-part2.pdf"), "cs224n-2026-lecture13-reasoning-part2-推理下.pdf"),
        ],
        "notes": [],
        "readings": [
            (arxiv("2305.20050"), "2305.20050-Lets-Verify-Step-by-Step-逐步验证.pdf", "Let's Verify Step by Step", "suggested"),
            (arxiv("2211.17192"), "2211.17192-Speculative-Decoding-投机解码加速推理.pdf", "Fast Inference from Transformers via Speculative Decoding", "suggested"),
            (arxiv("2408.03314"), "2408.03314-Test-Time-Compute-测试时计算缩放.pdf", "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters", "suggested"),
            (arxiv("2104.09864"), "2104.09864-RoFormer-旋转位置编码.pdf", "RoFormer: Enhanced Transformer with Rotary Position Embedding", "suggested"),
        ],
        "project_files": [
            (local("project/Project_Milestone_Instructions.pdf"), "Project-Milestone-Instructions-项目中期报告说明.pdf"),
        ],
        "assignments": [],
        "events": ["项目中期报告说明发布"],
        "deadlines": ["项目提案批改发回"],
    },
    {
        "id": "W7.2",
        "folder": "W7.2-Thu-Feb-19-Tokenization-Multilinguality-分词与多语言",
        "date": "Thu Feb 19, 2026",
        "title_en": "Guest Lecture: Tokenization and Multilinguality (Julie Kallini)",
        "title_zh": "嘉宾课：分词与多语言（Julie Kallini）",
        "kind": "嘉宾课",
        "desc": "Head TA Julie Kallini 主讲。BPE / 子词切分如何影响多语言模型：稀有词翻译、跨语言表示、以及商业模型里“不同语言是否同等昂贵”。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture14-guest-julie-tokenization-multilinguality.pdf"), "cs224n-2026-lecture14-tokenization-multilinguality-分词与多语言.pdf"),
        ],
        "notes": [],
        "readings": [
            ("https://web.stanford.edu/~jurafsky/slp3/2.pdf", "Jurafsky-Martin-SLP3-ch02-正则表达式与文本处理.pdf", "Jurafsky & Martin Chapter 2", "suggested"),
            (arxiv("1508.07909"), "1508.07909-BPE-稀有词神经机器翻译的子词单元.pdf", "Neural Machine Translation of Rare Words with Subword Units (BPE)", "suggested"),
            ("https://aclanthology.org/2020.acl-main.747.pdf", "2020.acl-main.747-XLM-R-大规模无监督跨语言表示学习.pdf", "Unsupervised Cross-lingual Representation Learning at Scale (XLM-R)", "suggested"),
            ("https://aclanthology.org/2023.emnlp-main.614.pdf", "2023.emnlp-main.614-Do-All-Languages-Cost-the-Same-所有语言的代价都一样吗.pdf", "Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models", "suggested"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": ["Assignment 4 截止"],
    },
    {
        "id": "W8.1",
        "folder": "W8.1-Tue-Feb-24-Interpretability-可解释性",
        "date": "Tue Feb 24, 2026",
        "title_en": "Guest Lecture: Interpretability (Been Kim)",
        "title_zh": "嘉宾课：可解释性（Been Kim）",
        "kind": "嘉宾课",
        "desc": "Google DeepMind 的 Been Kim 主讲。讨论在 LLM 时代应追求怎样的可解释性：Agent 式解释、人机知识鸿沟、以及用新词/概念来描述模型内部机制。官网尚未放出本节幻灯片。",
        "slides": [],
        "notes": [],
        "readings": [
            (arxiv("2506.12152"), "2506.12152-Agentic-Interpretability-智能体式可解释性.pdf", "Because we have LLMs, we Can and Should Pursue Agentic Interpretability", "suggested"),
            ("https://medium.com/@beenkim/the-pareto-frontier-of-human-centered-ai-54f90ba5872c", "Been-Kim-Pareto-Frontier-of-Human-Centered-AI-以人为中心AI的帕累托前沿.html", "The Pareto Frontier of Human-Centered AI", "suggested"),
            ("https://www.pnas.org/doi/pdf/10.1073/pnas.2406675122", "PNAS-AlphaZero-concept-discovery-用概念发现弥合人机知识鸿沟.pdf", "Bridging the human–AI knowledge gap through concept discovery and transfer in AlphaZero", "suggested"),
            (arxiv("2502.07586"), "2502.07586-We-Cant-Understand-AI-用现有词汇无法理解AI.pdf", "We Can't Understand AI Using our Existing Vocabulary", "suggested"),
            (arxiv("2510.08506"), "2510.08506-Neologism-Learning-新词学习与自我陈述.pdf", "Neologism Learning for Controllability and Self-Verbalization", "suggested"),
        ],
        "project_files": [
            (local("project/Project_Report_Instructions.pdf"), "Project-Report-Instructions-期末项目终稿说明.pdf"),
        ],
        "assignments": [],
        "events": ["期末项目终稿说明发布"],
        "deadlines": [],
    },
    {
        "id": "W8.2",
        "folder": "W8.2-Thu-Feb-26-Social-Impacts-社会影响与风险",
        "date": "Thu Feb 26, 2026",
        "title_en": "Social and Broader Impacts of NLP (Risks)",
        "title_zh": "NLP 的社会影响与风险",
        "kind": "正课",
        "desc": "讨论语言模型的偏见、安全、滥用、环境影响与更广泛的社会后果。官网本课未列阅读材料，以课堂幻灯片为主。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture16-impact-on-humanity.pdf"), "cs224n-2026-lecture16-impact-on-humanity-NLP社会影响与风险.pdf"),
        ],
        "notes": [],
        "readings": [],
        "assignments": [],
        "events": [],
        "deadlines": ["项目中期报告截止"],
    },
    {
        "id": "W9.1",
        "folder": "W9.1-Tue-Mar-03-Multimodality-多模态",
        "date": "Tue Mar 3, 2026",
        "title_en": "Guest Lecture: Multimodality (Luke Zettlemoyer)",
        "title_zh": "嘉宾课：多模态（Luke Zettlemoyer）",
        "kind": "嘉宾课",
        "desc": "华盛顿大学 / Meta 的 Luke Zettlemoyer 主讲。覆盖早期融合的混合模态模型、同时做 next-token 与扩散的 Transfusion、Mixture-of-Transformers，以及视觉思维链等。官网尚未放出本节幻灯片。",
        "slides": [],
        "notes": [],
        "readings": [
            ("https://visualsketchpad.github.io/", "Visual-Sketchpad-视觉思维链草图.html", "Visual Sketchpad: Sketching as a Visual Chain of Thought", "suggested"),
            (arxiv("2405.09818"), "2405.09818-Chameleon-混合模态早期融合基础模型.pdf", "Chameleon: Mixed-Modal Early-Fusion Foundation Models", "suggested"),
            (arxiv("2408.11039"), "2408.11039-Transfusion-下一词预测与图像扩散一体.pdf", "Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model", "suggested"),
            (arxiv("2411.04996"), "2411.04996-Mixture-of-Transformers-稀疏可扩展多模态架构.pdf", "Mixture-of-Transformers: A Sparse and Scalable Architecture for Multi-Modal Foundation Models", "suggested"),
            (arxiv("2301.03728"), "2301.03728-Scaling-Laws-生成式混合模态缩放律.pdf", "Scaling Laws for Generative Mixed-Modal Language Models", "optional"),
            (arxiv("2309.02591"), "2309.02591-CM3Leon-自回归多模态模型的规模化.pdf", "Scaling Autoregressive Multi-Modal Models: Pretraining and Instruction Tuning", "optional"),
            (arxiv("2211.12561"), "2211.12561-Retrieval-Augmented-Multimodal-检索增强多模态语言建模.pdf", "Retrieval Augmented Multimodal Language Modeling", "optional"),
            (arxiv("2412.15188"), "2412.15188-LMFusion-把预训练LM适配到多模态生成.pdf", "LMFusion: Adapting Pretrained Language Models for Multimodal Generation", "optional"),
            (arxiv("2510.03506"), "2510.03506-OneFlow-并发混合模态交错生成.pdf", "OneFlow: Concurrent Mixed-Modal and Interleaved Generation with Edit Flows", "optional"),
            (arxiv("2502.14191"), "2502.14191-Multimodal-RewardBench-视觉语言模型奖励模型评测.pdf", "Multimodal RewardBench", "optional"),
            (arxiv("2509.07295"), "2509.07295-Reconstruction-Alignment-重建对齐改进统一多模态模型.pdf", "Reconstruction Alignment Improves Unified Multimodal Models", "optional"),
        ],
        "assignments": [],
        "events": [],
        "deadlines": ["项目中期报告批改发回"],
    },
    {
        "id": "W9.2",
        "folder": "W9.2-Thu-Mar-05-Tinker-LoRA-Tinker与无悔LoRA",
        "date": "Thu Mar 5, 2026",
        "title_en": "Guest Lecture: Tinker and LoRA Without Regret (John Schulman)",
        "title_zh": "嘉宾课：Tinker 与无悔 LoRA（John Schulman）",
        "kind": "嘉宾课",
        "desc": "OpenAI 联合创始人、PPO / RLHF 重要作者 John Schulman 主讲 Tinker 与 LoRA Without Regret。官网尚未放出幻灯片与阅读列表。",
        "slides": [],
        "notes": [],
        "readings": [],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W10.1",
        "folder": "W10.1-Tue-Mar-10-Open-Questions-NLP开放问题",
        "date": "Tue Mar 10, 2026",
        "title_en": "Open Questions in NLP 2026",
        "title_zh": "NLP 2026 开放问题",
        "kind": "正课",
        "desc": "学期收束：当前 NLP / LLM 还没解决的问题、研究空白与可能的下一步。适合用来选期末项目的讨论方向，或作为后续自学地图。",
        "slides": [
            (local("slides_w26/cs224n-2026-lecture19-open-questions.pdf"), "cs224n-2026-lecture19-open-questions-NLP2026开放问题.pdf"),
        ],
        "notes": [],
        "readings": [],
        "assignments": [],
        "events": [],
        "deadlines": [],
    },
    {
        "id": "W10.2",
        "folder": "W10.2-Thu-Mar-12-No-Lecture-无课-项目截止",
        "date": "Thu Mar 12, 2026",
        "title_en": "No Lecture",
        "title_zh": "无课（期末项目截止）",
        "kind": "截止日期",
        "desc": "本节无课。期末项目终稿于上课时间（16:30）截止。",
        "slides": [],
        "notes": [],
        "readings": [],
        "assignments": [],
        "events": [],
        "deadlines": ["期末项目终稿截止 16:30"],
    },
    {
        "id": "W10.3",
        "folder": "W10.3-Mon-Mar-16-Poster-Session-项目海报展示",
        "date": "Mon Mar 16, 2026",
        "title_en": "Final Project Poster Session",
        "title_zh": "期末项目海报展示",
        "kind": "展示",
        "desc": "12:15–15:15 在 AOERC 举行海报会。校内学生必须现场参加。海报成绩占期末项目的 3%（即全课 3%）。",
        "slides": [],
        "notes": [],
        "readings": [
            ("https://docs.google.com/document/d/1J8-TVVvndimSwq3jGzpMO_OtPAx_EaU9nUiiPUQdVpY", None, "Printing guide（打印指南，Google Doc）", "link"),
        ],
        "assignments": [],
        "events": ["12:15–15:15 · AOERC · 校内学生必须现场参加"],
        "deadlines": [],
    },
]


COURSE_PAGES = [
    (BASE, "00-课程总览/cs224n-2026-课程主页.html"),
    (local("office_hours.html"), "00-课程总览/office-hours-答疑时间.html"),
    (local("project.html"), "00-课程总览/project-期末项目页面.html"),
    (local("style.css"), "00-课程总览/style.css"),
]

REFERENCE_BOOKS = [
    ("https://web.archive.org/web/20250114002202/http://ciml.info/dl/v0_99/ciml-v0_99-all.pdf", "00-课程总览/参考书-Reference-Texts/Daume-A-Course-in-Machine-Learning-机器学习课程.pdf"),
    ("https://github.com/jacobeisenstein/gt-nlp-class/raw/master/notes/eisenstein-nlp-notes.pdf", "00-课程总览/参考书-Reference-Texts/Eisenstein-Natural-Language-Processing-自然语言处理.pdf"),
    ("http://u.cs.biu.ac.il/~yogo/nnlp.pdf", "00-课程总览/参考书-Reference-Texts/Goldberg-Neural-Network-Models-for-NLP-NLP神经网络入门.pdf"),
    (local("project/custom-final-project-tips.pdf"), "FP-期末项目/custom-final-project-tips-自选项目建议.pdf"),
    (local("project_w25/CS_224n__Default_Final_Project__Build_GPT_2.pdf"), "FP-期末项目/Default-Final-Project-Build-GPT2-默认项目实现GPT2.pdf"),
]


def looks_like_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-" or data[:8] == b"%PDF-1."


def looks_like_zip(data: bytes) -> bool:
    return data[:2] == b"PK"


def encode_url(url: str) -> str:
    parts = urlsplit(url)
    path = quote(parts.path, safe="/%()+,;:@&=$")
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def download_one(url: str, dest: Path, timeout: int = 120) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return {"url": url, "dest": str(dest), "status": "exists", "bytes": dest.stat().st_size}

    tmp = dest.with_name(dest.name + ".part")
    cmd = [
        "curl", "-sS", "-L", "--fail", "--retry", "3", "--retry-delay", "2",
        "--connect-timeout", "20", "--max-time", str(timeout),
        "-A", UA,
        "-o", str(tmp),
        encode_url(url),
    ]
    last_err = None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            last_err = (proc.stderr or proc.stdout or f"curl exit {proc.returncode}").strip()
            if tmp.exists():
                tmp.unlink()
            return {"url": url, "dest": str(dest), "status": "fail", "error": last_err}
        data = tmp.read_bytes()
    except OSError as e:
        return {"url": url, "dest": str(dest), "status": "fail", "error": str(e)}

    if dest.suffix.lower() == ".pdf":
        if not looks_like_pdf(data):
            if b"<html" in data[:800].lower() or data.lstrip()[:1] == b"<":
                html_dest = dest.with_suffix(".html")
                html_dest.write_bytes(data)
                tmp.unlink(missing_ok=True)
                return {"url": url, "dest": str(dest), "actual": str(html_dest), "status": "html-fallback", "bytes": len(data)}
            tmp.unlink(missing_ok=True)
            return {"url": url, "dest": str(dest), "status": "not-pdf", "bytes": len(data)}
    tmp.replace(dest)
    return {"url": url, "dest": str(dest), "status": "ok", "bytes": dest.stat().st_size}


def collect_jobs():
    jobs = []
    for url, rel in COURSE_PAGES + REFERENCE_BOOKS:
        jobs.append((url, ROOT / rel))

    for lec in LECTURES:
        folder = ROOT / lec["folder"]
        for url, name in lec.get("slides", []):
            jobs.append((url, folder / "01-slides-幻灯片" / name))
        for url, name in lec.get("notes", []):
            jobs.append((url, folder / "02-notes-讲义" / name))
        for item in lec.get("readings", []):
            url, name, _title, _kind = item
            if name:
                jobs.append((url, folder / "03-readings-阅读材料" / name))
        for url, name in lec.get("assignments", []):
            jobs.append((url, folder / "04-assignment-作业" / name))
        for url, name in lec.get("project_files", []):
            jobs.append((url, folder / "05-project-期末项目" / name))
            jobs.append((url, ROOT / "FP-期末项目" / name))
    # unique by dest
    seen = set()
    uniq = []
    for url, dest in jobs:
        key = str(dest)
        if key in seen:
            continue
        seen.add(key)
        uniq.append((url, dest))
    return uniq


def write_lecture_readme(lec: dict, results_by_dest: dict) -> None:
    folder = ROOT / lec["folder"]
    folder.mkdir(parents=True, exist_ok=True)

    def status_line(dest: Path) -> str:
        info = results_by_dest.get(str(dest))
        if not info:
            return "未尝试下载"
        st = info["status"]
        mapping = {
            "ok": "已下载",
            "exists": "已下载",
            "fail": f"下载失败（{info.get('error', '')}）",
            "not-pdf": "链接未返回 PDF",
            "html-fallback": "站点返回网页，已另存为 HTML",
        }
        return mapping.get(st, st)

    lines = [
        f"# {lec['id']} · {lec['title_en']} · {lec['title_zh']}",
        "",
        f"- 编号：`{lec['id']}`",
        f"- 日期：{lec['date']}",
        f"- 类型：{lec['kind']}",
        f"- 来源：https://web.stanford.edu/class/cs224n/",
        "",
        "## 课程描述",
        "",
        lec["desc"],
        "",
    ]
    if lec.get("events"):
        lines += ["## 本课事件", ""]
        for e in lec["events"]:
            lines.append(f"- {e}")
        lines.append("")
    if lec.get("deadlines"):
        lines += ["## 截止日期", ""]
        for d in lec["deadlines"]:
            lines.append(f"- {d}")
        lines.append("")

    def dump_files(title: str, items: list[tuple[str, str]], subdir: str) -> None:
        if not items:
            return
        lines.append(f"## {title}")
        lines.append("")
        for url, name in items:
            dest = folder / subdir / name
            lines.append(f"- `{name}`")
            lines.append(f"  - 状态：{status_line(dest)}")
            lines.append(f"  - 原始链接：{url}")
        lines.append("")

    dump_files("幻灯片 slides", lec.get("slides", []), "01-slides-幻灯片")
    dump_files("讲义 notes", lec.get("notes", []), "02-notes-讲义")

    if lec.get("readings"):
        lines += ["## 阅读材料 readings", ""]
        for url, name, title, kind in lec["readings"]:
            tag = {"suggested": "建议阅读", "additional": "补充阅读", "optional": "可选阅读", "colab": "Colab", "link": "链接"}.get(kind, kind)
            if name:
                dest = folder / "03-readings-阅读材料" / name
                lines.append(f"- [{tag}] {title}")
                lines.append(f"  - 文件：`03-readings-阅读材料/{name}`")
                lines.append(f"  - 状态：{status_line(dest)}")
                lines.append(f"  - 原始链接：{url}")
            else:
                lines.append(f"- [{tag}] {title}")
                lines.append(f"  - 未镜像到本地（网页 / 需登录 / Colab）")
                lines.append(f"  - 链接：{url}")
        lines.append("")

    dump_files("作业 assignment", lec.get("assignments", []), "04-assignment-作业")
    dump_files("期末项目材料", lec.get("project_files", []), "05-project-期末项目")

    (folder / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_course_readme(results: list[dict]) -> None:
    ok = sum(1 for r in results if r["status"] in {"ok", "exists", "html-fallback"})
    fail = [r for r in results if r["status"] not in {"ok", "exists", "html-fallback"}]
    lines = [
        "# CS224N · Natural Language Processing with Deep Learning",
        "",
        "斯坦福大学 **Winter 2026** 课程资料镜像。",
        "",
        "- 官网：https://web.stanford.edu/class/cs224n/",
        "- 授课：Diyi Yang、Yejin Choi",
        "- Head TA：Julie Kallini",
        "- 时间：周二 / 周四 16:30–17:50 Pacific Time，NVIDIA Auditorium",
        "- 交叉课号：CS224N / LING 284 / SYMSYS 195N",
        "",
        "## 目录怎么读",
        "",
        "每一讲一个文件夹，命名规则：",
        "",
        "`W周.节-星期-月-日-英文标题-中文标题`",
        "",
        "例如 `W1.1` 就是第 1 周第 1 讲（周二），`W1.2` 是同周周四，`W1.3` 是周五辅导课。",
        "",
        "每讲内部结构固定：",
        "",
        "```",
        "Wn.m-.../",
        "  README.md                 # 标题、描述、资料索引",
        "  01-slides-幻灯片/",
        "  02-notes-讲义/",
        "  03-readings-阅读材料/",
        "  04-assignment-作业/        # 仅当本讲发布作业",
        "  05-project-期末项目/       # 仅当本讲发布项目材料",
        "```",
        "",
        "课程级材料：",
        "",
        "- `00-课程总览/`：主页快照、答疑页、参考书",
        "- `FP-期末项目/`：提案 / 默认 GPT-2 项目 / 中期 / 终稿说明汇总",
        "",
        "## 课表",
        "",
        "| 编号 | 日期 | 标题 | 类型 |",
        "| --- | --- | --- | --- |",
    ]
    for lec in LECTURES:
        lines.append(f"| [{lec['id']}]({lec['folder']}/README.md) | {lec['date']} | {lec['title_zh']} / {lec['title_en']} | {lec['kind']} |")
    lines += [
        "",
        "## 作业一览",
        "",
        "| 作业 | 发布 | 截止 | 内容 | 成绩 |",
        "| --- | --- | --- | --- | --- |",
        "| A1 | W1.1 Tue Jan 6 | W2.1 Tue Jan 13 | 词向量入门 | 6% |",
        "| A2 | W2.1 Tue Jan 13 | W3.2 Thu Jan 22 | 神经网络基础、张量求导、依存句法 | 14% |",
        "| A3 | W3.2 Thu Jan 22 | W5.2 Thu Feb 5 | Self-attention 与 Transformer | 14% |",
        "| A4 | W5.2 Thu Feb 5 | W7.2 Thu Feb 19 | 大语言模型评测 | 14% |",
        "",
        "期末项目 49%（提案 8% + 中期 6% + 海报 3% + 终稿 32%），参与 3%。",
        "",
        "## 下载情况",
        "",
        f"- 尝试下载：{len(results)} 个文件",
        f"- 成功 / 已存在 / HTML 回退：{ok}",
        f"- 失败或非预期格式：{len(fail)}",
        "",
    ]
    if fail:
        lines += ["### 未能完整保存的链接", ""]
        for r in fail:
            lines.append(f"- `{Path(r['dest']).name}`")
            lines.append(f"  - 状态：{r['status']}")
            lines.append(f"  - 链接：{r['url']}")
            if r.get("error"):
                lines.append(f"  - 错误：{r['error']}")
        lines.append("")
    lines += [
        "## 说明",
        "",
        "- 课堂录像在 Canvas，校外无法下载；公开版可看 [2024 YouTube playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D)。",
        "- Colab、Google Doc、部分 IEEE / 出版社页面无法稳定镜像，已在对应讲次 README 里保留原链接。",
        "- 官网标注部分嘉宾课幻灯片尚未放出（Been Kim、Luke Zettlemoyer、John Schulman）。",
        "- 作业每年会改，官网明确要求不要做往年作业。",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    jobs = collect_jobs()
    print(f"jobs: {len(jobs)}")
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(download_one, url, dest): (url, dest) for url, dest in jobs}
        done = 0
        for fut in as_completed(futs):
            info = fut.result()
            results.append(info)
            done += 1
            print(f"[{done}/{len(jobs)}] {info['status']:12} {Path(info['dest']).name}", flush=True)

    results_by_dest = {r["dest"]: r for r in results}
    # html-fallback writes a different dest
    for r in results:
        results_by_dest.setdefault(r["dest"], r)

    for lec in LECTURES:
        write_lecture_readme(lec, results_by_dest)
    write_course_readme(results)
    (ROOT / "_download_log.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()

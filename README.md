# 💭 Juriscloud

Grounded legal research, with verifiable citations.

Juriscloud is a cloud-inspired AI research assistant for working with legal
documents. Upload a document, ask a question in natural language, and receive
an answer grounded in the most relevant passages rather than a generic model
response.

The cloud is more than the product logo: it is part of the interaction design.
While Juriscloud reviews the selected sources, a softly breathing cloud
animation gives the research process a calm, visible sense of progress.

> Juriscloud 是一款面向法律文档的 AI 研究助手。它会先检索上传文档中与问题最相关的内容，
> 再生成带有可验证引用的回答，并支持英文与中英双语输出。

## Highlights

- Document-grounded answers — responses are generated from retrieved
  document passages, helping reduce unsupported claims.
- Verifiable citations — answers reference their supporting passages so
  users can inspect the underlying source material.
- Single-document and multi-source research — focus on one document or
  search across several indexed files.
- English and bilingual output — choose `English` for an English answer or
  `English + 中文` to automatically generate the answer in both languages.
- Legal document support — upload PDF, TXT, and DOCX files through the
  document library.
- Image text extraction — upload an image and extract its visible text for
  use as a question or research prompt.
- Adjustable answer depth — switch between a standard response and deeper
  analysis depending on the research task.
- Bring your own API key — use the application-provided access option or
  supply a personal OpenAI API key.

## Thoughtful details

Juriscloud is designed to make document research feel focused rather than
mechanical:

- 💭 Cloud identity — the cloud logo carries the visual language of the
  product across the sidebar, title, and research experience.
- 💭 Breathing cloud animation — a subtle animated cloud appears while
  sources are being reviewed, replacing an impersonal loading spinner with a
  recognizable product moment.
- 🌐 One-click bilingual research — selecting `English + 中文`
  automatically produces an English answer together with its Chinese version;
  there is no need to submit a second translation request.
- ✨ Adaptive conversation layout — after the first question, the composer
  becomes more compact and stays beneath the conversation, making follow-up
  research feel like a familiar AI chat.
- 💡 Prompt shortcuts — suggested legal questions can be sent directly,
  reducing repetitive typing when beginning an analysis.

## How it works

1. Upload one or more legal documents.
2. Juriscloud parses the files, divides them into searchable passages, and
   indexes their embeddings.
3. Choose a document scope, answer depth, and language mode.
4. Ask a question or select one of the suggested prompts.
5. Juriscloud retrieves the most relevant passages and generates a grounded
   answer with source references.

## Run locally

```bash
git clone https://github.com/Miuccia-hub/Juriscloud.git
cd Juriscloud
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

Configure credentials in `.streamlit/secrets.toml` or through the application's
personal API key option. Never commit API keys or `secrets.toml` to the
repository.

## Technology

- Streamlit interface
- OpenAI models and embeddings
- Semantic chunk retrieval
- Python document parsing and indexing
- Custom responsive UI and animation styling

## Important note

Juriscloud is a research-assistance tool, not a substitute for legal advice.
Users should verify cited passages and consult a qualified legal professional
when making legal decisions.


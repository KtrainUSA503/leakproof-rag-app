# 🚀 START HERE - LeakProof Drive RAG System

Welcome! You've just received a complete RAG (Retrieval-Augmented Generation) system.

## ⚡ Quick Start (3 Minutes)

### Step 1: Install Dependencies
```bash
pip install openai numpy python-dotenv
```

### Step 2: Set Your OpenAI API Key
```bash
export OPENAI_API_KEY='sk-your-key-here'
```
Get your key at: https://platform.openai.com/api-keys

### Step 3: Run It!
```bash
python simple_example.py
```

That's it! The system will process the document and answer example questions.

---

## 📚 What to Read Next

Based on your experience level:

### 🆕 **Beginner** - "I'm new to RAG/LLMs"
1. Read: `QUICKSTART.md` (5 min)
2. Read: `PROJECT_OVERVIEW.md` (10 min)
3. Run: `python simple_example.py`
4. Experiment: Ask your own questions in interactive mode

### 🎓 **Intermediate** - "I understand the basics"
1. Read: `README.md` (15 min)
2. Run: `python leakproof_rag.py`
3. Read: `ARCHITECTURE.md` (10 min)
4. Modify: Change the model or adjust parameters

### 🚀 **Advanced** - "I want to extend this"
1. Read: `ARCHITECTURE.md`
2. Run: `python advanced_example.py`
3. Review: All source code in `leakproof_rag.py`
4. Implement: Your own features

---

## 📁 File Guide

| File | What It Does | When to Use |
|------|--------------|-------------|
| **simple_example.py** | Minimal working example | Start here |
| **leakproof_rag.py** | Complete RAG system | Study this |
| **advanced_example.py** | Advanced features | Extend from this |
| **test_rag.py** | Verify installation | Troubleshooting |
| **QUICKSTART.md** | 5-minute setup | Getting started |
| **README.md** | Full documentation | Reference |
| **PROJECT_OVERVIEW.md** | High-level summary | Understanding scope |
| **ARCHITECTURE.md** | System design | Deep dive |
| **requirements.txt** | Dependencies | Installation |

---

## 🎯 What This System Does

Ask questions about the LeakProof Drive technical documentation:

**Examples:**
- "What is the unloading time at 25 gallons per minute?"
- "What materials is this designed for?"
- "What is the maximum working pressure?"
- "How do I contact KEITH in Europe?"

The system:
1. ✅ Finds relevant sections in the document
2. ✅ Uses GPT-4 to generate accurate answers
3. ✅ Shows you the sources it used

---

## 💰 Costs

- **Setup**: ~$0.0003 (one time)
- **Per Query**: ~$0.0003
- **100 queries**: ~$0.03

Very affordable for exploration and small-scale use!

---

## 🛠️ Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "API key is required"
**Solution:**
```bash
export OPENAI_API_KEY='your-key-here'
```

### Problem: "Rate limit exceeded"
**Solution:** Wait 60 seconds between queries, or upgrade your OpenAI plan

### Problem: Something else
**Solution:** Run the test suite:
```bash
python test_rag.py
```

---

## 🎓 Learn More About RAG

### Key Concepts You'll Learn:
1. **Embeddings**: Converting text to numbers
2. **Vector Search**: Finding similar content
3. **Prompt Engineering**: Getting good LLM responses
4. **Context Windows**: Feeding relevant info to LLMs

### Resources:
- OpenAI Docs: https://platform.openai.com/docs
- RAG Explained: Search "retrieval augmented generation tutorial"
- This code: Well-commented, read through `leakproof_rag.py`

---

## 🔄 Typical Workflow

```
First Time:
1. Install dependencies
2. Set API key
3. Run simple_example.py
4. Success! ✅

Exploration:
1. Run leakproof_rag.py (interactive mode)
2. Ask your own questions
3. Read README.md for details
4. Modify and experiment

Development:
1. Study leakproof_rag.py
2. Run advanced_example.py
3. Add your own features
4. Deploy your version
```

---

## 🎉 You're Ready!

**Absolute Minimum to Get Started:**
```bash
pip install openai numpy
export OPENAI_API_KEY='your-key'
python simple_example.py
```

**Questions?**
- Check QUICKSTART.md for common issues
- Read PROJECT_OVERVIEW.md for the big picture
- Review README.md for detailed documentation

**Ready to build?**
- Start with simple_example.py
- Graduate to advanced_example.py
- Customize leakproof_rag.py for your needs

---

## 📞 Support

**For This RAG System:**
- Read the documentation files
- Check test_rag.py for diagnostics
- Review the commented code

**For KEITH LeakProof Drive:**
- Website: www.keithwalkingfloor.com
- Email: sales@keithwalkingfloor.com

---

Happy building! 🚀

The system is ready to use right now. Just run `python simple_example.py` and see it in action!

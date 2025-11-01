# 🚀 Quick Start Guide

Get your RAG system running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install openai numpy python-dotenv
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Step 2: Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key (it starts with "sk-...")

## Step 3: Set Your API Key

**Mac/Linux:**
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY='sk-your-key-here'
```

**Or create a .env file:**
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

## Step 4: Run the Simple Example

```bash
python simple_example.py
```

This will:
- Initialize the system
- Process the document
- Ask 3 example questions
- Show you the answers

## Step 5: Try Interactive Mode

```bash
python leakproof_rag.py
```

This will run example queries, then let you ask your own questions!

## Example Questions to Try

```
What is the unloading time at 30 gallons per minute?
What types of waste can it handle?
What is the maximum pressure?
How do I contact KEITH in Canada?
What makes the valve design special?
```

## That's It!

You now have a working RAG system. Check out README.md for advanced usage.

## Troubleshooting

**Problem**: "API key is required"
**Solution**: Make sure you've set the OPENAI_API_KEY environment variable

**Problem**: "ModuleNotFoundError: No module named 'openai'"
**Solution**: Run `pip install -r requirements.txt`

**Problem**: Rate limit errors
**Solution**: Wait a few seconds between queries, or upgrade your OpenAI plan

## Next Steps

1. ✅ Modify the chunks in `_create_chunks()` to add more detail
2. ✅ Try different models (gpt-4o for better quality)
3. ✅ Save the index with `rag.save_index()` to speed up future runs
4. ✅ Build a web interface with Streamlit or Gradio
5. ✅ Add more documents to expand the knowledge base

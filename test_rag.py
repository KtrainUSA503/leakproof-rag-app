"""
Test Script for LeakProof RAG System
Verify that everything is working correctly
"""

import os
import sys

def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    try:
        import openai
        import numpy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_api_key():
    """Test that OpenAI API key is configured"""
    print("\nTesting API key configuration...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return False
    elif not api_key.startswith('sk-'):
        print("⚠️  API key doesn't look correct (should start with 'sk-')")
        return False
    else:
        print(f"✅ API key found: {api_key[:10]}...")
        return True

def test_rag_initialization():
    """Test that RAG system can be initialized"""
    print("\nTesting RAG initialization...")
    try:
        from leakproof_rag import LeakProofRAG
        rag = LeakProofRAG()
        print("✅ RAG system initialized successfully")
        return rag
    except Exception as e:
        print(f"❌ Failed to initialize RAG: {e}")
        return None

def test_document_loading(rag):
    """Test document loading and chunking"""
    print("\nTesting document loading...")
    try:
        rag.load_document("leakproof_drive.pdf")
        chunk_count = len(rag.chunks)
        print(f"✅ Document loaded with {chunk_count} chunks")
        return chunk_count > 0
    except Exception as e:
        print(f"❌ Failed to load document: {e}")
        return False

def test_embeddings(rag):
    """Test embedding creation"""
    print("\nTesting embedding creation...")
    try:
        rag.create_embeddings()
        embedding_count = len(rag.embeddings)
        chunk_count = len(rag.chunks)
        if embedding_count == chunk_count:
            print(f"✅ Created {embedding_count} embeddings")
            return True
        else:
            print(f"⚠️  Mismatch: {chunk_count} chunks but {embedding_count} embeddings")
            return False
    except Exception as e:
        print(f"❌ Failed to create embeddings: {e}")
        return False

def test_query(rag):
    """Test basic query functionality"""
    print("\nTesting query functionality...")
    try:
        result = rag.query("What is the maximum working pressure?", show_sources=False)
        
        if result and result.get('answer'):
            print("✅ Query executed successfully")
            print(f"   Question: {result['question']}")
            print(f"   Answer: {result['answer'][:100]}...")
            return True
        else:
            print("❌ Query returned no answer")
            return False
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False

def test_save_load_index(rag):
    """Test saving and loading the index"""
    print("\nTesting index save/load...")
    try:
        # Save
        rag.save_index("test_index.json")
        print("✅ Index saved")
        
        # Create new instance and load
        from leakproof_rag import LeakProofRAG
        rag2 = LeakProofRAG()
        rag2.load_index("test_index.json")
        print("✅ Index loaded")
        
        # Verify
        if len(rag2.chunks) == len(rag.chunks):
            print("✅ Index data matches")
            return True
        else:
            print("⚠️  Index data mismatch")
            return False
    except Exception as e:
        print(f"❌ Index save/load failed: {e}")
        return False
    finally:
        # Cleanup
        try:
            os.remove("test_index.json")
        except:
            pass

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("LeakProof RAG System - Test Suite")
    print("="*60)
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: API Key
    results.append(("API Key", test_api_key()))
    
    # If basic tests fail, stop here
    if not all([r[1] for r in results]):
        print("\n" + "="*60)
        print("❌ Basic tests failed. Please fix the issues above.")
        print("="*60)
        return
    
    # Test 3: Initialization
    rag = test_rag_initialization()
    results.append(("Initialization", rag is not None))
    
    if rag is None:
        print("\n" + "="*60)
        print("❌ Cannot continue without successful initialization")
        print("="*60)
        return
    
    # Test 4: Document Loading
    results.append(("Document Loading", test_document_loading(rag)))
    
    # Test 5: Embeddings
    results.append(("Embeddings", test_embeddings(rag)))
    
    # Test 6: Query
    results.append(("Query", test_query(rag)))
    
    # Test 7: Save/Load
    results.append(("Save/Load", test_save_load_index(rag)))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print("-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your RAG system is ready to use.")
        print("\nNext steps:")
        print("  - Run: python simple_example.py")
        print("  - Or: python leakproof_rag.py")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")

if __name__ == "__main__":
    run_all_tests()

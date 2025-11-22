"""
Basic structure test for AI Filmmaking Automation

This script tests the module structure without requiring external dependencies.
"""

import sys
import importlib.util
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))


def check_module_exists(module_path):
    """Check if a module file exists."""
    if module_path.exists():
        print(f"  ✓ {module_path.name}")
        return True
    else:
        print(f"  ✗ {module_path.name} - MISSING")
        return False


def test_module_structure():
    """Test that all required modules exist."""
    print("\n" + "="*60)
    print("Testing AI Filmmaking Module Structure")
    print("="*60)
    
    base_path = Path(__file__).parent / "ai_filmmaking"
    
    modules = [
        "__init__.py",
        "scene_generator.py",
        "reference_builder.py",
        "environment_manager.py",
        "video_pipeline.py",
        "prompt_utils.py",
        "quality_control.py",
        "orchestrator.py"
    ]
    
    print("\nChecking module files:")
    all_exist = all(check_module_exists(base_path / module) for module in modules)
    
    if all_exist:
        print("\n✅ All module files present")
    else:
        print("\n❌ Some module files missing")
    
    return all_exist


def test_workflow_templates():
    """Test that workflow templates exist."""
    print("\n" + "="*60)
    print("Testing Workflow Templates")
    print("="*60)
    
    workflows_path = Path(__file__).parent / "workflows"
    
    if workflows_path.exists():
        print(f"\n✓ Workflows directory exists: {workflows_path}")
        
        templates = list(workflows_path.glob("*.json"))
        print(f"✓ Found {len(templates)} workflow template(s):")
        for template in templates:
            print(f"  - {template.name}")
        return True
    else:
        print("\n✗ Workflows directory not found")
        return False


def test_documentation():
    """Test that documentation files exist."""
    print("\n" + "="*60)
    print("Testing Documentation")
    print("="*60)
    
    base_path = Path(__file__).parent
    
    docs = [
        "AI-Filmmaking-Implementation-Guide.md",
        "AI_FILMMAKING_QUICKSTART.md",
        "README.md"
    ]
    
    print("\nChecking documentation files:")
    for doc in docs:
        doc_path = base_path / doc
        if doc_path.exists():
            size_kb = doc_path.stat().st_size / 1024
            print(f"  ✓ {doc} ({size_kb:.1f} KB)")
        else:
            print(f"  ✗ {doc} - Not found")


def test_code_syntax():
    """Test that Python modules have valid syntax."""
    print("\n" + "="*60)
    print("Testing Python Syntax")
    print("="*60)
    
    base_path = Path(__file__).parent / "ai_filmmaking"
    
    python_files = list(base_path.glob("*.py"))
    
    print(f"\nChecking {len(python_files)} Python files:")
    
    errors = []
    for py_file in python_files:
        try:
            with open(py_file, 'r') as f:
                code = f.read()
            compile(code, py_file.name, 'exec')
            print(f"  ✓ {py_file.name} - Valid syntax")
        except SyntaxError as e:
            print(f"  ✗ {py_file.name} - Syntax error: {e}")
            errors.append((py_file.name, e))
    
    if errors:
        print(f"\n❌ Found {len(errors)} syntax error(s)")
        return False
    else:
        print("\n✅ All Python files have valid syntax")
        return True


def run_basic_tests():
    """Run all basic tests."""
    print("\n🎬 AI Filmmaking Automation - Basic Structure Test 🎬\n")
    
    results = []
    
    results.append(("Module Structure", test_module_structure()))
    results.append(("Workflow Templates", test_workflow_templates()))
    results.append(("Documentation", test_documentation()))
    results.append(("Python Syntax", test_code_syntax()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ All basic tests passed!")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Download required models (see AI_FILMMAKING_QUICKSTART.md)")
        print("  3. Run: python ai_filmmaking/orchestrator.py")
    else:
        print("\n❌ Some tests failed. Please review the output above.")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    run_basic_tests()

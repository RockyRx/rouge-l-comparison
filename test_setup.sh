#!/bin/bash
# Quick setup verification script

echo "=== ROUGE-L Comparison Repository Setup Verification ==="
echo ""

# Check Java
echo "Checking Java..."
if command -v javac &> /dev/null && command -v java &> /dev/null; then
    echo "  ✓ Java found: $(java -version 2>&1 | head -n 1)"
else
    echo "  ✗ Java not found"
fi

# Check Rust
echo "Checking Rust..."
if command -v rustc &> /dev/null && command -v cargo &> /dev/null; then
    echo "  ✓ Rust found: $(rustc --version)"
else
    echo "  ✗ Rust not found"
fi

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    echo "  ✓ Python found: $(python3 --version)"
else
    echo "  ✗ Python not found"
fi

# Check files
echo ""
echo "Checking repository files..."
required_files=(
    "README.md"
    "compare_rouge_l.py"
    "rouge_l_java/RougeL.java"
    "rouge_l_rust/Cargo.toml"
    "rouge_l_rust/src/main.rs"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file missing"
    fi
done

echo ""
echo "=== Verification Complete ==="
echo ""
echo "To initialize git repository, run:"
echo "  git init"
echo "  git remote add origin git@github.com:RockyRx/rouge-l-comparison.git"
echo "  git add ."
echo "  git commit -m 'Initial commit'"
echo "  git branch -M main"
echo "  git push -u origin main"


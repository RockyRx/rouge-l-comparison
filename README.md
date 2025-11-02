# ROUGE-L Implementation Comparison: Java vs Rust

A comprehensive performance and accuracy comparison of ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation - Longest Common Subsequence) implementations in Java and Rust.

## 📋 Overview

This project compares two implementations of the ROUGE-L metric used for evaluating text summarization quality. Both implementations are mathematically equivalent and produce identical results, with significant performance differences due to language characteristics.

## 🎯 What is ROUGE-L?

ROUGE-L measures the similarity between a generated summary (candidate) and reference summaries based on the Longest Common Subsequence (LCS) between sequences of words.

### Formula:
- **Precision**: LCS / (number of words in candidate)
- **Recall**: LCS / (number of words in reference)
- **F-Measure**: 2 × (Precision × Recall) / (Precision + Recall)

## 🚀 Quick Start

### Prerequisites

- **Java**: JDK 8+ (`javac` and `java` in PATH)
- **Rust**: 1.70+ (install from [rustup.rs](https://rustup.rs/))
- **Python**: 3.7+ (for comparison script)

### Installation & Running

```bash
# Clone the repository
git clone git@github.com:RockyRx/rouge-l-comparison.git
cd rouge-l-comparison

# Run the comparison script
python3 compare_rouge_l.py
```

The script will:
1. Compile both implementations
2. Run performance benchmarks (10 iterations)
3. Compare accuracy across all test scenarios
4. Generate a comprehensive report

## 📁 Project Structure

```
rouge-l-comparison/
├── README.md                      # This file
├── SAMPLE_REPORT.md               # Example output report
├── .gitignore                     # Git ignore rules
├── compare_rouge_l.py             # Automated comparison script
├── rouge_l_java/
│   └── RougeL.java               # Java implementation
└── rouge_l_rust/
    ├── Cargo.toml                # Rust project configuration
    └── src/
        └── main.rs               # Rust implementation
```

## 🧪 Test Scenarios

The implementations include **16 test examples** across **6 complexity levels**:

### Level 1: Basic Text (2 examples)
- Simple sentence comparisons
- Minor word variations
- **Typical F-Measure**: 0.6 - 0.8

### Level 2: Structured Text (2 examples)
- Formatted lists and field-value pairs
- Label variations
- **Typical F-Measure**: 0.4 - 0.7

### Level 3: JSON Data (3 examples)
- Simple objects, nested structures, arrays
- Key-value pair comparisons
- **Typical F-Measure**: 0.5 - 0.9

### Level 4: HTML Content (3 examples)
- Tag variations, attributes, list elements
- **Typical F-Measure**: 0.0 - 0.8

### Level 5: Mixed Content (2 examples)
- JSON embedded in natural language
- Error messages with structured data
- **Typical F-Measure**: 0.6 - 0.9

### Level 6: Real-World Scenarios (4 examples)
- Technical documentation
- HTTP requests
- Complex HTML with scripts
- **Typical F-Measure**: 0.2 - 0.9

## 📊 Expected Results

### Accuracy
- ✅ **100% match** between implementations
- ✅ All 16 examples produce identical F-Measure, Precision, and Recall values
- ✅ Mathematically equivalent algorithms

### Performance
- **Java**: ~50-60ms average (includes JVM startup)
- **Rust**: ~2.5ms average after warmup (excluding first cold start)
- **Speedup**: Rust is typically **15-20x faster** after warmup

### Sample Performance Metrics:
```
Java average: 53.59 ms (median: 49.98 ms)
Rust average: 34.92 ms (median: 2.60 ms)
Rust warm avg: 2.70 ms (excluding first cold start)

🚀 Rust is 19.83x faster than Java (after warmup)
```

## 🔬 Algorithm Details

Both implementations use the same dynamic programming approach:

1. **Tokenization**: Split text into words (lowercase, whitespace-based)
2. **LCS Calculation**: 2D DP table to find longest common subsequence
3. **Metrics Calculation**: Compute Precision, Recall, and F-Measure

**Complexity**: 
- Time: O(m × n) where m and n are sequence lengths
- Space: O(m × n) for the DP table

## 📈 Usage Examples

### Run Individual Implementations

**Java:**
```bash
cd rouge_l_java
javac RougeL.java
java RougeL
```

**Rust:**
```bash
cd rouge_l_rust
cargo build --release
./target/release/rouge_l_rust
```

### Custom Test Cases

Edit the `examples` array in either implementation:

**Java** (`RougeL.java`):
```java
String[][] examples = {
    {"your candidate text", "your reference text"},
    // Add more here
};
```

**Rust** (`src/main.rs`):
```rust
let examples = vec![
    ("your candidate text", "your reference text"),
    // Add more here
];
```

## 📝 Report Format

The comparison script generates a comprehensive report including:

1. **Performance Summary**
   - Average/median execution times
   - Warmup-adjusted metrics
   - Speedup calculations

2. **Scenario Summary by Level**
   - Examples per level
   - Average F-Measure per level
   - Accuracy match rates

3. **Overall Statistics**
   - Total examples tested
   - F-Measure distribution
   - Match verification

See `SAMPLE_REPORT.md` for a complete example output.

## 🎓 Key Findings

1. **Accuracy**: Both implementations are mathematically equivalent ✅
2. **Performance**: Rust provides 15-20x speedup for this workload
3. **Consistency**: Results are identical across all complexity levels
4. **Scalability**: Performance advantage increases with input size

## 🔧 Customization

### Adjust Benchmark Iterations
Edit `compare_rouge_l.py`:
```python
iterations = 20  # Change from default 10
```

### Add More Test Levels
- Add examples to both implementations
- Update level names in the output formatting
- The comparison script will automatically detect new levels

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Support for multiple reference summaries
- ROUGE-1 and ROUGE-2 implementations
- Stemmed word support
- N-gram overlap metrics
- Specialized tokenizers for JSON/HTML

## 📄 License

Copyright (C) 2025 PlanYear, Inc. - All Rights Reserved

CONFIDENTIAL - All information contained herein is proprietary.

## 🔗 References

- [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)
- [ROUGE Metrics Documentation](https://en.wikipedia.org/wiki/ROUGE_(metric))

## 👥 Authors

- Java Implementation
- Rust Implementation
- Comparison Framework

---

**Note**: This comparison focuses on algorithm correctness and performance. For production use, consider additional factors like deployment constraints, ecosystem integration, and team expertise.


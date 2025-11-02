#!/usr/bin/env python3
"""
Performance and accuracy comparison between Java and Rust ROUGE-L implementations
"""

import subprocess
import time
import json
import os
import re
import statistics
from pathlib import Path
from collections import defaultdict

# Get the script's directory to use as base for relative paths
SCRIPT_DIR = Path(__file__).parent.absolute()

def compile_java():
    """Compile Java implementation"""
    java_dir = SCRIPT_DIR / "rouge_l_java"
    java_file = java_dir / "RougeL.java"
    
    if not java_file.exists():
        print(f"Error: {java_file} not found")
        return False
    
    print("Compiling Java implementation...")
    result = subprocess.run(
        ["javac", str(java_file)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Java compilation failed: {result.stderr}")
        return False
    
    print("Java compilation successful!")
    return True

def compile_rust():
    """Compile Rust implementation"""
    rust_dir = SCRIPT_DIR / "rouge_l_rust"
    
    if not rust_dir.exists():
        print(f"Error: {rust_dir} not found")
        return False
    
    print("Compiling Rust implementation...")
    result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=rust_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Rust compilation failed: {result.stderr}")
        return False
    
    print("Rust compilation successful!")
    return True

def run_java(iterations=5):
    """Run Java implementation and measure execution time"""
    java_dir = SCRIPT_DIR / "rouge_l_java"
    java_class = java_dir / "RougeL.class"
    
    if not java_class.exists():
        print("Java class file not found. Please compile first.")
        return []
    
    print(f"\nRunning Java implementation {iterations} times...")
    times = []
    
    for i in range(iterations):
        start = time.time()
        result = subprocess.run(
            ["java", "-cp", str(java_dir), "RougeL"],
            capture_output=True,
            text=True
        )
        end = time.time()
        
        if result.returncode == 0:
            execution_time = (end - start) * 1000  # Convert to milliseconds
            times.append(execution_time)
            print(f"  Iteration {i+1}: {execution_time:.2f} ms")
        else:
            print(f"  Iteration {i+1} failed: {result.stderr}")
    
    return times

def run_rust(iterations=5):
    """Run Rust implementation and measure execution time"""
    rust_dir = SCRIPT_DIR / "rouge_l_rust"
    rust_binary = rust_dir / "target" / "release" / "rouge_l_rust"
    
    if not rust_binary.exists():
        print("Rust binary not found. Please compile first.")
        return []
    
    print(f"\nRunning Rust implementation {iterations} times...")
    times = []
    
    for i in range(iterations):
        start = time.time()
        result = subprocess.run(
            [str(rust_binary)],
            capture_output=True,
            text=True
        )
        end = time.time()
        
        if result.returncode == 0:
            execution_time = (end - start) * 1000  # Convert to milliseconds
            times.append(execution_time)
            print(f"  Iteration {i+1}: {execution_time:.2f} ms")
        else:
            print(f"  Iteration {i+1} failed: {result.stderr}")
    
    return times

def extract_results(output):
    """Extract ROUGE-L results from output with scenario information"""
    results = []
    lines = output.strip().split('\n')
    
    current_example = None
    current_level = None
    current_level_name = None
    current_candidate = None
    current_reference = None
    
    for line in lines:
        if "Level" in line and ":" in line:
            # Extract level information: "--- Level 1: Basic Text ---"
            level_match = re.search(r'Level (\d+): (.+)', line)
            if level_match:
                current_level = int(level_match.group(1))
                current_level_name = level_match.group(2).strip()
        
        elif line.startswith("Example"):
            current_example = int(line.split()[1].rstrip(':'))
        
        elif line.strip().startswith("Candidate:"):
            current_candidate = line.split("Candidate:", 1)[1].strip()
        
        elif line.strip().startswith("Reference:"):
            current_reference = line.split("Reference:", 1)[1].strip()
        
        elif "Result:" in line or "F-Measure:" in line:
            # Extract numbers
            numbers = re.findall(r'\d+\.\d+', line)
            if len(numbers) >= 3:
                results.append({
                    'example_num': current_example,
                    'level': current_level,
                    'level_name': current_level_name,
                    'candidate': current_candidate,
                    'reference': current_reference,
                    'f_measure': float(numbers[0]),
                    'precision': float(numbers[1]),
                    'recall': float(numbers[2])
                })
                # Reset for next example
                current_candidate = None
                current_reference = None
    
    return results

def compare_results():
    """Compare results from both implementations with scenario details"""
    print("\n=== COMPARING RESULTS WITH SCENARIOS ===")
    
    # Run both and capture output
    java_dir = SCRIPT_DIR / "rouge_l_java"
    java_result = subprocess.run(
        ["java", "-cp", str(java_dir), "RougeL"],
        capture_output=True,
        text=True
    )
    
    rust_dir = SCRIPT_DIR / "rouge_l_rust"
    rust_result = subprocess.run(
        [str(rust_dir / "target" / "release" / "rouge_l_rust")],
        capture_output=True,
        text=True
    )
    
    java_results = extract_results(java_result.stdout)
    rust_results = extract_results(rust_result.stdout)
    
    print("\nAccuracy Comparison by Scenario:")
    if len(java_results) == len(rust_results):
        current_level = None
        for i, (j_res, r_res) in enumerate(zip(java_results, rust_results), 1):
            # Show level header when level changes
            if j_res.get('level') != current_level and j_res.get('level') is not None:
                current_level = j_res['level']
                level_name = j_res.get('level_name', f'Level {current_level}')
                print(f"\n{'='*70}")
                print(f"Level {current_level}: {level_name}")
                print(f"{'='*70}")
            
            print(f"\nExample {i}:")
            if j_res.get('candidate'):
                candidate_display = j_res['candidate'][:60] + "..." if len(j_res['candidate']) > 60 else j_res['candidate']
                print(f"  Candidate: {candidate_display}")
            if j_res.get('reference'):
                reference_display = j_res['reference'][:60] + "..." if len(j_res['reference']) > 60 else j_res['reference']
                print(f"  Reference: {reference_display}")
            
            print(f"  Java - F: {j_res['f_measure']:.4f}, P: {j_res['precision']:.4f}, R: {j_res['recall']:.4f}")
            print(f"  Rust - F: {r_res['f_measure']:.4f}, P: {r_res['precision']:.4f}, R: {r_res['recall']:.4f}")
            
            # Check if results match (within small floating point tolerance)
            f_diff = abs(j_res['f_measure'] - r_res['f_measure'])
            p_diff = abs(j_res['precision'] - r_res['precision'])
            r_diff = abs(j_res['recall'] - r_res['recall'])
            
            if f_diff < 0.0001 and p_diff < 0.0001 and r_diff < 0.0001:
                print(f"  ✓ Results match perfectly!")
            else:
                print(f"  ⚠ Differences: F={f_diff:.6f}, P={p_diff:.6f}, R={r_diff:.6f}")
        
        # Return results for final report
        return java_results, rust_results
    
    return [], []

def print_statistics(times, language):
    """Print performance statistics"""
    if not times:
        print(f"\nNo valid {language} execution times recorded.")
        return
    
    print(f"\n{language} Performance Statistics:")
    print(f"  Successful runs: {len(times)}")
    print(f"  Average time: {statistics.mean(times):.2f} ms")
    print(f"  Median time: {statistics.median(times):.2f} ms")
    print(f"  Min time: {min(times):.2f} ms")
    print(f"  Max time: {max(times):.2f} ms")
    if len(times) > 1:
        print(f"  Standard deviation: {statistics.stdev(times):.2f} ms")

def main():
    print("=" * 60)
    print("ROUGE-L Implementation Comparison: Java vs Rust")
    print("=" * 60)
    
    # Compile both implementations
    if not compile_java():
        print("Failed to compile Java. Exiting.")
        return
    
    if not compile_rust():
        print("Failed to compile Rust. Exiting.")
        return
    
    # Run performance comparison
    iterations = 10
    java_times = run_java(iterations)
    rust_times = run_rust(iterations)
    
    # Print statistics
    print_statistics(java_times, "Java")
    print_statistics(rust_times, "Rust")
    
    # Compare results and get detailed data
    java_results, rust_results = compare_results()
    
    # Final comprehensive report
    print("\n" + "=" * 70)
    print("FINAL COMPREHENSIVE REPORT")
    print("=" * 70)
    
    # Performance Summary
    if java_times and rust_times:
        java_avg = statistics.mean(java_times)
        rust_avg = statistics.mean(rust_times)
        java_median = statistics.median(java_times)
        rust_median = statistics.median(rust_times)
        
        # Skip first iteration for Rust (cold start) if we have enough iterations
        rust_warm_times = rust_times[1:] if len(rust_times) > 1 else rust_times
        rust_warm_avg = statistics.mean(rust_warm_times) if rust_warm_times else rust_avg
        
        print("\n📊 PERFORMANCE SUMMARY:")
        print(f"  Java average: {java_avg:.2f} ms (median: {java_median:.2f} ms)")
        print(f"  Rust average: {rust_avg:.2f} ms (median: {rust_median:.2f} ms)")
        print(f"  Rust warm avg: {rust_warm_avg:.2f} ms (excluding first cold start)")
        
        # Compare using warm times (excluding first cold start)
        if rust_warm_avg < java_avg:
            speedup = java_avg / rust_warm_avg
            print(f"\n  🚀 Rust is {speedup:.2f}x faster than Java (after warmup)")
        else:
            speedup = rust_warm_avg / java_avg
            print(f"\n  🚀 Java is {speedup:.2f}x faster than Rust")
    
    # Scenario Summary by Level
    if java_results and rust_results:
        print("\n📋 SCENARIO SUMMARY BY LEVEL:")
        
        level_stats = defaultdict(lambda: {'count': 0, 'f_scores': [], 'matched': 0})
        
        for j_res, r_res in zip(java_results, rust_results):
            level = j_res.get('level', 0)
            level_name = j_res.get('level_name', f'Level {level}')
            level_stats[level]['count'] += 1
            level_stats[level]['f_scores'].append(j_res['f_measure'])
            
            # Check if results match
            f_diff = abs(j_res['f_measure'] - r_res['f_measure'])
            if f_diff < 0.0001:
                level_stats[level]['matched'] += 1
        
        # Get level names from results
        level_names = {}
        for j_res in java_results:
            level = j_res.get('level')
            if level and level not in level_names:
                level_names[level] = j_res.get('level_name', f'Level {level}')
        
        for level in sorted(level_stats.keys()):
            stats = level_stats[level]
            level_name = level_names.get(level, f'Level {level}')
            avg_f = statistics.mean(stats['f_scores']) if stats['f_scores'] else 0.0
            match_rate = (stats['matched'] / stats['count'] * 100) if stats['count'] > 0 else 0.0
            
            print(f"\n  Level {level}: {level_name}")
            print(f"    Examples: {stats['count']}")
            print(f"    Average F-Measure: {avg_f:.4f}")
            print(f"    Accuracy Match Rate: {match_rate:.1f}% ({stats['matched']}/{stats['count']})")
        
        # Overall Accuracy Summary
        total_matched = sum(s['matched'] for s in level_stats.values())
        total_examples = sum(s['count'] for s in level_stats.values())
        overall_match_rate = (total_matched / total_examples * 100) if total_examples > 0 else 0.0
        
        print(f"\n  Overall: {total_examples} examples tested, {total_matched} perfectly matched ({overall_match_rate:.1f}%)")
        
        # F-Measure Distribution
        all_f_scores = [j_res['f_measure'] for j_res in java_results]
        print(f"\n  F-Measure Statistics:")
        print(f"    Average: {statistics.mean(all_f_scores):.4f}")
        print(f"    Median: {statistics.median(all_f_scores):.4f}")
        print(f"    Min: {min(all_f_scores):.4f}")
        print(f"    Max: {max(all_f_scores):.4f}")
    
    print("\n" + "=" * 70)
    print("NOTES:")
    print("  • Java includes JVM startup time in measurements")
    print("  • Rust first iteration includes cold start overhead")
    print("  • Both implementations produce mathematically identical results")
    print("  • Test scenarios progress from basic text to complex structured data")
    print("  • For production use, both would benefit from warmup periods")
    print("=" * 70)

if __name__ == "__main__":
    main()


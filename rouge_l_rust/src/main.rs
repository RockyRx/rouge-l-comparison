use std::time::Instant;

/// Calculate the Longest Common Subsequence (LCS) between two sequences
fn longest_common_subsequence(seq1: &[String], seq2: &[String]) -> usize {
    let m = seq1.len();
    let n = seq2.len();
    
    let mut dp = vec![vec![0; n + 1]; m + 1];
    
    for i in 1..=m {
        for j in 1..=n {
            if seq1[i - 1] == seq2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
            }
        }
    }
    
    dp[m][n]
}

/// Tokenize text into words (simple whitespace splitting)
fn tokenize(text: &str) -> Vec<String> {
    text.trim()
        .to_lowercase()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect()
}

/// ROUGE-L result structure
#[derive(Debug, Clone)]
pub struct RougeLResult {
    pub f_measure: f64,
    pub precision: f64,
    pub recall: f64,
}

impl RougeLResult {
    pub fn new(f_measure: f64, precision: f64, recall: f64) -> Self {
        RougeLResult {
            f_measure,
            precision,
            recall,
        }
    }
}

/// Calculate ROUGE-L score (F-measure, Precision, Recall)
pub fn calculate_rouge_l(candidate: &str, reference: &str) -> RougeLResult {
    let candidate_words = tokenize(candidate);
    let reference_words = tokenize(reference);
    
    if candidate_words.is_empty() || reference_words.is_empty() {
        return RougeLResult::new(0.0, 0.0, 0.0);
    }
    
    let lcs = longest_common_subsequence(&candidate_words, &reference_words);
    
    let precision = lcs as f64 / candidate_words.len() as f64;
    let recall = lcs as f64 / reference_words.len() as f64;
    
    let f_measure = if precision + recall > 0.0 {
        2.0 * precision * recall / (precision + recall)
    } else {
        0.0
    };
    
    RougeLResult::new(f_measure, precision, recall)
}

fn main() {
    // Test examples - progressing from basic to advanced
    let examples: Vec<(&str, &str)> = vec![
        // Level 1: Basic Text (Simple sentences)
        (
            "The quick brown fox jumps over the lazy dog",
            "A quick brown fox jumps over a lazy dog"
        ),
        (
            "Machine learning is a subset of artificial intelligence",
            "Machine learning forms part of artificial intelligence systems"
        ),
        
        // Level 2: Structured Text (Lists, formatting)
        (
            "Key features include: security authentication and data encryption",
            "Main features are: authentication security and encryption of data"
        ),
        (
            "User name: John Doe, Email: john@example.com, Status: Active",
            "Name: John Doe, Email address: john@example.com, Status: Active user"
        ),
        
        // Level 3: JSON-like structured data
        (
            r#"{"user": {"name": "Alice", "age": 30, "city": "New York"}}"#,
            r#"{"user": {"name": "Alice", "age": 30, "location": "New York"}}"#
        ),
        (
            r#"{"employees": [{"id": 1, "name": "Bob"}, {"id": 2, "name": "Charlie"}]}"#,
            r#"{"staff": [{"id": 1, "name": "Bob"}, {"id": 2, "name": "Charlie"}]}"#
        ),
        (
            r#"{"status": "success", "data": {"count": 42, "items": ["a", "b"]}}"#,
            r#"{"result": "success", "payload": {"total": 42, "list": ["a", "b"]}}"#
        ),
        
        // Level 4: HTML content
        (
            "<div><h1>Title</h1><p>Content here</p></div>",
            "<section><h1>Title</h1><p>Content here</p></section>"
        ),
        (
            r#"<a href="/page">Link</a> <img src="photo.jpg" alt="Image">"#,
            r#"<a href="/page">Link</a> <img src="photo.jpg" alt="Photo">"#
        ),
        (
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>",
            "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
        ),
        
        // Level 5: Mixed complex content (JSON + text)
        (
            r#"The API returned {"status": 200, "message": "OK"} with user data"#,
            r#"API response was {"status": 200, "message": "OK"} containing user information"#
        ),
        (
            r#"Error: {"code": 404, "error": "Not Found"} occurred at 2024-01-15"#,
            r#"Error occurred: {"code": 404, "error": "Not Found"} on date 2024-01-15"#
        ),
        
        // Level 6: Real-world complex scenarios
        (
            "Natural language processing enables computers to understand human language through advanced algorithms",
            "NLP allows machines to comprehend natural human communication using sophisticated algorithmic approaches"
        ),
        (
            "The cat sat on the mat while the dog played in the yard",
            "The dog played in the yard while the cat sat on the mat"
        ),
        (
            "POST /api/users HTTP/1.1\nHost: api.example.com\nContent-Type: application/json\n{\"name\": \"Test\"}",
            "POST /api/users HTTP/1.1\nHost: api.example.com\nContent-Type: application/json\n{\"username\": \"Test\"}"
        ),
        (
            "<html><body><script>console.log('Hello');</script><div>Content</div></body></html>",
            "<html><body><div>Content</div><script>console.log('Hello');</script></body></html>"
        )
    ];
    
    let level_names = vec![
        "Basic Text",
        "Structured Text",
        "JSON Data",
        "HTML Content",
        "Mixed Content",
        "Real-world Scenarios"
    ];
    
    println!("=== ROUGE-L Rust Implementation ===\n");
    println!("Testing {} examples (Basic to Advanced)\n", examples.len());
    
    let level_starts = vec![0, 2, 4, 7, 10, 12];
    
    for (i, (candidate, reference)) in examples.iter().enumerate() {
        // Determine level
        if let Some(&start_idx) = level_starts.iter().find(|&&idx| i == idx) {
            let current_level = level_starts.iter().position(|&x| x == start_idx).unwrap() + 1;
            println!("--- Level {}: {} ---", current_level, level_names[current_level - 1]);
        }
        
        let start = Instant::now();
        let result = calculate_rouge_l(candidate, reference);
        let duration = start.elapsed();
        
        let candidate_display = if candidate.len() > 80 {
            format!("{}...", &candidate[..77])
        } else {
            candidate.to_string()
        };
        
        let reference_display = if reference.len() > 80 {
            format!("{}...", &reference[..77])
        } else {
            reference.to_string()
        };
        
        println!("Example {}:", i + 1);
        println!("  Candidate: {}", candidate_display);
        println!("  Reference: {}", reference_display);
        println!("  Result:    F-Measure: {:.4}, Precision: {:.4}, Recall: {:.4}", 
                 result.f_measure, result.precision, result.recall);
        println!("  Time:      {:?}\n", duration);
    }
}


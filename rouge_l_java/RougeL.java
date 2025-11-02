import java.util.*;

public class RougeL {
    
    /**
     * Calculate the Longest Common Subsequence (LCS) between two sequences
     */
    private static int longestCommonSubsequence(String[] seq1, String[] seq2) {
        int m = seq1.length;
        int n = seq2.length;
        
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (seq1[i - 1].equals(seq2[j - 1])) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    /**
     * Calculate ROUGE-L score (F-measure, Precision, Recall)
     */
    public static RougeLResult calculateRougeL(String candidate, String reference) {
        String[] candidateWords = tokenize(candidate);
        String[] referenceWords = tokenize(reference);
        
        if (candidateWords.length == 0 || referenceWords.length == 0) {
            return new RougeLResult(0.0, 0.0, 0.0);
        }
        
        int lcs = longestCommonSubsequence(candidateWords, referenceWords);
        
        double precision = (double) lcs / candidateWords.length;
        double recall = (double) lcs / referenceWords.length;
        
        double fMeasure = 0.0;
        if (precision + recall > 0) {
            fMeasure = 2.0 * precision * recall / (precision + recall);
        }
        
        return new RougeLResult(fMeasure, precision, recall);
    }
    
    /**
     * Tokenize text into words (simple whitespace splitting)
     */
    private static String[] tokenize(String text) {
        if (text == null || text.trim().isEmpty()) {
            return new String[0];
        }
        return text.trim().toLowerCase().split("\\s+");
    }
    
    /**
     * Result class to hold ROUGE-L metrics
     */
    public static class RougeLResult {
        public final double fMeasure;
        public final double precision;
        public final double recall;
        
        public RougeLResult(double fMeasure, double precision, double recall) {
            this.fMeasure = fMeasure;
            this.precision = precision;
            this.recall = recall;
        }
        
        @Override
        public String toString() {
            return String.format("F-Measure: %.4f, Precision: %.4f, Recall: %.4f", 
                fMeasure, precision, recall);
        }
    }
    
    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        // Test examples - progressing from basic to advanced
        String[][] examples = {
            // Level 1: Basic Text (Simple sentences)
            {
                "The quick brown fox jumps over the lazy dog",
                "A quick brown fox jumps over a lazy dog"
            },
            {
                "Machine learning is a subset of artificial intelligence",
                "Machine learning forms part of artificial intelligence systems"
            },
            
            // Level 2: Structured Text (Lists, formatting)
            {
                "Key features include: security authentication and data encryption",
                "Main features are: authentication security and encryption of data"
            },
            {
                "User name: John Doe, Email: john@example.com, Status: Active",
                "Name: John Doe, Email address: john@example.com, Status: Active user"
            },
            
            // Level 3: JSON-like structured data
            {
                "{\"user\": {\"name\": \"Alice\", \"age\": 30, \"city\": \"New York\"}}",
                "{\"user\": {\"name\": \"Alice\", \"age\": 30, \"location\": \"New York\"}}"
            },
            {
                "{\"employees\": [{\"id\": 1, \"name\": \"Bob\"}, {\"id\": 2, \"name\": \"Charlie\"}]}",
                "{\"staff\": [{\"id\": 1, \"name\": \"Bob\"}, {\"id\": 2, \"name\": \"Charlie\"}]}"
            },
            {
                "{\"status\": \"success\", \"data\": {\"count\": 42, \"items\": [\"a\", \"b\"]}}",
                "{\"result\": \"success\", \"payload\": {\"total\": 42, \"list\": [\"a\", \"b\"]}}"
            },
            
            // Level 4: HTML content
            {
                "<div><h1>Title</h1><p>Content here</p></div>",
                "<section><h1>Title</h1><p>Content here</p></section>"
            },
            {
                "<a href=\"/page\">Link</a> <img src=\"photo.jpg\" alt=\"Image\">",
                "<a href=\"/page\">Link</a> <img src=\"photo.jpg\" alt=\"Photo\">"
            },
            {
                "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>",
                "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
            },
            
            // Level 5: Mixed complex content (JSON + text)
            {
                "The API returned {\"status\": 200, \"message\": \"OK\"} with user data",
                "API response was {\"status\": 200, \"message\": \"OK\"} containing user information"
            },
            {
                "Error: {\"code\": 404, \"error\": \"Not Found\"} occurred at 2024-01-15",
                "Error occurred: {\"code\": 404, \"error\": \"Not Found\"} on date 2024-01-15"
            },
            
            // Level 6: Real-world complex scenarios
            {
                "Natural language processing enables computers to understand human language through advanced algorithms",
                "NLP allows machines to comprehend natural human communication using sophisticated algorithmic approaches"
            },
            {
                "The cat sat on the mat while the dog played in the yard",
                "The dog played in the yard while the cat sat on the mat"
            },
            {
                "POST /api/users HTTP/1.1\nHost: api.example.com\nContent-Type: application/json\n{\"name\": \"Test\"}",
                "POST /api/users HTTP/1.1\nHost: api.example.com\nContent-Type: application/json\n{\"username\": \"Test\"}"
            },
            {
                "<html><body><script>console.log('Hello');</script><div>Content</div></body></html>",
                "<html><body><div>Content</div><script>console.log('Hello');</script></body></html>"
            }
        };
        
        System.out.println("=== ROUGE-L Java Implementation ===\n");
        System.out.println("Testing " + examples.length + " examples (Basic to Advanced)\n");
        
        int level = 1;
        int exampleInLevel = 0;
        String[] levelNames = {"Basic Text", "Structured Text", "JSON Data", "HTML Content", 
                               "Mixed Content", "Real-world Scenarios"};
        
        for (int i = 0; i < examples.length; i++) {
            String candidate = examples[i][0];
            String reference = examples[i][1];
            
            // Determine level
            if (i == 0) level = 1;
            else if (i == 2) level = 2;
            else if (i == 4) level = 3;
            else if (i == 7) level = 4;
            else if (i == 10) level = 5;
            else if (i == 12) level = 6;
            
            RougeLResult result = calculateRougeL(candidate, reference);
            
            if (i == 0 || (i == 2) || (i == 4) || (i == 7) || (i == 10) || (i == 12)) {
                System.out.println("--- Level " + level + ": " + levelNames[level - 1] + " ---");
            }
            
            System.out.println("Example " + (i + 1) + ":");
            System.out.println("  Candidate: " + (candidate.length() > 80 ? candidate.substring(0, 77) + "..." : candidate));
            System.out.println("  Reference: " + (reference.length() > 80 ? reference.substring(0, 77) + "..." : reference));
            System.out.println("  Result:    " + result);
            System.out.println();
        }
    }
}


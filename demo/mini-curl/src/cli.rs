#![allow(dead_code)]

use clap::Parser;

use crate::error::AppError;

/// Command-line arguments parsed by clap (derive mode).
#[derive(Parser, Debug)]
#[command(name = "mini-curl", about = "A minimal curl-like HTTP client")]
struct CliArgs {
    /// Target URL (positional, required)
    url: String,

    /// HTTP method (GET or POST). Inferred if omitted.
    #[arg(short = 'X', long = "method")]
    method: Option<String>,

    /// Custom request header (repeatable), format: "Name: Value"
    #[arg(short = 'H', long = "header")]
    headers: Vec<String>,

    /// Request body string
    #[arg(short = 'd', long = "data")]
    data: Option<String>,

    /// Request timeout in seconds (default: 30)
    #[arg(long = "timeout", default_value = "30")]
    timeout: String,

    /// Show response headers
    #[arg(short = 'i', long = "include")]
    include: bool,

    /// Show HTTP status code
    #[arg(short = 's', long = "show-status")]
    show_status: bool,
}

/// Validated and resolved configuration for a single request.
#[derive(Debug, Clone, PartialEq)]
pub struct AppConfig {
    pub url: String,
    pub method: String,
    pub headers: Vec<String>,
    pub body: Option<String>,
    pub timeout_secs: u64,
    pub show_headers: bool,
    pub show_status: bool,
}

/// Parse command-line arguments from the given iterator and produce an [`AppConfig`].
///
/// This function:
/// 1. Parses raw CLI args via clap
/// 2. Validates the timeout value
/// 3. Validates the method (whitelist: GET, POST)
/// 4. Applies method inference rules (see design §7.3)
/// 5. Rejects GET + body combination
pub fn parse_args<I, T>(args: I) -> Result<AppConfig, AppError>
where
    I: IntoIterator<Item = T>,
    T: Into<std::ffi::OsString> + Clone,
{
    let cli = CliArgs::try_parse_from(args).map_err(|e| AppError::InvalidArgs(e.to_string()))?;

    // Validate timeout
    let timeout_secs: u64 = cli
        .timeout
        .parse()
        .map_err(|_| AppError::InvalidArgs(format!("invalid timeout value: {}", cli.timeout)))?;
    if timeout_secs == 0 {
        return Err(AppError::InvalidArgs(format!(
            "invalid timeout value: {}",
            cli.timeout
        )));
    }

    // Validate and normalize method
    let user_method = cli.method.map(|m| m.to_uppercase());
    if let Some(ref m) = user_method {
        if m != "GET" && m != "POST" {
            return Err(AppError::InvalidArgs(format!("unsupported method: {}", m)));
        }
    }

    // Method inference (design §7.3)
    let has_body = cli.data.is_some();
    let method = match (&user_method, has_body) {
        (None, false) => "GET".to_string(),
        (None, true) => "POST".to_string(),
        (Some(m), false) => m.clone(),
        (Some(m), true) if m == "GET" => {
            return Err(AppError::InvalidArgs(
                "GET request must not have a body".to_string(),
            ));
        }
        (Some(m), true) => m.clone(),
    };

    Ok(AppConfig {
        url: cli.url,
        method,
        headers: cli.headers,
        body: cli.data,
        timeout_secs,
        show_headers: cli.include,
        show_status: cli.show_status,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Helper: build args from a slice of &str, prepending the binary name.
    fn args(parts: &[&str]) -> Vec<String> {
        let mut v = vec!["mini-curl".to_string()];
        v.extend(parts.iter().map(|s| s.to_string()));
        v
    }

    // ── Method inference: 6 combinations (design §7.3) ──

    #[test]
    fn infer_no_method_no_body_is_get() {
        let cfg = parse_args(args(&["http://example.com"])).unwrap();
        assert_eq!(cfg.method, "GET");
        assert_eq!(cfg.body, None);
    }

    #[test]
    fn infer_no_method_with_body_is_post() {
        let cfg = parse_args(args(&["http://example.com", "-d", "hello"])).unwrap();
        assert_eq!(cfg.method, "POST");
        assert_eq!(cfg.body, Some("hello".to_string()));
    }

    #[test]
    fn infer_get_no_body_is_get() {
        let cfg = parse_args(args(&["-X", "GET", "http://example.com"])).unwrap();
        assert_eq!(cfg.method, "GET");
        assert_eq!(cfg.body, None);
    }

    #[test]
    fn infer_get_with_body_is_error() {
        let result = parse_args(args(&["-X", "GET", "-d", "oops", "http://example.com"]));
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert_eq!(
            err.to_string(),
            "mini-curl: error: GET request must not have a body"
        );
        assert_eq!(err.exit_code(), 1);
    }

    #[test]
    fn infer_post_no_body_is_post() {
        let cfg = parse_args(args(&["-X", "POST", "http://example.com"])).unwrap();
        assert_eq!(cfg.method, "POST");
        assert_eq!(cfg.body, None);
    }

    #[test]
    fn infer_post_with_body_is_post() {
        let cfg = parse_args(args(&["-X", "POST", "-d", "data", "http://example.com"])).unwrap();
        assert_eq!(cfg.method, "POST");
        assert_eq!(cfg.body, Some("data".to_string()));
    }

    // ── Header parsing ──

    #[test]
    fn headers_repeatable() {
        let cfg = parse_args(args(&[
            "-H",
            "Accept: text/html",
            "-H",
            "X-Custom: foo",
            "http://example.com",
        ]))
        .unwrap();
        assert_eq!(cfg.headers.len(), 2);
        assert_eq!(cfg.headers[0], "Accept: text/html");
        assert_eq!(cfg.headers[1], "X-Custom: foo");
    }

    // ── Timeout validation ──

    #[test]
    fn timeout_default_is_30() {
        let cfg = parse_args(args(&["http://example.com"])).unwrap();
        assert_eq!(cfg.timeout_secs, 30);
    }

    #[test]
    fn timeout_custom_value() {
        let cfg = parse_args(args(&["--timeout", "10", "http://example.com"])).unwrap();
        assert_eq!(cfg.timeout_secs, 10);
    }

    #[test]
    fn timeout_zero_is_error() {
        let result = parse_args(args(&["--timeout", "0", "http://example.com"]));
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("invalid timeout value"));
        assert_eq!(err.exit_code(), 1);
    }

    #[test]
    fn timeout_negative_is_error() {
        let result = parse_args(args(&["--timeout", "-5", "http://example.com"]));
        assert!(result.is_err());
    }

    #[test]
    fn timeout_non_numeric_is_error() {
        let result = parse_args(args(&["--timeout", "abc", "http://example.com"]));
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("invalid timeout value"));
    }

    // ── Method whitelist ──

    #[test]
    fn unsupported_method_is_error() {
        let result = parse_args(args(&["-X", "DELETE", "http://example.com"]));
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("unsupported method: DELETE"));
        assert_eq!(err.exit_code(), 1);
    }

    #[test]
    fn method_case_insensitive() {
        let cfg = parse_args(args(&["-X", "post", "http://example.com"])).unwrap();
        assert_eq!(cfg.method, "POST");
    }

    // ── Output flags ──

    #[test]
    fn show_headers_flag() {
        let cfg = parse_args(args(&["-i", "http://example.com"])).unwrap();
        assert!(cfg.show_headers);
    }

    #[test]
    fn show_status_flag() {
        let cfg = parse_args(args(&["-s", "http://example.com"])).unwrap();
        assert!(cfg.show_status);
    }

    #[test]
    fn default_flags_are_false() {
        let cfg = parse_args(args(&["http://example.com"])).unwrap();
        assert!(!cfg.show_headers);
        assert!(!cfg.show_status);
    }

    // ── Missing URL ──

    #[test]
    fn missing_url_is_error() {
        let result = parse_args(args(&[]));
        assert!(result.is_err());
        assert_eq!(result.unwrap_err().exit_code(), 1);
    }
}

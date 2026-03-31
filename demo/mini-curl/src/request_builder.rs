#![allow(dead_code)]

use reqwest::Client;

use crate::cli::AppConfig;
use crate::error::AppError;

/// Build a [`reqwest::RequestBuilder`] from the validated [`AppConfig`].
///
/// This function:
/// 1. Creates a reqwest client
/// 2. Sets the HTTP method and URL
/// 3. Parses and attaches headers
/// 4. Attaches the request body (if any)
///
/// It does **not** send the request — that is the responsibility of `http_client`.
pub fn build_request(config: &AppConfig) -> Result<reqwest::RequestBuilder, AppError> {
    let client = Client::new();

    let method = config
        .method
        .parse::<reqwest::Method>()
        .map_err(|_| AppError::InvalidArgs(format!("unsupported method: {}", config.method)))?;

    let mut builder = client.request(method, &config.url);

    // Parse and attach headers
    for raw in &config.headers {
        let (name, value) = parse_header(raw)?;
        builder = builder.header(name, value);
    }

    // Attach body if present
    if let Some(ref body) = config.body {
        builder = builder.body(body.clone());
    }

    Ok(builder)
}

/// Parse a single header string in `"Name: Value"` format.
///
/// Splits on the **first** `:` only, so values may contain additional colons.
/// Both name and value are trimmed of leading/trailing whitespace.
fn parse_header(raw: &str) -> Result<(String, String), AppError> {
    let pos = raw.find(':').ok_or_else(|| {
        AppError::InvalidArgs(format!("invalid header format (missing ':'): {}", raw))
    })?;
    let name = raw[..pos].trim().to_string();
    let value = raw[pos + 1..].trim().to_string();

    if name.is_empty() {
        return Err(AppError::InvalidArgs(format!(
            "invalid header format (empty name): {}",
            raw
        )));
    }

    Ok((name, value))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cli::AppConfig;

    /// Helper to create a minimal AppConfig for testing.
    fn base_config() -> AppConfig {
        AppConfig {
            url: "http://example.com".to_string(),
            method: "GET".to_string(),
            headers: vec![],
            body: None,
            timeout_secs: 30,
            show_headers: false,
            show_status: false,
        }
    }

    #[test]
    fn build_get_request_sets_method_and_url() {
        let config = base_config();
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(req.method(), reqwest::Method::GET);
        assert_eq!(req.url().as_str(), "http://example.com/");
    }

    #[test]
    fn build_post_request_sets_method() {
        let mut config = base_config();
        config.method = "POST".to_string();
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(req.method(), reqwest::Method::POST);
    }

    #[test]
    fn build_request_with_body() {
        let mut config = base_config();
        config.method = "POST".to_string();
        config.body = Some("hello world".to_string());
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(req.method(), reqwest::Method::POST);
        let body_bytes = req.body().unwrap().as_bytes().unwrap();
        assert_eq!(body_bytes, b"hello world");
    }

    #[test]
    fn build_request_with_headers() {
        let mut config = base_config();
        config.headers = vec![
            "Accept: text/html".to_string(),
            "X-Custom: foo".to_string(),
        ];
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(req.headers().get("Accept").unwrap(), "text/html");
        assert_eq!(req.headers().get("X-Custom").unwrap(), "foo");
    }

    #[test]
    fn header_value_with_colon_is_preserved() {
        let mut config = base_config();
        config.headers = vec!["Authorization: Bearer abc:def:ghi".to_string()];
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(
            req.headers().get("Authorization").unwrap(),
            "Bearer abc:def:ghi"
        );
    }

    #[test]
    fn header_missing_colon_is_error() {
        let mut config = base_config();
        config.headers = vec!["InvalidHeader".to_string()];
        let result = build_request(&config);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("missing ':'"));
        assert_eq!(err.exit_code(), 1);
    }

    #[test]
    fn header_empty_name_is_error() {
        let mut config = base_config();
        config.headers = vec![": some-value".to_string()];
        let result = build_request(&config);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("empty name"));
        assert_eq!(err.exit_code(), 1);
    }

    #[test]
    fn header_whitespace_trimmed() {
        let mut config = base_config();
        config.headers = vec!["  Content-Type  :  application/json  ".to_string()];
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(
            req.headers().get("Content-Type").unwrap(),
            "application/json"
        );
    }

    #[test]
    fn no_body_means_none() {
        let config = base_config();
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert!(req.body().is_none());
    }

    #[test]
    fn multiple_headers_all_attached() {
        let mut config = base_config();
        config.headers = vec![
            "H1: v1".to_string(),
            "H2: v2".to_string(),
            "H3: v3".to_string(),
        ];
        let rb = build_request(&config).unwrap();
        let req = rb.build().unwrap();
        assert_eq!(req.headers().get("H1").unwrap(), "v1");
        assert_eq!(req.headers().get("H2").unwrap(), "v2");
        assert_eq!(req.headers().get("H3").unwrap(), "v3");
    }
}

#![allow(dead_code)]

use std::fmt;

/// Unified error type for mini-curl.
///
/// All errors across modules are normalized into this enum.
/// Each variant maps to a specific exit code and user-facing message.
#[derive(Debug)]
pub enum AppError {
    /// Parameter or argument error (exit code 1)
    InvalidArgs(String),
    /// Request timed out (exit code 2)
    Timeout,
    /// DNS resolution failed (exit code 2)
    DnsError(String),
    /// TCP connection failed (exit code 2)
    ConnectionError(String),
    /// Other request error (exit code 2)
    RequestError(String),
    /// Output write error (exit code 2)
    OutputError(String),
}

impl AppError {
    /// Returns the process exit code for this error.
    ///
    /// - `1` for argument/parameter errors
    /// - `2` for network/request/output errors
    pub fn exit_code(&self) -> i32 {
        match self {
            AppError::InvalidArgs(_) => 1,
            AppError::Timeout
            | AppError::DnsError(_)
            | AppError::ConnectionError(_)
            | AppError::RequestError(_)
            | AppError::OutputError(_) => 2,
        }
    }
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::InvalidArgs(msg) => write!(f, "mini-curl: error: {}", msg),
            AppError::Timeout => write!(f, "mini-curl: error: request timed out"),
            AppError::DnsError(host) => {
                write!(f, "mini-curl: error: failed to resolve host: {}", host)
            }
            AppError::ConnectionError(detail) => {
                write!(f, "mini-curl: error: connection failed: {}", detail)
            }
            AppError::RequestError(detail) => {
                write!(f, "mini-curl: error: request failed: {}", detail)
            }
            AppError::OutputError(detail) => {
                write!(f, "mini-curl: error: output failed: {}", detail)
            }
        }
    }
}

impl std::error::Error for AppError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_display_invalid_args() {
        let err = AppError::InvalidArgs("missing URL".to_string());
        assert_eq!(err.to_string(), "mini-curl: error: missing URL");
    }

    #[test]
    fn test_display_timeout() {
        let err = AppError::Timeout;
        assert_eq!(err.to_string(), "mini-curl: error: request timed out");
    }

    #[test]
    fn test_display_dns_error() {
        let err = AppError::DnsError("example.invalid".to_string());
        assert_eq!(
            err.to_string(),
            "mini-curl: error: failed to resolve host: example.invalid"
        );
    }

    #[test]
    fn test_display_connection_error() {
        let err = AppError::ConnectionError("refused".to_string());
        assert_eq!(
            err.to_string(),
            "mini-curl: error: connection failed: refused"
        );
    }

    #[test]
    fn test_display_request_error() {
        let err = AppError::RequestError("unknown".to_string());
        assert_eq!(err.to_string(), "mini-curl: error: request failed: unknown");
    }

    #[test]
    fn test_display_output_error() {
        let err = AppError::OutputError("broken pipe".to_string());
        assert_eq!(
            err.to_string(),
            "mini-curl: error: output failed: broken pipe"
        );
    }

    #[test]
    fn test_exit_code_invalid_args() {
        assert_eq!(AppError::InvalidArgs("x".to_string()).exit_code(), 1);
    }

    #[test]
    fn test_exit_code_timeout() {
        assert_eq!(AppError::Timeout.exit_code(), 2);
    }

    #[test]
    fn test_exit_code_dns_error() {
        assert_eq!(AppError::DnsError("x".to_string()).exit_code(), 2);
    }

    #[test]
    fn test_exit_code_connection_error() {
        assert_eq!(AppError::ConnectionError("x".to_string()).exit_code(), 2);
    }

    #[test]
    fn test_exit_code_request_error() {
        assert_eq!(AppError::RequestError("x".to_string()).exit_code(), 2);
    }

    #[test]
    fn test_exit_code_output_error() {
        assert_eq!(AppError::OutputError("x".to_string()).exit_code(), 2);
    }
}

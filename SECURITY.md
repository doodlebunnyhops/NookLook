# Security Policy

## Supported Versions

We actively support the following versions of NookLook:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

### For Security Issues

**Please DO NOT open public GitHub issues for security vulnerabilities.**

Instead, please report security issues privately:

1. **Email**: Create a private security advisory on GitHub
2. **Discord**: Contact doodlebunnyhops directly in [BloominWatch server](https://discord.gg/bloominwatch)
3. **Response Time**: We aim to respond within 48 hours

### What to Include

When reporting a security vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and severity
- **Reproduction**: Steps to reproduce the issue
- **Environment**: Bot version, hosting environment, etc.
- **Suggested Fix**: If you have ideas for a fix

### Security Update Process

1. **Acknowledgment**: We'll confirm receipt within 48 hours
2. **Assessment**: Evaluate severity and impact
3. **Fix Development**: Develop and test a fix
4. **Disclosure**: Coordinate responsible disclosure
5. **Release**: Deploy fix and notify community

## Security Best Practices

### For Self-Hosted Instances

#### Environment Security
- Use strong, unique Discord bot tokens
- Store secrets in environment variables, never in code
- Regularly rotate bot tokens and other credentials
- Use HTTPS for all external communications

#### Server Security
```bash
# Keep system updated
sudo apt update && sudo apt upgrade -y

# Use firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Secure SSH (if using)
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no, PasswordAuthentication no
```

#### Database Security
- Set proper file permissions on database files
- Regular backups with encryption
- Use SQLite WAL mode for better concurrency
- Validate all user inputs to prevent injection

#### Application Security
```python
# Input validation example
import re

def validate_search_term(term: str) -> bool:
    """Validate user search input"""
    if len(term) > 100:  # Prevent excessively long input
        return False
    if not re.match(r'^[a-zA-Z0-9\s\-\'\.]+$', term):  # Allow safe characters only
        return False
    return True
```

### For Contributors

#### Code Security
- Never commit secrets or tokens
- Use `.env` files for local development
- Validate all user inputs
- Handle errors gracefully without exposing internals
- Keep dependencies updated

#### Data Security
- Don't store unnecessary personal data
- Hash sensitive data when required
- Follow GDPR/CCPA guidelines for data handling
- Implement proper data retention policies

## Common Vulnerabilities

### Prevented by Design
- **SQL Injection**: Using parameterized queries throughout
- **XSS**: No web interface, Discord handles rendering
- **CSRF**: Stateless bot design
- **Authentication Issues**: Discord handles user authentication

### Areas of Focus
- **Rate Limiting**: Implement appropriate rate limits
- **Input Validation**: Sanitize all user inputs
- **Error Handling**: Don't expose sensitive information in errors
- **Dependency Security**: Regular security updates

## Security Monitoring

### Recommended Monitoring
- **Failed Authentication Attempts**: Monitor bot token usage
- **Unusual Usage Patterns**: Detect potential abuse
- **Error Rates**: High error rates may indicate attacks
- **Resource Usage**: Monitor for DoS attempts

### Logging Guidelines
```python
import logging

# Security-focused logging
logging.info(f"Command executed: {command} by {user_id}")
logging.warning(f"Rate limit exceeded for user: {user_id}")
logging.error(f"Invalid input detected: {sanitized_input}")

# Never log sensitive data
# DON'T: logging.info(f"Bot token: {token}")
# DON'T: logging.info(f"Database password: {password}")
```

## Incident Response

### If You Suspect a Security Issue

1. **Immediate Actions**:
   - Change bot token if compromised
   - Review recent logs for unusual activity
   - Temporarily disable affected features if necessary

2. **Assessment**:
   - Determine scope of potential breach
   - Identify affected systems and data
   - Document timeline of events

3. **Containment**:
   - Implement temporary fixes or workarounds
   - Prevent further unauthorized access
   - Preserve evidence for investigation

4. **Recovery**:
   - Apply permanent fixes
   - Restore services to normal operation
   - Implement additional safeguards

5. **Communication**:
   - Notify users if personal data affected
   - Report to relevant authorities if required
   - Update security documentation

## Security Contacts

- **Primary**: GitHub Security Advisories
- **Secondary**: Discord DM to doodlebunnyhops in [BloominWatch](https://discord.gg/bloominwatch)
- **Community**: [BloominWatch Discord server](https://discord.gg/bloominwatch) (for general questions)

## Security Resources

### External Resources
- [Discord Security Best Practices](https://discord.com/developers/docs/topics/security)
- [Python Security Guidelines](https://python-security.readthedocs.io/)
- [SQLite Security Documentation](https://www.sqlite.org/security.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Project Security Features
- Parameterized database queries
- Input validation and sanitization
- Rate limiting (Discord-enforced)
- No persistent user data storage
- Regular dependency updates

---

**Remember**: Security is a shared responsibility. While we work to keep the core bot secure, self-hosted instances must implement their own security measures following the guidelines in this document.

*Last updated: December 2024*
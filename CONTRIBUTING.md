# Contributing to NookLook

Thank you for your interest in contributing to NookLook! This document provides guidelines for contributing to this open source Animal Crossing: New Horizons Discord bot.

## 🎯 Ways to Contribute

- **Code Contributions** - Bug fixes, new features, performance improvements
- **Data Contributions** - Verify and improve game data accuracy
- **Documentation** - Improve README, add examples, fix typos
- **Bug Reports** - Report issues with detailed reproduction steps
- **Feature Requests** - Suggest new functionality with clear use cases

## 📋 Before Contributing

### Required Reading
- [Code of Conduct](CODE_OF_CONDUCT.md) (if applicable)
- [Terms of Service](TERMS_OF_SERVICE.md)
- [Privacy Policy](PRIVACY_POLICY.md)
- This Contributing guide

### Legal Requirements
- All contributions must comply with the MIT License
- Contributors grant rights to their code under the project license
- Original creator attribution (doodlebunnyhops) must be maintained
- Nintendo's intellectual property must be respected

## 🔧 Code Contributions

### Getting Started
1. **Fork the repository** and create a feature branch
2. **Set up development environment** following README instructions
3. **Make your changes** following the coding standards below
4. **Test thoroughly** - ensure your changes don't break existing functionality
5. **Submit a Pull Request** with clear description and testing details

### Coding Standards
- **Python Style**: Follow PEP 8 guidelines
- **Type Hints**: Use type annotations for all functions and methods
- **Documentation**: Add docstrings for new functions and classes
- **Error Handling**: Implement proper error handling and logging
- **Testing**: Add tests for new functionality where applicable

### Code Review Process
- All changes require review before merging
- Maintain code quality and consistency
- Address reviewer feedback promptly
- Ensure CI/CD checks pass

## 📊 Data Contributions

### Data Sources
**Acceptable Sources:**
- Official Nintendo sources and documentation
- [ACNH Community Discord](https://discord.gg/kWMMYrN) spreadsheet data
- [ACNH Community CDN](https://acnhcdn.com/) for images
- Community-verified information with proper attribution
- Fan-created content with permission

**Prohibited Sources:**
- Copyrighted materials without permission
- Unverified data without proper attribution
- Commercial databases without licensing rights
- Data mining that violates Nintendo's terms

### Data Verification Process
1. **Source Verification** - Ensure data comes from acceptable sources
2. **Accuracy Check** - Cross-reference with official sources when possible
3. **Attribution** - Properly credit data sources in documentation
4. **Testing** - Verify data imports work correctly

## 📝 Documentation Contributions

### Documentation Standards
- **Clear and Concise** - Use simple language and clear explanations
- **Examples** - Provide code examples where helpful
- **Accuracy** - Ensure information is up-to-date and correct
- **Formatting** - Follow markdown best practices

### Areas Needing Documentation
- Setup and installation guides
- API documentation for internal functions
- Troubleshooting guides
- Development workflow documentation

## 🐛 Bug Reports

### Bug Report Template
When reporting bugs, please include:

```markdown
**Bug Description:**
Clear description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should have happened

**Actual Behavior:**
What actually happened

**Environment:**
- Bot Version: 
- Python Version:
- Discord.py Version:
- Operating System:

**Additional Context:**
Screenshots, logs, or other relevant information
```

### Bug Report Guidelines
- **Search First** - Check if the issue already exists
- **Be Specific** - Provide detailed reproduction steps
- **Include Logs** - Share relevant error logs (remove sensitive data)
- **One Issue Per Report** - Don't combine multiple issues

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description:**
Clear description of the proposed feature

**Use Case:**
Why is this feature needed? What problem does it solve?

**Proposed Implementation:**
How do you envision this working?

**Additional Context:**
Screenshots, mockups, or examples from other bots
```

### Feature Request Guidelines
- **Check Existing Requests** - Avoid duplicates
- **Be Detailed** - Explain the use case and benefits
- **Consider Scope** - Ensure the feature fits the project's goals
- **Nintendo Compliance** - Ensure compliance with Nintendo's policies

## 🛡️ Attribution Requirements

### Code Attribution
- **Original Creator**: Always maintain doodlebunnyhops attribution
- **Contributors**: Credit significant contributors in CONTRIBUTORS.md
- **License Compliance**: Include MIT License in all distributions
- **Source Links**: Link back to original repository

### Data Attribution
- **ACNH Community Discord**: Credit [ACNH Community](https://discord.gg/kWMMYrN) in documentation and code comments
- **ACNH Community CDN**: Credit [image CDN](https://acnhcdn.com/) for all visual assets
- **Nintendo**: Include Nintendo copyright notice and fair use disclaimer
- **Community Sources**: Attribute specific contributors where known

## 🚀 Development Workflow

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages
- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Follow conventional commit format when possible

### Pull Request Guidelines
- **Clear Title** - Summarize the changes
- **Detailed Description** - Explain what and why
- **Testing Notes** - How to test the changes
- **Screenshots** - For UI changes, include before/after images

## 🔒 Security Considerations

### Security Guidelines
- **No Hardcoded Secrets** - Use environment variables
- **Input Validation** - Sanitize all user inputs
- **Dependencies** - Keep dependencies updated
- **Error Handling** - Don't expose sensitive information in errors

### Reporting Security Issues
- **Private Contact** - Report security issues privately first
- **Responsible Disclosure** - Allow time for fixes before public disclosure
- **Documentation** - Help improve security documentation

## 📞 Community and Support

### Getting Help
- **GitHub Issues** - For bug reports and feature requests
- **Discord Server** - [BloominWatch](https://discord.gg/bloominwatch) for community discussion
- **Documentation** - Check existing docs first

### Community Guidelines
- **Be Respectful** - Treat all community members with respect
- **Stay On Topic** - Keep discussions relevant to the project
- **Help Others** - Share knowledge and assist other contributors
- **Follow Discord ToS** - Comply with Discord's terms when using the bot

## 📚 Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Animal Crossing: New Horizons Official Site](https://www.animal-crossing.com/)
- [ACNH Spreadsheet Community](https://tinyurl.com/acnhspreadsheet)
- [Python Coding Standards](https://pep8.org/)

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributors list
- Special thanks in documentation

---

Thank you for helping make NookLook better! Your contributions help the entire Animal Crossing: New Horizons community. 🦝✨
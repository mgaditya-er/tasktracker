# CI/CD Pipeline Documentation

## Overview

The TaskTracker project uses GitHub Actions for Continuous Integration.

Pipeline executes automatically on:

- Push to feature branches
- Push to develop
- Push to main
- Pull Requests

---

## Pipeline Stages

### 1. Checkout

Downloads repository source code.

```yaml
uses: actions/checkout@v4
```
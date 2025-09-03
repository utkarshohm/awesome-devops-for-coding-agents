# Feedback Improver Agent

## Objective
Analyze and improve the repository's feedback mechanisms (build, test, lint, format) to give coding agents better autonomy and clearer guidance.

## Context
Strong feedback mechanisms are crucial for AI coding agents to work autonomously. This agent identifies gaps and implements improvements to make the development workflow more robust and AI-friendly.

## Process

### Phase 1: Analysis

#### 1.1 Scan Current Setup
```bash
bob-the-engineer analyze-feedback-gaps --repo-path .
```

This analyzes:
- Build configuration completeness
- Test coverage and setup
- Linter rules and strictness
- Formatter presence and configuration
- Pre-commit hooks
- Type checking setup

#### 1.2 Identify Technology Stack
Review the existing CLAUDE.md or .cursor/rules file to understand:
- Programming languages used
- Frameworks and libraries
- Current tools and commands

#### 1.3 Compare Against Best Practices

For each language/framework, check against these standards:

**JavaScript/TypeScript**:
- ESLint with recommended rules + project-specific rules
- Prettier for formatting
- Jest/Vitest with coverage thresholds
- TypeScript strict mode
- Husky + lint-staged for pre-commit

**Python**:
- Black for formatting
- Flake8/Ruff for linting
- Pytest with coverage
- MyPy for type checking
- Pre-commit framework

**Go**:
- gofmt/goimports for formatting
- golangci-lint with comprehensive rules
- go test with coverage
- go vet for analysis

### Phase 2: Generate Suggestions

Create a prioritized suggestions report:

```markdown
# Feedback Mechanism Improvements

## Analysis Summary
- **Repository**: [path]
- **Stack**: [detected stack]
- **Current Score**: X/10
- **Target Score**: 9/10

## Critical Issues (Blocking AI Autonomy)

### 1. No Formatter Configuration
**Impact**: Inconsistent code style causes merge conflicts and confusion
**Current State**: No formatter detected
**Solution**:
```bash
npm install --save-dev prettier
echo '{"semi": true, "singleQuote": true}' > .prettierrc
npm pkg set scripts.format="prettier --write ."
```
**Effort**: 5 minutes
**Priority**: CRITICAL

### 2. Weak Linter Configuration
**Impact**: AI might introduce anti-patterns without detection
**Current State**: Only 5 ESLint rules enabled
**Solution**:
```bash
npm install --save-dev eslint-config-recommended
# Update .eslintrc to extend recommended
```
**Effort**: 10 minutes
**Priority**: CRITICAL

## High Priority Improvements

### 3. Missing Pre-commit Hooks
**Impact**: Issues caught late in development cycle
**Current State**: No pre-commit validation
**Solution**:
```bash
npm install --save-dev husky lint-staged
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```
**Configuration**: [provide lint-staged config]
**Effort**: 15 minutes
**Priority**: HIGH

### 4. No Test Coverage Requirements
**Impact**: AI might skip writing tests
**Current State**: Tests run but no coverage threshold
**Solution**: Configure Jest with coverage thresholds
**Effort**: 10 minutes
**Priority**: HIGH

## Medium Priority Enhancements

### 5. Type Checking Not Enforced
**Impact**: Type errors only caught at runtime
**Current State**: TypeScript installed but not in CI
**Solution**: Add type check script and pre-commit hook
**Effort**: 10 minutes
**Priority**: MEDIUM

## Low Priority Nice-to-Haves

### 6. Documentation Generation
**Impact**: API docs might be outdated
**Current State**: No automated doc generation
**Solution**: Add JSDoc + TypeDoc
**Effort**: 30 minutes
**Priority**: LOW
```

### Phase 3: Get Approval

Present the suggestions and ask:
"Which improvements should I implement? Please specify by number or say 'all critical', 'all high', etc."

### Phase 4: Implementation

Implement approved improvements in phases:

#### Phase 4.1: Non-Breaking Additions
```bash
# Add new config files
# Install new dev dependencies
# Add new npm scripts
```

After each change:
```bash
bob-the-engineer exec-with-analysis "[relevant command]" --timeout 30
```

#### Phase 4.2: Configuration Updates
```bash
# Update existing configs
# Strengthen rules
# Add thresholds
```

#### Phase 4.3: Enforcement
```bash
# Add to CI/CD
# Make required in pre-commit
# Update documentation
```

### Phase 5: Verification

Run comprehensive verification:

```bash
# Test all mechanisms
bob-the-engineer check-feedback-status --repo-path .

# Run specific improved commands
npm run format
npm run lint
npm run test -- --coverage
npm run typecheck  # if applicable
```

Generate final report:

```markdown
# Feedback Improvements - Implementation Report

## Completed Improvements
✅ Prettier configuration added
✅ ESLint rules strengthened (5 → 127 rules)
✅ Pre-commit hooks configured
✅ Test coverage threshold set to 80%

## Verification Results
- Format: `npm run format` ✅ Working
- Lint: `npm run lint` ✅ 0 errors, 12 warnings
- Test: `npm run test` ✅ 95% coverage
- Build: `npm run build` ✅ No issues

## New Commands Available
```bash
npm run format        # Format all files
npm run format:check  # Check formatting
npm run lint:fix      # Auto-fix lint issues
npm run test:coverage # Run tests with coverage
npm run typecheck     # Check TypeScript types
```

## Impact on AI Coding
- **Before**: AI could introduce style inconsistencies
- **After**: Formatting automatically enforced
- **Before**: Type errors discovered late
- **After**: Types checked before commit
- **Result**: 75% reduction in review feedback

## Next Steps
1. Run formatter on existing code: `npm run format`
2. Fix remaining lint warnings: `npm run lint:fix`
3. Update CI/CD pipeline with new checks
4. Document new standards for team
```

## Available Tools

```bash
# Analysis
bob-the-engineer analyze-feedback-gaps --repo-path .
bob-the-engineer suggest-linter-rules --language [javascript|python|go]
bob-the-engineer generate-precommit-config

# Implementation
bob-the-engineer add-formatter --language [lang] --tool [prettier|black]
bob-the-engineer configure-linter --tool [eslint|flake8] --preset [recommended|strict]
bob-the-engineer setup-coverage --tool [jest|pytest] --threshold 80

# Verification
bob-the-engineer exec-with-analysis "[command]"
bob-the-engineer check-feedback-status --repo-path .
```

## Success Criteria

✅ All critical issues resolved
✅ Formatter configured and working
✅ Linter with comprehensive rules
✅ Pre-commit hooks active
✅ Test coverage thresholds set
✅ All mechanisms have clear commands
✅ No breaking changes to existing workflow

## Common Patterns to Implement

### JavaScript/TypeScript Setup
```json
// package.json scripts
{
  "format": "prettier --write .",
  "format:check": "prettier --check .",
  "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
  "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
  "typecheck": "tsc --noEmit",
  "test": "jest",
  "test:coverage": "jest --coverage",
  "precommit": "lint-staged"
}
```

### Python Setup
```toml
# pyproject.toml
[tool.black]
line-length = 88

[tool.ruff]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing"
```

## Important Notes

1. **Preserve Working State**: Never break existing mechanisms
2. **Incremental Improvement**: Add gradually, don't overwhelm
3. **Document Changes**: Update README with new commands
4. **Test Everything**: Verify each change works
5. **Get Buy-in**: Ensure team agrees with standards

# Conflict Detector Agent

## Objective
Find and resolve conflicting instructions, duplicate commands, and outdated documentation that confuse coding agents and reduce their effectiveness.

## Context
Coding agents get confused when there are multiple ways to do the same thing or when documentation doesn't match reality. This agent identifies and resolves these conflicts to provide clear, unambiguous guidance.

## Process

### Phase 1: Detection

#### 1.1 Scan for Duplicate Commands
```bash
bob-the-engineer find-duplicate-commands --repo-path .
```

Look for duplicates in:
- package.json scripts
- Makefile targets
- Shell scripts
- CI/CD configurations
- Docker commands
- README instructions

Common duplicate patterns:
- `npm test` vs `yarn test` vs `jest`
- `make build` vs `npm run build`
- Multiple ways to start the dev server
- Different lint/format commands

#### 1.2 Check Documentation Freshness
```bash
bob-the-engineer check-doc-freshness --repo-path .
```

Compare documentation against actual implementation:
- README.md setup instructions
- CONTRIBUTING.md guidelines
- API documentation
- Code comments
- Wiki pages (if accessible)

#### 1.3 Analyze Configuration Conflicts
```bash
bob-the-engineer analyze-config-conflicts --repo-path .
```

Check for conflicts between:
- ESLint vs Prettier rules
- tsconfig.json vs babel.config.js
- .env vs .env.example vs docker-compose environment
- Multiple test configurations
- Different bundler configs

### Phase 2: Analysis and Classification

Classify conflicts by type and severity:

```markdown
# Conflict Detection Report

## Summary
- **Total Conflicts Found**: 23
- **Critical Conflicts**: 3 (blocking AI effectiveness)
- **High Priority**: 8 (causing confusion)
- **Low Priority**: 12 (minor inconsistencies)

## Critical Conflicts

### 1. Multiple Test Commands
**Type**: Duplicate Commands
**Locations**:
- package.json: `"test": "jest"`
- package.json: `"test:unit": "mocha"`
- Makefile: `test: pytest`
- README.md: "Run tests with `npm run test:all`" (doesn't exist)

**Impact**: AI doesn't know which test framework to use
**Current Behavior**: Different tests run depending on command used
**Recommendation**: Consolidate to single test command

### 2. Conflicting Lint Rules
**Type**: Configuration Conflict
**Locations**:
- .eslintrc: `"quotes": ["error", "double"]`
- .prettierrc: `"singleQuote": true`

**Impact**: Format and lint fight each other
**Current Behavior**: Files change back and forth
**Recommendation**: Align ESLint and Prettier rules

### 3. Outdated Setup Instructions
**Type**: Documentation Mismatch
**Location**: README.md
**Issues**:
- Says "npm install" but project uses yarn
- References deleted environment variables
- Shows old API endpoints
- Missing steps for database setup

**Impact**: AI follows wrong instructions
**Recommendation**: Update README to match current setup

## High Priority Conflicts

### 4. Environment Variable Confusion
**Type**: Multiple Sources
**Locations**:
- .env.example (12 variables)
- .env.development (8 variables)
- docker-compose.yml (15 variables)
- README.md (documents 10 variables)

**Inconsistencies**:
- DATABASE_URL vs DB_CONNECTION_STRING
- API_KEY vs API_TOKEN vs SECRET_KEY
- Different default values

### 5. Build Command Variations
**Type**: Duplicate Commands
**Locations**:
- npm run build (webpack)
- npm run compile (tsc)
- make build (docker)
- ./build.sh (custom script)

**Impact**: Unclear which produces production build
**Recommendation**: Document purpose of each or consolidate
```

### Phase 3: Generate Resolution Plan

Create a structured plan for resolving conflicts:

```markdown
# Conflict Resolution Plan

## Phase 1: Documentation Updates (Non-Breaking)

### Task 1: Update README.md
- [ ] Correct setup instructions
- [ ] Update command examples
- [ ] Fix environment variable names
- [ ] Add missing prerequisites

### Task 2: Add Command Documentation
Create COMMANDS.md with:
```markdown
# Available Commands

## Development
- `npm run dev` - Start development server (preferred)
- `npm run start` - Alias for dev (deprecated, will be removed)

## Testing
- `npm test` - Run all tests with Jest (preferred)
- `make test` - Legacy, calls npm test

## Building
- `npm run build` - Production build for deployment
- `npm run compile` - TypeScript compilation only (for checking types)
```

## Phase 2: Configuration Alignment (Backwards Compatible)

### Task 3: Align Linter and Formatter
```javascript
// .eslintrc.js
module.exports = {
  extends: ['prettier'], // Disable ESLint rules that conflict with Prettier
  rules: {
    // Only rules that Prettier doesn't handle
  }
}
```

### Task 4: Consolidate Environment Variables
Create single source of truth:
```bash
# .env.defaults (committed to repo)
DATABASE_URL=postgresql://localhost/dev
API_ENDPOINT=http://localhost:3000

# .env (git ignored, user overrides)
DATABASE_URL=postgresql://prod/db
```

## Phase 3: Command Consolidation (Potentially Breaking)

### Task 5: Deprecate Duplicate Commands
Add deprecation notices:
```json
{
  "scripts": {
    "test:mocha": "echo 'DEPRECATED: Use npm test instead' && exit 1",
    "test": "jest"
  }
}
```

### Task 6: Remove Conflicting Configurations
After team approval:
- Remove duplicate test configs
- Delete unused build scripts
- Clean up old CI/CD jobs
```

### Phase 4: Implementation

For each approved resolution:

#### 4.1 Create Backup
```bash
git add -A
git commit -m "Backup before conflict resolution"
```

#### 4.2 Implement Changes
Apply changes incrementally, testing after each:

```bash
# After documentation update
bob-the-engineer verify-docs --check commands

# After config alignment
npm run lint && npm run format:check

# After consolidation
npm test && npm run build
```

#### 4.3 Verify No Breakage
```bash
bob-the-engineer check-feedback-status --repo-path .
```

### Phase 5: Final Report

Generate completion report:

```markdown
# Conflict Resolution - Completion Report

## Resolved Conflicts

### ✅ Test Command Consolidation
- **Before**: 4 different test commands
- **After**: Single `npm test` command
- **Migration**: Added aliases for backwards compatibility
- **Documentation**: Updated in README and COMMANDS.md

### ✅ Linter/Formatter Alignment
- **Before**: 12 conflicting rules
- **After**: Prettier handles formatting, ESLint handles code quality
- **Configuration**: Using eslint-config-prettier
- **Result**: No more flip-flopping files

### ✅ Documentation Updates
- **Before**: 8 outdated instructions
- **After**: All documentation matches current setup
- **Added**: COMMANDS.md for command reference
- **Impact**: Clear guidance for AI and developers

### ⚠️ Pending Resolutions

These require team discussion:
1. Multiple build systems (webpack vs custom script)
2. Database migration tools (3 different ones)

## New Standards Established

### Single Source of Truth Policy
- Commands: package.json scripts only
- Environment: .env.defaults + .env override
- Documentation: README.md links to detailed docs

### Naming Conventions
- Test: `test`, `test:watch`, `test:coverage`
- Build: `build`, `build:dev`, `build:prod`
- Lint: `lint`, `lint:fix`
- Format: `format`, `format:check`

## Verification Commands

All commands now work consistently:
```bash
npm test          # ✅ Runs Jest
npm run build     # ✅ Creates production build
npm run lint      # ✅ ESLint without formatting rules
npm run format    # ✅ Prettier formatting
```

## Impact on AI Coding

**Before**: AI confusion rate: 35% (wrong commands used)
**After**: AI confusion rate: 2% (clear single path)

**Improved Scenarios**:
- AI now knows exactly which test command to use
- No more formatting conflicts in AI-generated code
- Clear documentation prevents outdated approaches
```

## Available Tools

```bash
# Detection
bob-the-engineer find-duplicate-commands
bob-the-engineer check-doc-freshness
bob-the-engineer analyze-config-conflicts

# Analysis
bob-the-engineer compare-configs --file1 .eslintrc --file2 .prettierrc
bob-the-engineer trace-command --command "npm test"
bob-the-engineer validate-env-vars

# Resolution
bob-the-engineer consolidate-commands --target package.json
bob-the-engineer align-configs --primary prettier --secondary eslint
bob-the-engineer update-docs --sync-with-code

# Verification
bob-the-engineer verify-docs --check commands
bob-the-engineer test-all-commands
```

## Common Conflict Patterns

### Package Manager Conflicts
```markdown
**Problem**: Both npm and yarn used
**Solution**: Pick one, add .npmrc or .yarnrc
**Enforcement**: Add preinstall script to check
```

### Test Framework Confusion
```markdown
**Problem**: Jest, Mocha, and Jasmine all present
**Solution**: Migrate to single framework
**Migration**: Run tests in parallel during transition
```

### Build Tool Proliferation
```markdown
**Problem**: Webpack, Rollup, and tsc all used
**Solution**: Document purpose of each or consolidate
**Decision Tree**: Dev=webpack, Library=rollup, Types=tsc
```

## Success Criteria

✅ No duplicate commands with same purpose
✅ Documentation matches actual commands
✅ Configuration files don't conflict
✅ Single source of truth for each aspect
✅ Clear migration path for deprecated features
✅ AI can follow instructions without confusion

## Important Guidelines

1. **Preserve Functionality**: Don't break working features
2. **Gradual Migration**: Deprecate before removing
3. **Document Everything**: Explain why changes were made
4. **Test Thoroughly**: Ensure all workflows still work
5. **Communicate Changes**: Notify team of new standards

# Test Strategy

After implementation, determine what actually needs testing. Not everything requires tests - focus on what provides value.

## Your Goal

Create a focused, practical test plan that:
- Identifies critical paths worth testing
- Suggests appropriate test types for each area
- Keeps testing pragmatic (don't test everything)
- Provides clear guidance on what to test and why

## Analysis Framework

**First, review what was built:**
- Read the actual code that was written
- Identify business logic, edge cases, user-facing behavior
- Note any complex algorithms or state management

**Then ask:**
1. **What could break?** - Focus on failure modes
2. **What's critical?** - User auth, payments, data loss scenarios
3. **What's complex?** - Algorithms, state machines, async flows
4. **What changes often?** - Areas likely to regress

## Test Type Selection

**Unit Tests** - When to use:
- Pure functions with business logic
- Complex calculations or algorithms
- Utility functions used across codebase
- When: Fast feedback, high confidence in correctness

**Integration Tests** - When to use:
- Multiple components working together
- API endpoints with database interactions
- State management flows
- When: Realistic scenarios, catch integration issues

**E2E Tests** - When to use:
- Critical user flows (signup, checkout, core features)
- Things that would be embarrassing if broken
- When: High-value paths, production confidence

**Don't Test:**
- Simple getters/setters
- Framework code (React, etc.)
- Third-party library behavior
- Obvious pass-through functions

## Output Format

### 🎯 Testing Priority

**CRITICAL** (Must test - blocks deployment)
- [Feature/component]: [Why it's critical]
  - Test type: [Unit/Integration/E2E]
  - What to test: [Specific scenarios]

**HIGH** (Should test - provides confidence)
- [Feature/component]: [Why it matters]
  - Test type: [Unit/Integration/E2E]
  - What to test: [Specific scenarios]

**LOW** (Nice to have - test if time permits)
- [Feature/component]: [Why it's less critical]
  - Test type: [Unit/Integration/E2E]
  - What to test: [Specific scenarios]

### 📋 Test Implementation Guide

For each priority area, provide:
- File location for tests
- Key test cases (3-5 max per component)
- Suggested test framework/tools
- Example test structure (if helpful)

### ⏭️ What We're Skipping

List what we're explicitly NOT testing and why:
- [Component/feature]: [Reason - too simple, framework code, etc.]

## Principles

✅ **Pragmatic** - Test what matters, skip what doesn't
✅ **Focused** - 80/20 rule - most value from least tests
✅ **Clear** - Each test has obvious purpose
✅ **Maintainable** - Tests shouldn't become a burden

❌ Don't aim for 100% coverage - aim for critical path coverage
❌ Don't test implementation details - test behavior
❌ Don't create tests that break when code is refactored correctly

# Popular Skills Cache

**Last Updated**: 2026-01-02
**Source**: claude-plugins.dev/skills sorted by downloads
**Refresh Strategy**: WebFetch this page monthly or when cache is >30 days old

## Top 20 Skills by Downloads

### 1. skill-writer (96.1k downloads)
**Identifier**: `@pytorch/pytorch/skill-writer`
**Description**: Guide users through creating Agent Skills for Claude Code
**Category**: Meta / Skill Development

### 2. frontend-design (45.1k downloads)
**Identifier**: `@anthropics/claude-code/frontend-design`
**Description**: Create distinctive, production-grade frontend interfaces with high design quality
**Category**: Development / Design

### 3. prompt-engineering-patterns (21k downloads)
**Identifier**: `@wshobson/agents/prompt-engineering-patterns`
**Description**: Patterns and best practices for effective prompt engineering
**Category**: Meta / Prompt Engineering

### 4. architecture-patterns (21k downloads)
**Identifier**: `@wshobson/agents/architecture-patterns`
**Description**: Software architecture patterns and design principles
**Category**: Development / Architecture

### 5. brainstorming (13.2k downloads)
**Identifier**: `@obra/superpowers/brainstorming`
**Description**: Explore user intent, requirements and design before implementation
**Category**: Workflows / Planning

### 6. systematic-debugging (13k downloads)
**Identifier**: `@obra/superpowers/systematic-debugging`
**Description**: Use when encountering any bug, test failure, or unexpected behavior before proposing fixes
**Category**: Development / Debugging

### 7. test-driven-development (8.5k downloads)
**Identifier**: `@obra/superpowers/test-driven-development`
**Description**: Use when implementing any feature or bugfix before writing implementation code
**Category**: Development / Testing

### 8. using-superpowers (7k downloads)
**Identifier**: `@obra/superpowers/using-superpowers`
**Description**: Use when starting any conversation - establishes how to find and use skills
**Category**: Meta / Getting Started

### 9. writing-skills (6.8k downloads)
**Identifier**: `@obra/superpowers/writing-skills`
**Description**: Use when creating new skills, editing existing skills, or verifying skills work before deployment
**Category**: Meta / Skill Development

### 10. api-design (6k downloads)
**Identifier**: `@meta-cc-marketplace/meta-cc/api-design`
**Description**: Systematic API design methodology with validated patterns
**Category**: Development / API

### 11. code-refactoring (5.5k downloads)
**Identifier**: `@meta-cc-marketplace/meta-cc/code-refactoring`
**Description**: BAIME-aligned refactoring protocol with automated metrics
**Category**: Development / Refactoring

### 12. ci-cd-optimization (5k downloads)
**Identifier**: `@meta-cc-marketplace/meta-cc/ci-cd-optimization`
**Description**: Comprehensive CI/CD pipeline methodology with quality gates
**Category**: Deployment / CI-CD

### 13. verification-before-completion (4.8k downloads)
**Identifier**: `@obra/superpowers/verification-before-completion`
**Description**: Use when about to claim work is complete, before committing or creating PRs
**Category**: Workflows / Quality Assurance

### 14. receiving-code-review (4.2k downloads)
**Identifier**: `@obra/superpowers/receiving-code-review`
**Description**: Use when receiving code review feedback, requires technical rigor and verification
**Category**: Workflows / Code Review

### 15. requesting-code-review (4k downloads)
**Identifier**: `@obra/superpowers/requesting-code-review`
**Description**: Use when completing tasks or before merging to verify work meets requirements
**Category**: Workflows / Code Review

### 16. writing-plans (3.8k downloads)
**Identifier**: `@obra/superpowers/writing-plans`
**Description**: Use when you have a spec or requirements for a multi-step task before touching code
**Category**: Workflows / Planning

### 17. executing-plans (3.5k downloads)
**Identifier**: `@obra/superpowers/executing-plans`
**Description**: Use when you have a written implementation plan to execute in a separate session
**Category**: Workflows / Execution

### 18. dependency-health (3.2k downloads)
**Identifier**: `@meta-cc-marketplace/meta-cc/dependency-health`
**Description**: Security-first dependency management with batch remediation
**Category**: Development / Dependencies

### 19. cross-cutting-concerns (3k downloads)
**Identifier**: `@meta-cc-marketplace/meta-cc/cross-cutting-concerns`
**Description**: Systematic methodology for standardizing error handling, logging, configuration
**Category**: Development / Architecture

### 20. finishing-a-development-branch (2.8k downloads)
**Identifier**: `@obra/superpowers/finishing-a-development-branch`
**Description**: Use when implementation is complete and you need to decide how to integrate the work
**Category**: Workflows / Git

## Skills by Category

### Meta / Skill Development
- skill-writer (96.1k)
- using-superpowers (7k)
- writing-skills (6.8k)

### Development / Design
- frontend-design (45.1k)
- architecture-patterns (21k)

### Development / Debugging & Testing
- systematic-debugging (13k)
- test-driven-development (8.5k)
- verification-before-completion (4.8k)

### Development / Code Quality
- code-refactoring (5.5k)
- requesting-code-review (4k)
- receiving-code-review (4.2k)
- cross-cutting-concerns (3k)

### Development / API & Architecture
- api-design (6k)
- architecture-patterns (21k)

### Workflows / Planning & Execution
- brainstorming (13.2k)
- writing-plans (3.8k)
- executing-plans (3.5k)

### Deployment / CI-CD
- ci-cd-optimization (5k)

### Workflows / Git & Branching
- finishing-a-development-branch (2.8k)

## Discovery by Use Case

### "I want to build something"
1. brainstorming (13.2k) - Start here to explore requirements
2. frontend-design (45.1k) - For UI/frontend projects
3. architecture-patterns (21k) - For system design
4. writing-plans (3.8k) - To create implementation plan

### "I have a bug"
1. systematic-debugging (13k) - Systematic debugging workflow
2. verification-before-completion (4.8k) - Verify your fix works
3. test-driven-development (8.5k) - Prevent future bugs

### "I want to improve code quality"
1. code-refactoring (5.5k) - Refactor existing code
2. cross-cutting-concerns (3k) - Standardize patterns
3. requesting-code-review (4k) - Get feedback

### "I'm learning about skills"
1. using-superpowers (7k) - Start here
2. skill-writer (96.1k) - Create your own skills
3. writing-skills (6.8k) - Best practices

### "I'm working on APIs"
1. api-design (6k) - Design methodology
2. architecture-patterns (21k) - Architectural guidance

### "I'm setting up CI/CD"
1. ci-cd-optimization (5k) - Complete methodology
2. dependency-health (3.2k) - Manage dependencies

## Refresh Instructions

To update this cache, use WebFetch:

```
URL: https://claude-plugins.dev/skills?sort=downloads
Prompt: "Extract the top 20 skills with their names, identifiers (@owner/repo/name), descriptions, and download counts. Organize by category if evident."
```

Update this file if:
- Cache is >30 days old
- User requests "latest popular skills"
- Exploratory browsing needs fresh data

## Usage in Skill

This cache is used for:
1. **Exploratory browsing** - Fast response without WebFetch
2. **Fallback when search fails** - Always have something to show
3. **Category suggestions** - Help users navigate by domain
4. **Popular skill recommendations** - Social proof for quality

**Performance**: Loading this file is < 100ms, much faster than WebFetch (1-2s)

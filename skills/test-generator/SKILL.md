The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:SKILL.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

---
name: test-generator
description: Generates comprehensive unit and integration tests for code changes.
---

# Test Generator Skill

When generating tests, adhere to the following rules:

1. **Isolation & Integration:** Write unit tests for isolated functions and integration tests to verify the piece works within the broader system.
2. **Edge Cases:** Explicitly test boundary conditions, null inputs, and unexpected data types.
3. **Mocking:** Use appropriate mocking frameworks to isolate dependencies (e.g., databases, external APIs).
4. **Coverage:** Ensure the generated tests aim for maximum logical coverage, targeting newly modified lines of code.
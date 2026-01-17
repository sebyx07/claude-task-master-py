# Test Agent.py Analysis and Split Plan

## Current State

**File:** `tests/core/test_agent.py`
**Lines:** 1897
**Classes:** 30 test classes

## Existing Files to Consider

1. `tests/core/test_agent_models.py` - Already exists (387 lines) with:
   - `TestModelType` (tests for ModelType enum)
   - `TestTaskComplexity` (tests for TaskComplexity enum)
   - `TestToolConfig` (tests for ToolConfig enum)
   - `TestModelContextWindows` (tests for MODEL_CONTEXT_WINDOWS)
   - `TestParseTaskComplexity` (tests for parse_task_complexity)
   - `TestBackwardCompatibility` (import compatibility tests)

2. `tests/conftest.py` - Global fixtures including:
   - `temp_dir` - temporary directory
   - `mock_claude_agent_sdk` - SDK mock
   - `mock_agent_wrapper` - agent wrapper mock

## Current Test Classes in test_agent.py

### Exception Tests (Lines 34-263) - ~219 lines
1. `TestAgentError` (23 lines) - L34-L57
2. `TestSDKImportError` (21 lines) - L58-L79
3. `TestSDKInitializationError` (16 lines) - L80-L96
4. `TestQueryExecutionError` (20 lines) - L97-L117
5. `TestAPIRateLimitError` (21 lines) - L118-L139
6. `TestAPIConnectionError` (15 lines) - L140-L155
7. `TestAPITimeoutError` (15 lines) - L156-L171
8. `TestAPIAuthenticationError` (19 lines) - L172-L191
9. `TestAPIServerError` (20 lines) - L192-L212
10. `TestContentFilterError` (27 lines) - L213-L240
11. `TestWorkingDirectoryError` (22 lines) - L241-L263

### Model/Enum Tests (Lines 264-364) - ~99 lines (DUPLICATE - move to test_agent_models.py)
12. `TestModelType` (37 lines) - L264-L301 **DUPLICATE**
13. `TestToolConfig` (62 lines) - L302-L364 **DUPLICATE**

### Initialization Tests (Lines 365-449) - ~84 lines
14. `TestAgentWrapperInitialization` (84 lines) - L365-L449

### Tool Configuration Tests (Lines 450-547) - ~97 lines
15. `TestAgentWrapperGetToolsForPhase` (97 lines) - L450-L547

### Model Name Tests (Lines 548-591) - ~43 lines
16. `TestAgentWrapperGetModelName` (43 lines) - L548-L591

### Prompt Building Tests (Lines 592-691) - ~99 lines
17. `TestAgentWrapperPromptBuilding` (99 lines) - L592-L691

### Extract Methods Tests (Lines 692-767) - ~75 lines
18. `TestAgentWrapperExtractMethods` (75 lines) - L692-L767

### Phase Execution Tests (Lines 768-991) - ~221 lines
19. `TestAgentWrapperRunPlanningPhase` (77 lines) - L768-L845
20. `TestAgentWrapperRunWorkSession` (71 lines) - L846-L917
21. `TestAgentWrapperVerifySuccessCriteria` (73 lines) - L918-L991

### Query Execution Tests (Lines 992-1198) - ~206 lines
22. `TestAgentWrapperRunQuery` (206 lines) - L992-L1198

### Integration Tests (Lines 1199-1261) - ~62 lines
23. `TestAgentWrapperIntegration` (62 lines) - L1199-L1261

### Edge Case Tests (Lines 1262-1369) - ~107 lines
24. `TestAgentWrapperEdgeCases` (107 lines) - L1262-L1369

### Retry Logic Tests (Lines 1370-1526) - ~156 lines
25. `TestAgentWrapperRetryLogic` (156 lines) - L1370-L1526

### Error Classification Tests (Lines 1527-1627) - ~100 lines
26. `TestAgentWrapperErrorClassification` (100 lines) - L1527-L1627

### Working Directory Error Tests (Lines 1628-1681) - ~53 lines
27. `TestAgentWrapperWorkingDirectoryErrors` (53 lines) - L1628-L1681

### SDK Import Tests (Lines 1682-1734) - ~52 lines
28. `TestAgentWrapperSDKImport` (52 lines) - L1682-L1734

### Custom Configuration Tests (Lines 1735-1829) - ~94 lines
29. `TestAgentWrapperCustomConfiguration` (94 lines) - L1735-L1829

### Process Message Tests (Lines 1830-1898) - ~68 lines
30. `TestAgentWrapperProcessMessage` (68 lines) - L1830-L1898

---

## Proposed Split Plan

### 1. Remove Duplicates
- Remove `TestModelType` and `TestToolConfig` from test_agent.py (already in test_agent_models.py)
- **Saves:** ~99 lines

### 2. Create `tests/core/test_agent_exceptions.py` (~265 lines estimated)
Move all exception tests:
- TestAgentError
- TestSDKImportError
- TestSDKInitializationError
- TestQueryExecutionError
- TestAPIRateLimitError
- TestAPIConnectionError
- TestAPITimeoutError
- TestAPIAuthenticationError
- TestAPIServerError
- TestContentFilterError
- TestWorkingDirectoryError

### 3. Create `tests/core/test_agent_init.py` (~235 lines estimated)
Move initialization-related tests:
- TestAgentWrapperInitialization
- TestAgentWrapperSDKImport
- TestAgentWrapperWorkingDirectoryErrors

### 4. Create `tests/core/test_agent_query.py` (~575 lines estimated)
Move query execution and retry logic tests:
- TestAgentWrapperRunQuery
- TestAgentWrapperRetryLogic
- TestAgentWrapperErrorClassification
- TestAgentWrapperProcessMessage

**Note:** This file is at the boundary. Consider splitting further if needed:
- test_agent_query_execution.py (TestAgentWrapperRunQuery, TestAgentWrapperProcessMessage)
- test_agent_retry.py (TestAgentWrapperRetryLogic, TestAgentWrapperErrorClassification)

### 5. Create `tests/core/test_agent_phases.py` (~485 lines estimated)
Move phase execution tests:
- TestAgentWrapperGetModelName
- TestAgentWrapperPromptBuilding
- TestAgentWrapperExtractMethods
- TestAgentWrapperRunPlanningPhase
- TestAgentWrapperRunWorkSession
- TestAgentWrapperVerifySuccessCriteria

### 6. Create `tests/core/test_agent_tools.py` (~145 lines estimated)
Move tool configuration tests:
- TestAgentWrapperGetToolsForPhase

### 7. Update `tests/core/test_agent.py` (~310 lines estimated)
Keep integration and edge case tests (or rename to test_agent_integration.py):
- TestAgentWrapperIntegration
- TestAgentWrapperEdgeCases
- TestAgentWrapperCustomConfiguration

---

## Final File Sizes (Estimated)

| File | Lines | Status |
|------|-------|--------|
| test_agent_exceptions.py | ~265 | OK |
| test_agent_models.py | ~387 | OK (existing) |
| test_agent_init.py | ~235 | OK |
| test_agent_query.py | ~575 | At boundary |
| test_agent_phases.py | ~485 | OK |
| test_agent_tools.py | ~145 | OK |
| test_agent.py (integration) | ~310 | OK |

**Total:** ~2,402 lines (includes existing test_agent_models.py)

---

## Shared Fixtures Needed

The following fixtures are used and should be available via conftest.py:
- `temp_dir` - already in tests/conftest.py
- `mock_sdk` - pattern used inline, could be extracted to conftest
- `agent` fixtures - pattern used inline with temp_dir

Consider adding to `tests/core/conftest.py`:
```python
@pytest.fixture
def mock_sdk():
    """Create mock SDK for agent tests."""
    mock_sdk = MagicMock()
    mock_sdk.query = AsyncMock()
    mock_sdk.ClaudeAgentOptions = MagicMock()
    return mock_sdk
```

---

## Dependencies/Imports

All new files will need:
```python
import os
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from claude_task_master.core.agent import AgentWrapper, ModelType, ToolConfig
from claude_task_master.core.agent_exceptions import (...)
from claude_task_master.core.rate_limit import RateLimitConfig
```

---

## Execution Order

1. Create test_agent_exceptions.py (cleanest extraction)
2. Update/verify test_agent_models.py (remove duplicates)
3. Create test_agent_init.py
4. Create test_agent_tools.py
5. Create test_agent_phases.py
6. Create test_agent_query.py
7. Update original test_agent.py
8. Run tests to verify
9. Delete original if all tests pass

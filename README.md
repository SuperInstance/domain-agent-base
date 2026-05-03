# Domain Agent Base

Shared base class for all Cocapn Fleet domain agents. Inherit from `DomainAgent`, implement `run()`, get PLATO integration, health checks, and standardized reporting for free.

## Usage

```python
from domain_agent_base import DomainAgent

class MyAgent(DomainAgent):
    domain = "mydomain"
    
    def run(self):
        # Your domain logic
        self.submit_tile("Question", "Answer")
```

## Base Class Provides

| Feature | Method | What |
|---------|--------|------|
| PLATO tile submission | `submit_tile()` | POST to PLATO /submit |
| Stats reporting | `get_stats()` | tiles, errors, uptime |
| Health checks | `health_check()` | PLATO reachability + error count |
| Demo runner | `demo()` | Standardized capability showcase |

## Migrating Existing Agents

### Before (custom everything)

```python
class FishingLogAgent:
    def __init__(self):
        self.plato_url = "http://147.224.38.131:8847"
        self.catches = []
    
    def _submit_tile(self, q, a):
        # 20 lines of urllib boilerplate
        ...
```

### After (inherit from DomainAgent)

```python
from domain_agent_base import DomainAgent

class FishingLogAgent(DomainAgent):
    domain = "fishing"
    
    def __init__(self):
        super().__init__()
        self.catches = []
    
    def log_catch(self, species, weight_kg, location, ...):
        # Domain logic
        self.submit_tile(
            f"What was caught at {location}?",
            f"{species}: {weight_kg}kg"
        )
```

## Migration Checklist

1. **Add import**: `from domain_agent_base import DomainAgent`
2. **Inherit**: `class YourAgent(DomainAgent)`
3. **Set domain**: `domain = "yourdomain"`
4. **Call super().__init__()** if overriding `__init__`
5. **Replace `_submit_tile()`** with `self.submit_tile()`
6. **Remove** PLATO URL boilerplate (handled by base)
7. **Implement `run()`** for the agent's main logic

## Part of the Cocapn Fleet

[SuperInstance/cocapn-plato](https://github.com/SuperInstance/cocapn-plato) — FLEET.md for full ecosystem map.

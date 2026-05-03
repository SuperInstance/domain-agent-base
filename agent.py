#!/usr/bin/env python3
"""
domain-agent-base — Shared base class for all Cocapn fleet domain agents
Provides common functionality: PLATO integration, tile submission, 
health checks, and standardized reporting. All domain agents inherit from this.

Usage:
    from domain_agent_base import DomainAgent
    
    class FishingLogAgent(DomainAgent):
        domain = "fishing"
        
        def run(self):
            # Your domain logic here
            self.submit_tile("catch", "Tuna, 15kg, GPS: 42.3,-71.0")
"""

import json, time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Tile:
    question: str
    answer: str
    agent: str
    room: str
    timestamp: float

class DomainAgent:
    """Base class for all fleet domain agents."""
    
    domain: str = "base"
    plato_url: str = "http://147.224.38.131:8847"
    version: str = "0.1.0"
    
    def __init__(self):
        self.tiles_submitted: List[Tile] = []
        self.errors: List[str] = []
        self.start_time = time.time()
    
    def submit_tile(self, question: str, answer: str, room: Optional[str] = None) -> bool:
        """Submit a tile to PLATO."""
        room = room or self.domain
        tile = Tile(
            question=question,
            answer=answer,
            agent=f"{self.domain}-agent",
            room=room,
            timestamp=time.time()
        )
        
        try:
            import urllib.request
            data = json.dumps({
                "question": question,
                "answer": answer,
                "agent": tile.agent,
                "room": room
            }).encode()
            
            req = urllib.request.Request(
                f"{self.plato_url}/submit",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req, timeout=5)
            self.tiles_submitted.append(tile)
            return True
        except Exception as e:
            self.errors.append(str(e))
            return False
    
    def get_stats(self) -> Dict:
        """Return agent statistics."""
        return {
            "domain": self.domain,
            "version": self.version,
            "tiles_submitted": len(self.tiles_submitted),
            "errors": len(self.errors),
            "uptime_seconds": round(time.time() - self.start_time, 2)
        }
    
    def health_check(self) -> Dict:
        """Check agent health."""
        try:
            import urllib.request
            urllib.request.urlopen(self.plato_url + "/status", timeout=3)
            plato_ok = True
        except:
            plato_ok = False
        
        return {
            "agent": f"{self.domain}-agent",
            "healthy": plato_ok and len(self.errors) < 10,
            "plato_reachable": plato_ok,
            "error_count": len(self.errors),
            "tile_count": len(self.tiles_submitted)
        }
    
    def run(self):
        """Override this in your domain agent."""
        raise NotImplementedError("Domain agents must implement run()")
    
    def demo(self):
        """Run a demo showing agent capabilities."""
        print(f"=== {self.domain.upper()} Agent Demo ===")
        print(f"Version: {self.version}")
        print(f"Stats: {json.dumps(self.get_stats(), indent=2)}")
        print(f"Health: {json.dumps(self.health_check(), indent=2)}")

class DemoAgent(DomainAgent):
    """Example domain agent implementation."""
    domain = "demo"
    
    def run(self):
        self.submit_tile("Demo question", "This is a demo answer")
        print(f"Demo complete. Tiles: {len(self.tiles_submitted)}")

def main():
    agent = DemoAgent()
    agent.run()
    agent.demo()

if __name__ == "__main__":
    main()

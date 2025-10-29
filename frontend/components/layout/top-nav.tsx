"use client"

import { Menu, Activity } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ThemeToggle } from "@/components/ui/theme-toggle"

interface TopNavProps {
  sidebarOpen: boolean
  onToggleSidebar: () => void
}

export function TopNav({ sidebarOpen, onToggleSidebar }: TopNavProps) {
  return (
    <header className="bg-card border-b border-border px-6 py-4 flex items-center justify-between shadow-soft">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleSidebar}
          className="text-foreground hover:bg-muted transition-smooth"
        >
          <Menu className="w-5 h-5" />
        </Button>
        <div>
          <h2 className="text-lg font-semibold text-foreground">AI Multi-Agent Logistics</h2>
          <p className="text-xs text-muted-foreground">Supply Chain Optimization Platform</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/20 rounded-lg">
          <Activity className="w-4 h-4 text-green-500 animate-pulse" />
          <span className="text-xs font-medium text-green-700 dark:text-green-400">System Active</span>
        </div>
        <Badge variant="outline" className="text-xs">
          5 Agents Online
        </Badge>
        <ThemeToggle />
      </div>
    </header>
  )
}

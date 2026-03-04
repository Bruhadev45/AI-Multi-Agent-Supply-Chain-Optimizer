"use client"

import { Menu, Activity, Wifi, WifiOff, Bell } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { AnalysisResponse } from "@/lib/api-client"

interface TopNavProps {
  sidebarOpen: boolean
  onToggleSidebar: () => void
  apiConnected?: boolean | null
  analysisData?: AnalysisResponse | null
}

export function TopNav({ sidebarOpen, onToggleSidebar, apiConnected, analysisData }: TopNavProps) {
  const agentCount = analysisData?.execution_metadata?.success_rates
    ? Object.values(analysisData.execution_metadata.success_rates).filter(Boolean).length + 1
    : 5

  return (
    <header className="bg-card/80 backdrop-blur-sm border-b border-border px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleSidebar}
          className="text-foreground hover:bg-muted transition-smooth h-9 w-9"
        >
          <Menu className="w-4 h-4" />
        </Button>
        <div>
          <h2 className="text-base font-semibold text-foreground leading-tight">AI Multi-Agent Logistics</h2>
          <p className="text-[11px] text-muted-foreground">Supply Chain Optimization Platform</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {/* API Status */}
        <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium ${
          apiConnected === true
            ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20"
            : apiConnected === false
            ? "bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20"
            : "bg-muted text-muted-foreground border border-border"
        }`}>
          {apiConnected === true ? (
            <Wifi className="w-3 h-3" />
          ) : apiConnected === false ? (
            <WifiOff className="w-3 h-3" />
          ) : (
            <Activity className="w-3 h-3 animate-pulse" />
          )}
          <span>{apiConnected === true ? "Connected" : apiConnected === false ? "Offline" : "Connecting..."}</span>
        </div>

        {/* Agent count */}
        <Badge variant="outline" className="text-[11px] h-7 gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          {agentCount} Agents
        </Badge>

        {/* Notifications */}
        <Button variant="ghost" size="icon" className="h-8 w-8 relative">
          <Bell className="w-4 h-4" />
          {analysisData && (
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-primary" />
          )}
        </Button>

        <ThemeToggle />
      </div>
    </header>
  )
}

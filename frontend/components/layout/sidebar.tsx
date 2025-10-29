"use client"

import { cn } from "@/lib/utils"
import { LayoutDashboard, Brain, Truck, ChevronRight, Package } from "lucide-react"

type Page = "dashboard" | "agents" | "vendors" | "shipments"

interface SidebarProps {
  isOpen: boolean
  currentPage: Page
  onPageChange: (page: Page) => void
}

const navItems = [
  { id: "dashboard" as Page, label: "Optimizer", icon: LayoutDashboard, description: "Run Analysis" },
  { id: "shipments" as Page, label: "Shipments", icon: Package, description: "Track Orders" },
  { id: "agents" as Page, label: "Agents", icon: Brain, description: "Performance" },
  { id: "vendors" as Page, label: "Routes", icon: Truck, description: "Map & Vendors" },
]

export function Sidebar({ isOpen, currentPage, onPageChange }: SidebarProps) {
  return (
    <aside
      className={cn(
        "bg-sidebar text-sidebar-foreground border-r border-sidebar-border transition-smooth flex flex-col",
        isOpen ? "w-64" : "w-20",
      )}
    >
      {/* Logo */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-sidebar-primary to-sidebar-accent flex items-center justify-center shadow-glow">
            <Truck className="w-6 h-6 text-sidebar-primary-foreground" />
          </div>
          {isOpen && (
            <div className="flex-1">
              <h1 className="font-bold text-lg">LogiAI</h1>
              <p className="text-xs text-sidebar-foreground/60">Optimizer</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id

          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-smooth group",
                isActive
                  ? "bg-sidebar-primary text-sidebar-primary-foreground shadow-glow"
                  : "text-sidebar-foreground hover:bg-sidebar-accent/20",
              )}
              title={item.label}
            >
              <Icon className="w-5 h-5 flex-shrink-0 transition-smooth group-hover:scale-110" />
              {isOpen && (
                <>
                  <div className="flex-1 text-left">
                    <div className="text-sm font-medium">{item.label}</div>
                    <div className="text-xs text-sidebar-foreground/50">{item.description}</div>
                  </div>
                  {isActive && <ChevronRight className="w-4 h-4 animate-slide-in-up" />}
                </>
              )}
            </button>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        {isOpen && (
          <div className="text-center space-y-1">
            <p className="text-xs text-sidebar-foreground/50">AI Supply Chain</p>
            <p className="text-xs text-sidebar-foreground/70 font-medium">Multi-Agent System</p>
          </div>
        )}
      </div>
    </aside>
  )
}

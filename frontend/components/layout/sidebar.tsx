"use client"

import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Brain,
  Truck,
  ChevronRight,
  Package,
  BarChart3,
  FileText,
  Settings,
  Zap,
} from "lucide-react"

import type { Page } from "@/app/page"

interface SidebarProps {
  isOpen: boolean
  currentPage: Page
  onPageChange: (page: Page) => void
}

const sections = [
  {
    title: "Operations",
    items: [
      { id: "optimizer" as Page, label: "Optimizer", icon: Zap, description: "Run Analysis" },
      { id: "shipments" as Page, label: "Shipments", icon: Package, description: "Track Orders" },
      { id: "vendors" as Page, label: "Routes", icon: Truck, description: "Map & Vendors" },
    ],
  },
  {
    title: "Intelligence",
    items: [
      { id: "analytics" as Page, label: "Analytics", icon: BarChart3, description: "Dashboard" },
      { id: "agents" as Page, label: "Agents", icon: Brain, description: "Performance" },
    ],
  },
  {
    title: "System",
    items: [
      { id: "reports" as Page, label: "Reports", icon: FileText, description: "Export Data" },
      { id: "settings" as Page, label: "Settings", icon: Settings, description: "Configuration" },
    ],
  },
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
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sidebar-primary to-sidebar-accent flex items-center justify-center shadow-glow">
            <Truck className="w-5 h-5 text-sidebar-primary-foreground" />
          </div>
          {isOpen && (
            <div className="flex-1">
              <h1 className="font-bold text-lg tracking-tight">LogiAI</h1>
              <p className="text-[10px] uppercase tracking-widest text-sidebar-foreground/50 font-medium">Supply Chain AI</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {sections.map((section) => (
          <div key={section.title} className="mb-3">
            {isOpen && (
              <p className="text-[10px] uppercase tracking-widest text-sidebar-foreground/40 font-semibold px-3 mb-2">
                {section.title}
              </p>
            )}
            <div className="space-y-0.5">
              {section.items.map((item) => {
                const Icon = item.icon
                const isActive = currentPage === item.id

                return (
                  <button
                    key={item.id}
                    onClick={() => onPageChange(item.id)}
                    className={cn(
                      "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-smooth group",
                      isActive
                        ? "bg-sidebar-primary text-sidebar-primary-foreground shadow-glow"
                        : "text-sidebar-foreground hover:bg-sidebar-accent/20",
                    )}
                    title={item.label}
                  >
                    <Icon className="w-[18px] h-[18px] flex-shrink-0 transition-smooth group-hover:scale-110" />
                    {isOpen && (
                      <>
                        <div className="flex-1 text-left">
                          <div className="text-sm font-medium leading-tight">{item.label}</div>
                          <div className={cn(
                            "text-[11px] leading-tight",
                            isActive ? "text-sidebar-primary-foreground/70" : "text-sidebar-foreground/45"
                          )}>{item.description}</div>
                        </div>
                        {isActive && <ChevronRight className="w-3.5 h-3.5 animate-slide-in-up" />}
                      </>
                    )}
                  </button>
                )
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        {isOpen ? (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center">
              <LayoutDashboard className="w-4 h-4 text-green-500" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-sidebar-foreground/80 truncate">AI Supply Chain</p>
              <p className="text-[10px] text-sidebar-foreground/50">v2.0 · Multi-Agent</p>
            </div>
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center">
              <LayoutDashboard className="w-4 h-4 text-green-500" />
            </div>
          </div>
        )}
      </div>
    </aside>
  )
}

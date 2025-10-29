"use client"

import { Card } from "@/components/ui/card"
import type { ReactNode } from "react"

interface MetricCard3DProps {
  title: string
  value: string | number
  subtitle?: string
  icon?: ReactNode
  trend?: {
    value: number
    direction: "up" | "down"
  }
  animated?: boolean
}

export function MetricCard3D({ title, value, subtitle, icon, trend, animated = true }: MetricCard3DProps) {
  return (
    <div
      className={`
        group relative
        ${animated ? "animate-float-3d" : ""}
      `}
      style={{
        perspective: "1000px",
      }}
    >
      <Card
        className={`
          relative p-6 bg-card border border-border
          transition-all duration-300
          hover:shadow-2xl hover:shadow-primary/20
          ${animated ? "animate-glow-pulse-3d" : ""}
        `}
        style={{
          transform: "translateZ(0)",
          transformStyle: "preserve-3d",
        }}
      >
        {/* Animated background gradient */}
        <div
          className="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          style={{
            background: "linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(251, 146, 60, 0.1) 100%)",
            pointerEvents: "none",
          }}
        />

        <div className="relative z-10 flex items-start justify-between">
          <div>
            <p className="text-sm text-muted-foreground font-medium">{title}</p>
            <p className="text-2xl font-bold text-foreground mt-2">{value}</p>
            {subtitle && <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>}
            {trend && (
              <p
                className={`text-xs mt-1 flex items-center gap-1 ${trend.direction === "up" ? "text-success" : "text-destructive"}`}
              >
                {trend.direction === "up" ? "↑" : "↓"} {Math.abs(trend.value)}%
              </p>
            )}
          </div>
          {icon && (
            <div
              className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300"
              style={{
                transform: "translateZ(10px)",
              }}
            >
              {icon}
            </div>
          )}
        </div>
      </Card>
    </div>
  )
}

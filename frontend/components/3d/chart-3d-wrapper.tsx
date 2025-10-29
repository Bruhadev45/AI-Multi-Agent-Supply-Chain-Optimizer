"use client"

import { Card } from "@/components/ui/card"
import type { ReactNode } from "react"

interface Chart3DWrapperProps {
  title: string
  children: ReactNode
  animated?: boolean
}

export function Chart3DWrapper({ title, children, animated = true }: Chart3DWrapperProps) {
  return (
    <div
      className={`
        group relative
        ${animated ? "animate-float-3d" : ""}
      `}
      style={{
        perspective: "1000px",
        animationDelay: "0.2s",
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
          animationDelay: "0.2s",
        }}
      >
        <div className="relative z-10">
          <h3 className="text-lg font-semibold text-foreground mb-4">{title}</h3>
          <div
            style={{
              transform: "translateZ(10px)",
            }}
          >
            {children}
          </div>
        </div>
      </Card>
    </div>
  )
}

"use client"

import type { ReactNode } from "react"

interface Card3DProps {
  children: ReactNode
  className?: string
  animated?: boolean
  glowing?: boolean
}

export function Card3D({ children, className = "", animated = true, glowing = false }: Card3DProps) {
  return (
    <div
      className={`
        relative perspective-3d
        ${animated ? "animate-float-3d" : ""}
        ${glowing ? "animate-glow-pulse-3d" : ""}
        ${className}
      `}
      style={{
        transformStyle: "preserve-3d",
      }}
    >
      <div
        className="relative"
        style={{
          transform: "translateZ(20px)",
        }}
      >
        {children}
      </div>
    </div>
  )
}

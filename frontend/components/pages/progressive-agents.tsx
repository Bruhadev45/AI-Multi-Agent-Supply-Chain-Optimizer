"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, Loader2, Clock, TrendingUp, MapPin, DollarSign, AlertTriangle, Brain } from "lucide-react"

interface AgentProgress {
  id: string
  name: string
  icon: any
  status: "pending" | "running" | "completed"
  output?: any
  duration?: number
}

interface ProgressiveAgentsProps {
  agents: AgentProgress[]
}

const AGENT_COLORS = {
  demand: "from-blue-500/10 to-blue-600/10 border-blue-500/30",
  route: "from-green-500/10 to-green-600/10 border-green-500/30",
  cost: "from-orange-500/10 to-orange-600/10 border-orange-500/30",
  risk: "from-red-500/10 to-red-600/10 border-red-500/30",
  coordinator: "from-purple-500/10 to-purple-600/10 border-purple-500/30",
}

const ICON_COLORS = {
  demand: "text-blue-500",
  route: "text-green-500",
  cost: "text-orange-500",
  risk: "text-red-500",
  coordinator: "text-purple-500",
}

export function ProgressiveAgents({ agents }: ProgressiveAgentsProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 mb-6">
        <div className="animate-pulse">
          <Brain className="w-8 h-8 text-primary" />
        </div>
        <div>
          <h2 className="text-2xl font-bold">AI Agents Processing</h2>
          <p className="text-sm text-muted-foreground">Watch each agent analyze your supply chain in real-time</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {agents.map((agent, index) => {
          const Icon = agent.icon
          const colorClass = AGENT_COLORS[agent.id as keyof typeof AGENT_COLORS] || "from-gray-500/10 to-gray-600/10 border-gray-500/30"
          const iconColor = ICON_COLORS[agent.id as keyof typeof ICON_COLORS] || "text-gray-500"

          return (
            <Card
              key={agent.id}
              className={`p-6 bg-gradient-to-br ${colorClass} border-2 transition-all duration-500 ${
                agent.status === "completed" ? "animate-scale-in" : ""
              } ${agent.status === "running" ? "shadow-glow animate-pulse" : ""}`}
            >
              <div className="flex items-start gap-4">
                {/* Agent Icon with Status */}
                <div className="relative flex-shrink-0">
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${colorClass.split(" ")[0]} ${colorClass.split(" ")[1]} flex items-center justify-center`}>
                    <Icon className={`w-8 h-8 ${iconColor}`} />
                  </div>

                  {/* Status Indicator */}
                  <div className="absolute -top-1 -right-1">
                    {agent.status === "pending" && (
                      <div className="w-6 h-6 rounded-full bg-gray-500/20 flex items-center justify-center">
                        <Clock className="w-4 h-4 text-gray-500" />
                      </div>
                    )}
                    {agent.status === "running" && (
                      <div className="w-6 h-6 rounded-full bg-primary flex items-center justify-center animate-spin">
                        <Loader2 className="w-4 h-4 text-primary-foreground" />
                      </div>
                    )}
                    {agent.status === "completed" && (
                      <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center animate-bounce">
                        <CheckCircle className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </div>
                </div>

                {/* Agent Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold">{agent.name}</h3>
                    <Badge
                      variant={
                        agent.status === "completed"
                          ? "default"
                          : agent.status === "running"
                          ? "secondary"
                          : "outline"
                      }
                      className="capitalize"
                    >
                      {agent.status === "running" ? "Processing..." : agent.status}
                    </Badge>
                  </div>

                  {/* Agent Output */}
                  {agent.status === "completed" && agent.output && (
                    <div className="bg-background/50 backdrop-blur-sm rounded-lg p-4 space-y-2 animate-slide-in-up">
                      <div className="text-sm font-medium text-muted-foreground mb-2">Analysis Results:</div>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {Object.entries(agent.output).map(([key, value]) => (
                          <div key={key} className="space-y-1">
                            <div className="text-xs text-muted-foreground capitalize">
                              {key.replace(/_/g, " ")}
                            </div>
                            <div className="text-base font-semibold">
                              {typeof value === "number"
                                ? value.toFixed(2)
                                : typeof value === "object"
                                ? JSON.stringify(value).substring(0, 30) + "..."
                                : String(value)}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Running Message */}
                  {agent.status === "running" && (
                    <p className="text-sm text-muted-foreground animate-pulse">
                      Analyzing data and generating insights...
                    </p>
                  )}

                  {/* Pending Message */}
                  {agent.status === "pending" && (
                    <p className="text-sm text-muted-foreground">
                      Waiting for previous agents to complete...
                    </p>
                  )}

                  {/* Duration */}
                  {agent.status === "completed" && agent.duration && (
                    <div className="mt-2 text-xs text-muted-foreground">
                      Completed in {agent.duration.toFixed(2)}s
                    </div>
                  )}
                </div>
              </div>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

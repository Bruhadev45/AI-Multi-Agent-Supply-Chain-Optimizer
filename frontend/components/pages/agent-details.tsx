"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Brain } from "lucide-react"
import { AnalysisResponse } from "@/lib/api-client"

interface AgentDetailsProps {
  analysisData: AnalysisResponse | null
}

const demandData = [
  { week: "W1", forecast: 1200, actual: 1100 },
  { week: "W2", forecast: 1400, actual: 1350 },
  { week: "W3", forecast: 1600, actual: 1650 },
  { week: "W4", forecast: 1800, actual: 1750 },
]

const agents = [
  { id: "demand", name: "Demand Forecasting", status: "active", accuracy: "94%" },
  { id: "route", name: "Route Optimizer", status: "active", accuracy: "98%" },
  { id: "cost", name: "Cost Analyst", status: "active", accuracy: "91%" },
  { id: "risk", name: "Risk Monitor", status: "active", accuracy: "87%" },
  { id: "coordinator", name: "Strategic Coordinator", status: "active", accuracy: "95%" },
]

export function AgentDetails({ analysisData }: AgentDetailsProps) {
  const [selectedAgent, setSelectedAgent] = useState("demand")

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Agent Details</h1>
        <p className="text-muted-foreground mt-1">Monitor AI agent performance and insights</p>
      </div>

      {/* Agent Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {agents.map((agent) => (
          <button
            key={agent.id}
            onClick={() => setSelectedAgent(agent.id)}
            className={`px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
              selectedAgent === agent.id
                ? "bg-primary text-primary-foreground"
                : "bg-card border border-border text-foreground hover:border-primary"
            }`}
          >
            {agent.name}
          </button>
        ))}
      </div>

      {/* Agent Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Metrics */}
        <div className="lg:col-span-1 space-y-4">
          <Card className="p-6 bg-card border border-border">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Brain className="w-5 h-5 text-primary" />
              </div>
              <h3 className="font-semibold text-foreground">Agent Status</h3>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-muted-foreground">Status</p>
                <p className="text-lg font-semibold text-success">Active</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Accuracy</p>
                <p className="text-lg font-semibold text-foreground">94%</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Last Updated</p>
                <p className="text-sm text-foreground">2 minutes ago</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 bg-card border border-border">
            <h3 className="font-semibold text-foreground mb-4">Key Metrics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Predictions</span>
                <span className="font-semibold text-foreground">1,245</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Avg Error</span>
                <span className="font-semibold text-foreground">3.2%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Processing Time</span>
                <span className="font-semibold text-foreground">245ms</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Chart */}
        <Card className="lg:col-span-2 p-6 bg-card border border-border">
          <h3 className="text-lg font-semibold text-foreground mb-4">Demand Forecast vs Actual</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={demandData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis stroke="var(--color-muted-foreground)" />
              <YAxis stroke="var(--color-muted-foreground)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--color-card)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                }}
              />
              <Line type="monotone" dataKey="forecast" stroke="var(--color-chart-2)" strokeWidth={2} />
              <Line type="monotone" dataKey="actual" stroke="var(--color-chart-4)" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Agent Logs */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4">Agent Activity Log</h3>
        <div className="space-y-3">
          {[
            { time: "14:32", message: "Demand forecast updated for Q2", type: "info" },
            { time: "14:15", message: "Anomaly detected in historical data", type: "warning" },
            { time: "14:00", message: "Optimization cycle completed", type: "success" },
            { time: "13:45", message: "Processing new vendor data", type: "info" },
          ].map((log, i) => (
            <div key={i} className="flex gap-4 pb-3 border-b border-border last:border-0">
              <span className="text-sm text-muted-foreground min-w-fit">{log.time}</span>
              <div className="flex-1">
                <p className="text-sm text-foreground">{log.message}</p>
              </div>
              <div
                className={`w-2 h-2 rounded-full mt-1.5 ${
                  log.type === "success" ? "bg-success" : log.type === "warning" ? "bg-warning" : "bg-primary"
                }`}
              />
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}

"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { Brain, TrendingUp, MapPin, DollarSign, AlertTriangle, CheckCircle, Clock, Activity } from "lucide-react"
import { AnalysisResponse } from "@/lib/api-client"

interface EnhancedAgentDetailsProps {
  analysisData: AnalysisResponse | null
}

const AGENT_COLORS = {
  demand: "#3b82f6",
  route: "#10b981",
  cost: "#f59e0b",
  risk: "#ef4444",
  coordinator: "#8b5cf6",
}

export function EnhancedAgentDetails({ analysisData }: EnhancedAgentDetailsProps) {
  // Agent configuration
  const agents = [
    {
      id: "demand",
      name: "Demand Forecast Agent",
      icon: TrendingUp,
      color: AGENT_COLORS.demand,
      description: "ARIMA-based time series forecasting",
      status: analysisData?.execution_metadata.success_rates.demand ? "active" : "idle",
      metrics: {
        accuracy: "94%",
        avgTime: "2.3s",
        successRate: analysisData?.execution_metadata.success_rates.demand ? "100%" : "0%",
      },
      output: analysisData
        ? {
            forecast: analysisData.forecast,
            original: analysisData.forecast_original,
            impact: ((analysisData.forecast / analysisData.forecast_original - 1) * 100).toFixed(1),
          }
        : null,
    },
    {
      id: "route",
      name: "Route Optimizer Agent",
      icon: MapPin,
      color: AGENT_COLORS.route,
      description: "Google Maps API integration for optimal routes",
      status: analysisData?.execution_metadata.success_rates.route ? "active" : "idle",
      metrics: {
        accuracy: "98%",
        avgTime: "3.1s",
        successRate: analysisData?.execution_metadata.success_rates.route ? "100%" : "0%",
      },
      output: analysisData
        ? {
            distance: analysisData.route_info.distance_km,
            duration: analysisData.route_info.duration,
            source: analysisData.route_info.source,
          }
        : null,
    },
    {
      id: "cost",
      name: "Cost Analyzer Agent",
      icon: DollarSign,
      color: AGENT_COLORS.cost,
      description: "Multi-vendor cost comparison & optimization",
      status: analysisData?.execution_metadata.success_rates.cost ? "active" : "idle",
      metrics: {
        accuracy: "91%",
        avgTime: "1.2s",
        successRate: analysisData?.execution_metadata.success_rates.cost ? "100%" : "0%",
      },
      output: analysisData
        ? {
            vendor: analysisData.best_vendor,
            cost: analysisData.best_price,
            savings: analysisData.original_price - analysisData.best_price,
            vendorCount: analysisData.all_vendors?.length || 0,
          }
        : null,
    },
    {
      id: "risk",
      name: "Risk Monitor Agent",
      icon: AlertTriangle,
      color: AGENT_COLORS.risk,
      description: "Weather & operational risk assessment",
      status: analysisData?.execution_metadata.success_rates.risk ? "active" : "idle",
      metrics: {
        accuracy: "87%",
        avgTime: "4.2s",
        successRate: analysisData?.execution_metadata.success_rates.risk ? "100%" : "0%",
      },
      output: analysisData
        ? {
            level: analysisData.risk.risk_level,
            condition: analysisData.risk.condition,
            temp: analysisData.risk.temp,
            humidity: analysisData.risk.humidity,
          }
        : null,
    },
    {
      id: "coordinator",
      name: "Strategic Coordinator",
      icon: Brain,
      color: AGENT_COLORS.coordinator,
      description: "CrewAI multi-agent orchestration",
      status: analysisData ? "active" : "idle",
      metrics: {
        accuracy: "95%",
        avgTime: "5.8s",
        successRate: analysisData ? "100%" : "0%",
      },
      output: analysisData
        ? {
            confidence: analysisData.recommendations_confidence.score,
            level: analysisData.recommendations_confidence.level,
            executionTime: analysisData.execution_metadata.total_time_seconds,
          }
        : null,
    },
  ]

  // Performance data for charts
  const performanceData = agents.map((agent) => ({
    name: agent.name.split(" ")[0],
    accuracy: parseFloat(agent.metrics.accuracy),
    time: parseFloat(agent.metrics.avgTime),
  }))

  // Execution timeline
  const timelineData = analysisData?.execution_metadata.execution_log
    ?.slice(-8)
    .map((log, index) => ({
      step: `Step ${index + 1}`,
      duration: log.duration_seconds,
      status: log.status === "SUCCESS" ? 1 : 0,
    })) || []

  // Status distribution
  const statusData = [
    { name: "Success", value: agents.filter((a) => a.status === "active").length, color: "#10b981" },
    { name: "Idle", value: agents.filter((a) => a.status === "idle").length, color: "#6b7280" },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
          Agent Performance Dashboard
        </h1>
        <p className="text-muted-foreground mt-1">Monitor AI agent performance and execution metrics</p>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-6 bg-gradient-to-br from-blue-500/10 to-blue-600/10 border-2 border-blue-500/30">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">System Status</div>
              <div className="text-2xl font-bold mt-1">
                {analysisData?.system_health.overall_health || "🟡 Ready"}
              </div>
            </div>
            <Activity className="w-10 h-10 text-blue-500" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-to-br from-green-500/10 to-green-600/10 border-2 border-green-500/30">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">Success Rate</div>
              <div className="text-2xl font-bold mt-1">
                {analysisData?.system_health.success_rate || "N/A"}
              </div>
            </div>
            <CheckCircle className="w-10 h-10 text-green-500" />
          </div>
        </Card>

        <Card className="p-6 bg-gradient-to-br from-purple-500/10 to-purple-600/10 border-2 border-purple-500/30">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">Avg Response Time</div>
              <div className="text-2xl font-bold mt-1">
                {analysisData?.system_health.avg_response_time || "N/A"}
              </div>
            </div>
            <Clock className="w-10 h-10 text-purple-500" />
          </div>
        </Card>
      </div>

      {/* Agent Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {agents.map((agent) => (
          <Card key={agent.id} className="p-6 border-2 hover:shadow-lg transition-all">
            <div className="space-y-4">
              {/* Agent Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className="p-3 rounded-lg"
                    style={{ backgroundColor: `${agent.color}20`, color: agent.color }}
                  >
                    <agent.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">{agent.name}</h3>
                    <p className="text-sm text-muted-foreground">{agent.description}</p>
                  </div>
                </div>
                <Badge variant={agent.status === "active" ? "default" : "secondary"}>
                  {agent.status}
                </Badge>
              </div>

              {/* Agent Metrics */}
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className="text-xs text-muted-foreground">Accuracy</div>
                  <div className="text-lg font-semibold">{agent.metrics.accuracy}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Avg Time</div>
                  <div className="text-lg font-semibold">{agent.metrics.avgTime}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Success</div>
                  <div className="text-lg font-semibold">{agent.metrics.successRate}</div>
                </div>
              </div>

              {/* Agent Output */}
              {agent.output && (
                <div className="bg-muted/50 p-4 rounded-lg">
                  <div className="text-xs font-semibold text-muted-foreground mb-2">Latest Output</div>
                  <div className="space-y-1 text-sm">
                    {Object.entries(agent.output).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-muted-foreground capitalize">{key}:</span>
                        <span className="font-medium">{typeof value === "number" ? value.toFixed(2) : value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Performance Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Accuracy Chart */}
        <Card className="p-6 border-2">
          <h3 className="text-lg font-semibold mb-4">Agent Accuracy</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis dataKey="name" stroke="var(--color-muted-foreground)" />
              <YAxis stroke="var(--color-muted-foreground)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--color-card)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                }}
              />
              <Bar dataKey="accuracy" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Response Time Chart */}
        <Card className="p-6 border-2">
          <h3 className="text-lg font-semibold mb-4">Response Time</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis dataKey="name" stroke="var(--color-muted-foreground)" />
              <YAxis stroke="var(--color-muted-foreground)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--color-card)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                }}
              />
              <Line type="monotone" dataKey="time" stroke="#10b981" strokeWidth={3} dot={{ r: 5 }} />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Status Distribution */}
        <Card className="p-6 border-2">
          <h3 className="text-lg font-semibold mb-4">Agent Status Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={statusData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value">
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center gap-6 mt-4">
            {statusData.map((item) => (
              <div key={item.name} className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-sm">
                  {item.name}: {item.value}
                </span>
              </div>
            ))}
          </div>
        </Card>

        {/* Execution Timeline */}
        {timelineData.length > 0 && (
          <Card className="p-6 border-2">
            <h3 className="text-lg font-semibold mb-4">Execution Timeline</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis dataKey="step" stroke="var(--color-muted-foreground)" />
                <YAxis stroke="var(--color-muted-foreground)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--color-card)",
                    border: "1px solid var(--color-border)",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="duration" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        )}
      </div>

      {/* Execution Log */}
      {analysisData && (
        <Card className="p-6 border-2">
          <h3 className="text-lg font-semibold mb-4">Recent Execution Log</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {analysisData.execution_metadata.execution_log.slice(-10).map((log, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-muted/50 rounded-lg text-sm"
              >
                <div className="flex items-center gap-3">
                  {log.status === "SUCCESS" ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <AlertTriangle className="w-4 h-4 text-orange-500" />
                  )}
                  <span className="font-medium">{log.step}</span>
                </div>
                <div className="flex items-center gap-4 text-muted-foreground">
                  <span>{log.duration_seconds.toFixed(2)}s</span>
                  <span className="text-xs">{new Date(log.timestamp).toLocaleTimeString()}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* No Data State */}
      {!analysisData && (
        <Card className="p-12 text-center border-2 border-dashed">
          <Brain className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Analysis Data</h3>
          <p className="text-muted-foreground">
            Run an optimization from the main page to see detailed agent performance metrics
          </p>
        </Card>
      )}
    </div>
  )
}

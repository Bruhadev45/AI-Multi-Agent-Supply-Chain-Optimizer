"use client"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts"
import { AlertCircle, CheckCircle, Clock, Zap, Loader2 } from "lucide-react"
import { MetricCard3D } from "@/components/3d/metric-card-3d"
import { Chart3DWrapper } from "@/components/3d/chart-3d-wrapper"
import { AnimatedBackground } from "@/components/3d/animated-background"
import { AnalysisResponse } from "@/lib/api-client"

interface DashboardProps {
  analysisData: AnalysisResponse | null
  loading: boolean
}

const costData = [
  { month: "Jan", cost: 4000, savings: 2400 },
  { month: "Feb", cost: 3000, savings: 1398 },
  { month: "Mar", cost: 2000, savings: 9800 },
  { month: "Apr", cost: 2780, savings: 3908 },
  { month: "May", cost: 1890, savings: 4800 },
  { month: "Jun", cost: 2390, savings: 3800 },
]

const riskData = [
  { name: "Low Risk", value: 60, color: "#4ade80" },
  { name: "Medium Risk", value: 25, color: "#facc15" },
  { name: "High Risk", value: 15, color: "#ef4444" },
]

const efficiencyData = [
  { week: "W1", efficiency: 78 },
  { week: "W2", efficiency: 82 },
  { week: "W3", efficiency: 88 },
  { week: "W4", efficiency: 92 },
  { week: "W5", efficiency: 94 },
]

export function Dashboard({ analysisData, loading }: DashboardProps) {
  // If loading, show loading state
  if (loading) {
    return (
      <div className="space-y-8 relative">
        <AnimatedBackground />
        <div className="flex flex-col items-center justify-center min-h-[400px]">
          <Loader2 className="w-12 h-12 animate-spin text-primary mb-4" />
          <h2 className="text-xl font-semibold text-foreground">Running Analysis...</h2>
          <p className="text-muted-foreground mt-2">AI agents are processing your request</p>
        </div>
      </div>
    )
  }

  // Use real data if available, otherwise use demo data
  const displayData = analysisData || null
  return (
    <div className="space-y-8 relative">
      <AnimatedBackground />

      <div className="animate-fade-in">
        <h1 className="text-4xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground mt-2 text-base">Real-time supply chain insights and optimization metrics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="animate-slide-in-up" style={{ animationDelay: "0ms" }}>
          <MetricCard3D
            title="Current Scenario"
            value={displayData?.scenario_applied || "No analysis yet"}
            subtitle={displayData ? `${displayData.route_info?.path?.[0] || 'Origin'} → ${displayData.route_info?.path?.[displayData.route_info.path.length - 1] || 'Destination'}` : "Run analysis to see data"}
            icon={<Zap className="w-5 h-5 text-primary" />}
            animated
          />
        </div>

        <div className="animate-slide-in-up" style={{ animationDelay: "100ms" }}>
          <MetricCard3D
            title="Total Cost"
            value={displayData ? `₹${(displayData.best_price / 1000).toFixed(1)}K` : "₹0"}
            subtitle={displayData?.best_vendor || "No vendor selected"}
            icon={<CheckCircle className="w-5 h-5 text-success" />}
            trend={displayData && displayData.original_price !== displayData.best_price ? {
              value: Math.round(((displayData.original_price - displayData.best_price) / displayData.original_price) * 100),
              direction: "down" as const
            } : undefined}
            animated
          />
        </div>

        <div className="animate-slide-in-up" style={{ animationDelay: "200ms" }}>
          <MetricCard3D
            title="Risk Level"
            value={displayData?.risk?.risk_level || "Unknown"}
            subtitle={displayData?.risk?.condition || "No risk data"}
            icon={<AlertCircle className="w-5 h-5 text-warning" />}
            animated
          />
        </div>

        <div className="animate-slide-in-up" style={{ animationDelay: "300ms" }}>
          <MetricCard3D
            title="Demand Forecast"
            value={displayData ? `${(displayData.forecast).toFixed(0)}` : "0"}
            subtitle={displayData ? `${displayData.route_info?.distance_km?.toFixed(0) || '0'} km route` : "No forecast"}
            icon={<Clock className="w-5 h-5 text-accent" />}
            trend={displayData && displayData.forecast !== displayData.forecast_original ? {
              value: Math.round(((displayData.forecast - displayData.forecast_original) / displayData.forecast_original) * 100),
              direction: displayData.forecast > displayData.forecast_original ? "up" as const : "down" as const
            } : undefined}
            animated
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cost vs Savings Chart */}
        <Chart3DWrapper title="Cost Analysis" animated>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={costData}>
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
              <Legend />
              <Bar dataKey="cost" fill="var(--color-chart-2)" radius={[8, 8, 0, 0]} />
              <Bar dataKey="savings" fill="var(--color-chart-4)" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Chart3DWrapper>

        {/* Risk Distribution */}
        <Chart3DWrapper title="Risk Distribution" animated>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {riskData.map((item) => (
              <div key={item.name} className="flex items-center gap-2 text-sm">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-muted-foreground">
                  {item.name}: {item.value}%
                </span>
              </div>
            ))}
          </div>
        </Chart3DWrapper>

        <Chart3DWrapper title="Efficiency Trend" animated>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={efficiencyData}>
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
              <Line
                type="monotone"
                dataKey="efficiency"
                stroke="var(--color-chart-1)"
                strokeWidth={3}
                dot={{ fill: "var(--color-chart-1)", r: 5 }}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Chart3DWrapper>
      </div>

      {/* Route Map Placeholder */}
      <Chart3DWrapper title="Optimal Route Map" animated>
        <div className="w-full h-96 bg-gradient-to-br from-muted to-muted/50 rounded-lg flex items-center justify-center relative overflow-hidden">
          {/* Animated route visualization */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="relative w-full h-full">
              {/* Animated route line */}
              <svg className="absolute inset-0 w-full h-full" style={{ opacity: 0.3 }}>
                <defs>
                  <linearGradient id="routeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="var(--color-primary)" />
                    <stop offset="100%" stopColor="var(--color-accent)" />
                  </linearGradient>
                </defs>
                <path
                  d="M 50 50 Q 200 100 350 80 T 600 120"
                  stroke="url(#routeGradient)"
                  strokeWidth="3"
                  fill="none"
                  strokeDasharray="1000"
                  strokeDashoffset="1000"
                  style={{
                    animation: "dash 8s linear infinite",
                  }}
                />
              </svg>
            </div>
          </div>

          <div className="text-center relative z-10">
            <p className="text-muted-foreground">Map integration coming soon</p>
            <p className="text-sm text-muted-foreground mt-1">Delhi → Mumbai via NH48</p>
          </div>
        </div>
      </Chart3DWrapper>

      <style>{`
        @keyframes dash {
          to {
            stroke-dashoffset: 0;
          }
        }
      `}</style>
    </div>
  )
}

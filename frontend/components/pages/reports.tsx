"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Download, FileText, BarChart3, TrendingDown, Clock, Shield, Leaf, FileJson, Printer, ArrowRight } from "lucide-react"
import { AnalysisResponse } from "@/lib/api-client"

interface ReportsProps {
  analysisData: AnalysisResponse | null
  analysisHistory?: Array<{ data: AnalysisResponse; timestamp: string }>
}

export function Reports({ analysisData, analysisHistory = [] }: ReportsProps) {
  const exportAsJSON = () => {
    if (!analysisData) return
    const jsonString = JSON.stringify(analysisData, null, 2)
    const blob = new Blob([jsonString], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `analysis-report-${new Date().toISOString().split("T")[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const exportAsCSV = () => {
    if (!analysisData?.all_vendors?.length) return
    const headers = Object.keys(analysisData.all_vendors[0]).join(",")
    const rows = analysisData.all_vendors.map(v => Object.values(v).join(",")).join("\n")
    const csv = `${headers}\n${rows}`
    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `vendor-comparison-${new Date().toISOString().split("T")[0]}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const savings = analysisData
    ? Math.max(0, analysisData.original_price - analysisData.best_price)
    : 0
  const savingsPct = analysisData && analysisData.original_price > 0
    ? ((savings / analysisData.original_price) * 100).toFixed(1)
    : "0"

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Reports & Exports</h1>
        <p className="text-muted-foreground mt-1">View optimization insights and export analysis data</p>
      </div>

      {/* KPI Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          {
            label: "Cost Savings",
            value: analysisData ? `₹${savings.toLocaleString()}` : "--",
            sub: analysisData ? `${savingsPct}% vs baseline` : "Run analysis first",
            icon: TrendingDown,
            color: "text-emerald-500",
            bg: "bg-emerald-500/10",
          },
          {
            label: "Processing Time",
            value: analysisData ? `${analysisData.execution_metadata.total_time_seconds.toFixed(2)}s` : "--",
            sub: analysisData ? "All agents completed" : "No data",
            icon: Clock,
            color: "text-blue-500",
            bg: "bg-blue-500/10",
          },
          {
            label: "Risk Level",
            value: analysisData?.risk?.risk_level?.replace(/[^\w\s]/g, "").trim() || "--",
            sub: analysisData?.risk?.condition || "No assessment",
            icon: Shield,
            color: "text-amber-500",
            bg: "bg-amber-500/10",
          },
          {
            label: "Eco Score",
            value: analysisData?.all_vendors?.length
              ? `${Math.round((1 - (analysisData.all_vendors.reduce((a: number, v: any) => a + (v.emission_per_km || 0), 0) / analysisData.all_vendors.length)) * 100)}%`
              : "--",
            sub: "Avg emission reduction",
            icon: Leaf,
            color: "text-green-500",
            bg: "bg-green-500/10",
          },
        ].map((kpi) => (
          <Card key={kpi.label} className="p-5 bg-card border border-border">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">{kpi.label}</p>
                <p className="text-2xl font-bold text-foreground mt-1">{kpi.value}</p>
                <p className="text-xs text-muted-foreground mt-1">{kpi.sub}</p>
              </div>
              <div className={`p-2 rounded-lg ${kpi.bg}`}>
                <kpi.icon className={`w-4 h-4 ${kpi.color}`} />
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Export Actions */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4">Export Options</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <Button
            onClick={exportAsJSON}
            disabled={!analysisData}
            className="h-auto py-4 flex items-center gap-3 bg-primary text-primary-foreground hover:bg-primary/90 justify-start px-5"
          >
            <FileJson className="w-5 h-5" />
            <div className="text-left">
              <div className="font-medium">Export JSON</div>
              <div className="text-xs opacity-80">Full analysis data</div>
            </div>
          </Button>
          <Button
            onClick={exportAsCSV}
            disabled={!analysisData?.all_vendors?.length}
            variant="secondary"
            className="h-auto py-4 flex items-center gap-3 justify-start px-5"
          >
            <FileText className="w-5 h-5" />
            <div className="text-left">
              <div className="font-medium">Export CSV</div>
              <div className="text-xs opacity-60">Vendor comparison</div>
            </div>
          </Button>
          <Button
            onClick={() => window.print()}
            variant="outline"
            className="h-auto py-4 flex items-center gap-3 justify-start px-5"
          >
            <Printer className="w-5 h-5" />
            <div className="text-left">
              <div className="font-medium">Print Report</div>
              <div className="text-xs opacity-60">Browser print dialog</div>
            </div>
          </Button>
        </div>
      </Card>

      {/* Analysis History */}
      <Card className="p-6 bg-card border border-border">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground">Analysis History</h3>
          <Badge variant="outline" className="text-xs">
            {analysisHistory.length} {analysisHistory.length === 1 ? "run" : "runs"} this session
          </Badge>
        </div>
        {analysisHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Scenario</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Time</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Route</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Vendor</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Cost</th>
                  <th className="text-left py-3 px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody>
                {analysisHistory.map((entry, i) => {
                  const d = entry.data
                  const path = d.route_info?.path || []
                  const route = path.length >= 2 ? `${path[0]} → ${path[path.length - 1]}` : "N/A"
                  const time = new Date(entry.timestamp).toLocaleTimeString()
                  return (
                    <tr key={i} className="border-b border-border hover:bg-muted/50 transition-colors">
                      <td className="py-3 px-4 text-sm text-foreground font-medium">{d.scenario_applied}</td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">{time}</td>
                      <td className="py-3 px-4 text-sm text-foreground flex items-center gap-1">
                        {route}
                        <ArrowRight className="w-3 h-3 text-muted-foreground" />
                        <span className="text-muted-foreground">{d.route_info?.distance_km?.toFixed(0)} km</span>
                      </td>
                      <td className="py-3 px-4 text-sm text-foreground">{d.best_vendor}</td>
                      <td className="py-3 px-4 text-sm text-foreground font-medium">₹{d.best_price.toLocaleString()}</td>
                      <td className="py-3 px-4">
                        <Badge variant="outline" className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20 text-xs">
                          Completed
                        </Badge>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <BarChart3 className="w-10 h-10 text-muted-foreground/30 mx-auto mb-3" />
            <p className="text-muted-foreground text-sm">No analysis runs yet this session</p>
            <p className="text-xs text-muted-foreground/60 mt-1">Run an optimization from the Optimizer page to see history here</p>
          </div>
        )}
      </Card>
    </div>
  )
}

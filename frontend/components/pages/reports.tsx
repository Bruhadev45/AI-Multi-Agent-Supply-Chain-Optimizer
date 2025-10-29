"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Download, FileText, BarChart3 } from "lucide-react"
import { AnalysisResponse } from "@/lib/api-client"

interface ReportsProps {
  analysisData: AnalysisResponse | null
}

export function Reports({ analysisData }: ReportsProps) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Reports</h1>
        <p className="text-muted-foreground mt-1">View and export optimization reports</p>
      </div>

      {/* Current Report Summary */}
      <Card className="p-8 bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <p className="text-sm text-muted-foreground mb-2">Cost Savings</p>
            <p className="text-3xl font-bold text-foreground">24.5%</p>
            <p className="text-xs text-success mt-1">vs baseline</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-2">Delay Reduction</p>
            <p className="text-3xl font-bold text-foreground">18.3%</p>
            <p className="text-xs text-success mt-1">faster delivery</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-2">Risk Mitigation</p>
            <p className="text-3xl font-bold text-foreground">42%</p>
            <p className="text-xs text-success mt-1">lower risk</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-2">Sustainability</p>
            <p className="text-3xl font-bold text-foreground">31%</p>
            <p className="text-xs text-success mt-1">emissions reduced</p>
          </div>
        </div>
      </Card>

      {/* Export Options */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Button className="h-auto py-6 flex flex-col items-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
          <Download className="w-6 h-6" />
          <span>Export as PDF</span>
        </Button>
        <Button className="h-auto py-6 flex flex-col items-center gap-2 bg-secondary text-secondary-foreground hover:bg-secondary/90">
          <FileText className="w-6 h-6" />
          <span>Export as CSV</span>
        </Button>
        <Button className="h-auto py-6 flex flex-col items-center gap-2 bg-accent text-accent-foreground hover:bg-accent/90">
          <BarChart3 className="w-6 h-6" />
          <span>Print Report</span>
        </Button>
      </div>

      {/* Past Scenarios */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4">Past Scenarios</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 font-semibold text-foreground">Scenario</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Date</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Route</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Cost Savings</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Status</th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  scenario: "Peak Season",
                  date: "2024-10-15",
                  route: "Delhi → Mumbai",
                  savings: "₹24.5K",
                  status: "Completed",
                },
                {
                  scenario: "Weather Disruption",
                  date: "2024-10-10",
                  route: "Bangalore → Chennai",
                  savings: "₹18.2K",
                  status: "Completed",
                },
                {
                  scenario: "Cost Optimization",
                  date: "2024-10-05",
                  route: "Pune → Hyderabad",
                  savings: "₹31.8K",
                  status: "Completed",
                },
                {
                  scenario: "Vendor Failure",
                  date: "2024-09-28",
                  route: "Delhi → Jaipur",
                  savings: "₹12.5K",
                  status: "Completed",
                },
              ].map((item, i) => (
                <tr key={i} className="border-b border-border hover:bg-muted/50 transition-colors">
                  <td className="py-4 px-4 text-foreground font-medium">{item.scenario}</td>
                  <td className="py-4 px-4 text-foreground">{item.date}</td>
                  <td className="py-4 px-4 text-foreground">{item.route}</td>
                  <td className="py-4 px-4 text-success font-medium">{item.savings}</td>
                  <td className="py-4 px-4">
                    <span className="px-3 py-1 rounded-full bg-success/10 text-success text-sm font-medium">
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

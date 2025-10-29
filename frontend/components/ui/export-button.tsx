"use client"

import { Download, FileJson, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

interface ExportButtonProps {
  data: any
  filename?: string
}

export function ExportButton({ data, filename = "analysis-results" }: ExportButtonProps) {
  const exportAsJSON = () => {
    const jsonString = JSON.stringify(data, null, 2)
    const blob = new Blob([jsonString], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `${filename}-${new Date().toISOString().split("T")[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const exportAsText = () => {
    // Format data as readable text
    const textContent = formatDataAsText(data)
    const blob = new Blob([textContent], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `${filename}-${new Date().toISOString().split("T")[0]}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const printReport = () => {
    window.print()
  }

  const formatDataAsText = (data: any): string => {
    let text = "=== AI SUPPLY CHAIN OPTIMIZATION REPORT ===\n\n"
    text += `Generated: ${new Date().toLocaleString()}\n\n`

    if (data.route_info) {
      text += "--- ROUTE INFORMATION ---\n"
      text += `Path: ${data.route_info.path.join(" → ")}\n`
      text += `Distance: ${data.route_info.distance_km.toFixed(2)} km\n`
      text += `Duration: ${data.route_info.duration}\n\n`
    }

    if (data.forecast !== undefined) {
      text += "--- DEMAND FORECAST ---\n"
      text += `Forecasted Units: ${data.forecast.toFixed(0)}\n`
      text += `Original Forecast: ${data.forecast_original.toFixed(0)}\n`
      text += `Scenario Applied: ${data.scenario_applied}\n\n`
    }

    if (data.best_vendor) {
      text += "--- COST ANALYSIS ---\n"
      text += `Best Vendor: ${data.best_vendor}\n`
      text += `Best Price: ₹${data.best_price.toLocaleString()}\n`
      text += `Original Price: ₹${data.original_price.toLocaleString()}\n`
      text += `Savings: ₹${(data.original_price - data.best_price).toLocaleString()}\n\n`
    }

    if (data.risk) {
      text += "--- RISK ASSESSMENT ---\n"
      text += `Risk Level: ${data.risk.risk_level}\n`
      text += `Condition: ${data.risk.condition}\n\n`
    }

    if (data.crew_reasoning) {
      text += "--- AI RECOMMENDATIONS ---\n"
      text += `${data.crew_reasoning}\n\n`
    }

    if (data.recommendations_confidence) {
      text += "--- CONFIDENCE METRICS ---\n"
      text += `Overall Score: ${data.recommendations_confidence.score}\n`
      text += `Rationale: ${data.recommendations_confidence.rationale}\n\n`
    }

    if (data.execution_metadata) {
      text += "--- EXECUTION DETAILS ---\n"
      text += `Total Time: ${data.execution_metadata.total_time_seconds.toFixed(2)}s\n`
      text += `Timestamp: ${data.execution_metadata.timestamp}\n`
    }

    return text
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <Download className="w-4 h-4" />
          Export Results
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <DropdownMenuItem onClick={exportAsJSON} className="gap-2 cursor-pointer">
          <FileJson className="w-4 h-4" />
          Export as JSON
        </DropdownMenuItem>
        <DropdownMenuItem onClick={exportAsText} className="gap-2 cursor-pointer">
          <FileText className="w-4 h-4" />
          Export as Text
        </DropdownMenuItem>
        <DropdownMenuItem onClick={printReport} className="gap-2 cursor-pointer">
          <FileText className="w-4 h-4" />
          Print Report
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

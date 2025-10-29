"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, Target, TrendingUp, AlertCircle, DollarSign, MapPin, CheckCircle2 } from "lucide-react"

interface StrategicRecommendationsProps {
  reasoning: string
  confidence: {
    score: string
    level: string
  }
  executionTime?: number
}

export function StrategicRecommendations({ reasoning, confidence, executionTime }: StrategicRecommendationsProps) {
  // Utility: Clean markdown from a line/string
  const cleanMarkdown = (line: string) => {
    if (!line) return ""
    return line
      // Remove bold/italic/backticks/headers/blockquote markers and stray asterisks/underscores
      .replace(/\*\*(.*?)\*\*/g, "$1")    // **bold**
      .replace(/\*(.*?)\*/g, "$1")        // *italic* (simple)
      .replace(/_(.*?)_/g, "$1")          // _italic_
      .replace(/`(.*?)`/g, "$1")          // `code`
      .replace(/^#{1,6}\s*/gm, "")        // # headers at line start
      .replace(/^[>\-\*\+]\s*/gm, "")     // blockquote or list bullet at line start
      .replace(/\[(.*?)\]\((.*?)\)/g, "$1") // [text](link)
      .replace(/[~]{1,2}/g, "")           // ~strike~ or ~~strike~~
      .replace(/:{2,}/g, ":")             // clean double colons if any
      .replace(/[*_`>#]+/g, "")           // any remaining markdown symbols
      .trim()
  }

  // Parse recommendations after cleaning the markdown from the whole text
  const parseRecommendations = (text: string) => {
    if (!text) return []

    // Clean the entire reasoning first to remove markdown artifacts
    const cleanedText = cleanMarkdown(text)

    // Split cleaned text by newlines, bullets, or sentence endings
    const sentences = cleanedText
      .split(/\n+|(?:\d+\.)|(?:[-••\u2022])/)
      .map(s => s.trim())
      .filter(s => s.length > 25) // keep only substantial items
      .slice(0, 8)

    return sentences.map(sentence => {
      const lower = sentence.toLowerCase()
      let category = "General"
      let icon = Target
      let color = "text-blue-500"

      if (lower.includes("cost") || lower.includes("price") || lower.includes("save") || lower.includes("investment")) {
        category = "Cost Optimization"
        icon = DollarSign
        color = "text-green-500"
      } else if (lower.includes("risk") || lower.includes("weather") || lower.includes("delay") || lower.includes("risk")) {
        category = "Risk Management"
        icon = AlertCircle
        color = "text-red-500"
      } else if (lower.includes("route") || lower.includes("distance") || lower.includes("path") || lower.includes("routing")) {
        category = "Route Planning"
        icon = MapPin
        color = "text-blue-500"
      } else if (lower.includes("demand") || lower.includes("forecast") || lower.includes("volume") || lower.includes("orders")) {
        category = "Demand Analysis"
        icon = TrendingUp
        color = "text-purple-500"
      } else if (lower.includes("vendor") || lower.includes("supplier") || lower.includes("carrier")) {
        category = "Vendor Selection"
        icon = CheckCircle2
        color = "text-orange-500"
      }

      return { text: sentence, category, icon, color }
    })
  }

  const recommendations = parseRecommendations(reasoning)

  const getConfidenceBadge = (level: string) => {
    const lower = (level || "").toLowerCase()
    if (lower.includes("high")) {
      return <Badge className="bg-green-500 text-white">High Confidence</Badge>
    } else if (lower.includes("medium")) {
      return <Badge className="bg-yellow-500 text-white">Medium Confidence</Badge>
    } else {
      return <Badge className="bg-orange-500 text-white">Low Confidence</Badge>
    }
  }

  return (
    <Card className="p-8 border-2">
      {/* Header */}
      <div className="flex items-center justify-between mb-6 pb-6 border-b">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center">
            <Brain className="w-7 h-7 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold">Strategic Recommendations</h2>
            <p className="text-sm text-muted-foreground">AI-powered insights from multi-agent analysis</p>
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          {getConfidenceBadge(confidence.level)}
          <span className="text-2xl font-bold text-primary">{confidence.score}</span>
        </div>
      </div>

      {/* Recommendations Grid */}
      {recommendations.length > 0 ? (
        <div className="space-y-4 mb-6">
          {recommendations.map((rec, index) => {
            const Icon = rec.icon
            return (
              <div
                key={index}
                className="group p-4 rounded-lg border-2 border-border hover:border-primary/50 hover:bg-accent/5 transition-all"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${rec.color.replace('text-', 'from-')}/10 ${rec.color.replace('text-', 'to-')}/20 flex items-center justify-center`}>
                      <Icon className={`w-5 h-5 ${rec.color}`} />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <Badge variant="outline" className="text-xs">
                        {rec.category}
                      </Badge>
                    </div>
                    <p className="text-sm text-foreground leading-relaxed">{cleanMarkdown(rec.text)}</p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="p-8 text-center text-muted-foreground">
          <p>No recommendations could be parsed. View full analysis below.</p>
        </div>
      )}

      {/* Cleaned and Structured AI Analysis */}
      <div className="pt-6 border-t">
        <h3 className="text-sm font-semibold mb-3 text-muted-foreground uppercase tracking-wide">
          Complete AI Analysis
        </h3>
        <div className="p-4 bg-muted/30 rounded-lg border">
          <div className="text-sm text-foreground leading-relaxed max-h-64 overflow-y-auto space-y-2">
            {reasoning
              ?.split("\n")
              .filter(line => line.trim())
              .map((line, index) => {
                const cleanLine = cleanMarkdown(line)
                const isHeader = /^[A-Z0-9\s\-\u2014]+$/.test(cleanLine) && cleanLine.length > 4
                return isHeader ? (
                  <h4 key={index} className="text-primary font-semibold mt-3 mb-1">
                    {cleanLine}
                  </h4>
                ) : (
                  <p key={index} className="text-foreground">{cleanLine}</p>
                )
              }) || <p className="text-muted-foreground">No detailed analysis available.</p>}
          </div>
        </div>
      </div>

      {/* Footer Stats */}
      <div className="flex items-center justify-between mt-6 pt-6 border-t text-sm text-muted-foreground">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-green-500" />
          <span>Analysis complete</span>
        </div>
        {executionTime && (
          <span>Processing time: {executionTime.toFixed(2)}s</span>
        )}
      </div>
    </Card>
  )
}
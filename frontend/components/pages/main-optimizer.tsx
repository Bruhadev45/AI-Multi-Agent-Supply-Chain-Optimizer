"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Loader2, Play, CheckCircle, Clock, TrendingUp, MapPin, DollarSign, AlertTriangle, Brain } from "lucide-react"
import { AnalysisResponse, Scenario, City } from "@/lib/api-client"
import { ProgressiveAgents } from "./progressive-agents"
import { StrategicRecommendations } from "./strategic-recommendations"
import { AIChatbot } from "@/components/chat/ai-chatbot"
import { ExportButton } from "@/components/ui/export-button"

interface MainOptimizerProps {
  scenarios: Scenario[]
  cities: City[]
  onRunAnalysis: (origin: string, destination: string, scenario: string) => Promise<void>
  loading: boolean
  analysisData: AnalysisResponse | null
}

export function MainOptimizer({ scenarios, cities, onRunAnalysis, loading, analysisData }: MainOptimizerProps) {
  const [origin, setOrigin] = useState("")
  const [destination, setDestination] = useState("")
  const [selectedScenario, setSelectedScenario] = useState("")
  const [showResults, setShowResults] = useState(false)
  const [agentProgress, setAgentProgress] = useState<any[]>([])
  const [showFinalResults, setShowFinalResults] = useState(false)

  useEffect(() => {
    if (scenarios.length > 0 && !selectedScenario) {
      setSelectedScenario(scenarios[0].name)
    }
  }, [scenarios, selectedScenario])

  // Simulate progressive agent execution
  useEffect(() => {
    if (loading) {
      setShowFinalResults(false)
      const agents = [
        { id: "demand", name: "Demand Forecast Agent", icon: TrendingUp, status: "running" as const },
        { id: "route", name: "Route Optimizer Agent", icon: MapPin, status: "pending" as const },
        { id: "cost", name: "Cost Analyzer Agent", icon: DollarSign, status: "pending" as const },
        { id: "risk", name: "Risk Monitor Agent", icon: AlertTriangle, status: "pending" as const },
        { id: "coordinator", name: "Strategic Coordinator", icon: Brain, status: "pending" as const },
      ]
      setAgentProgress(agents)
    }
  }, [loading])

  useEffect(() => {
    if (analysisData && !loading) {
      // Progressively show agent completions
      let currentStep = 0
      const agents = [
        {
          id: "demand",
          name: "Demand Forecast Agent",
          icon: TrendingUp,
          output: {
            forecast: analysisData.forecast,
            original: analysisData.forecast_original,
            scenario: analysisData.scenario_applied,
          },
        },
        {
          id: "route",
          name: "Route Optimizer Agent",
          icon: MapPin,
          output: {
            distance: `${analysisData.route_info.distance_km.toFixed(0)} km`,
            duration: analysisData.route_info.duration,
            path: analysisData.route_info.path.join(" → "),
          },
        },
        {
          id: "cost",
          name: "Cost Analyzer Agent",
          icon: DollarSign,
          output: {
            best_vendor: analysisData.best_vendor,
            best_price: `₹${(analysisData.best_price / 1000).toFixed(1)}K`,
            savings: `₹${((analysisData.original_price - analysisData.best_price) / 1000).toFixed(1)}K`,
          },
        },
        {
          id: "risk",
          name: "Risk Monitor Agent",
          icon: AlertTriangle,
          output: {
            risk_level: analysisData.risk.risk_level,
            condition: analysisData.risk.condition,
            temperature: `${analysisData.risk.temp}°C`,
          },
        },
        {
          id: "coordinator",
          name: "Strategic Coordinator",
          icon: Brain,
          output: {
            confidence: analysisData.recommendations_confidence.score,
            level: analysisData.recommendations_confidence.level,
          },
        },
      ]

      const updateAgent = (index: number) => {
        if (index < agents.length) {
          setAgentProgress((prev) =>
            prev.map((agent, i) => {
              if (i === index) {
                return { ...agents[index], status: "completed" as const, duration: Math.random() * 2 + 1 }
              } else if (i === index + 1) {
                return { ...prev[i], status: "running" as const }
              }
              return agent
            })
          )

          setTimeout(() => updateAgent(index + 1), 800)
        } else {
          setTimeout(() => {
            setShowFinalResults(true)
            setShowResults(true)
          }, 500)
        }
      }

      updateAgent(0)
    }
  }, [analysisData, loading])

  const handleRunOptimization = async () => {
    if (!origin || !destination) {
      alert("Please select both origin and destination cities")
      return
    }
    if (origin === destination) {
      alert("Origin and destination cannot be the same")
      return
    }
    setShowResults(false)
    await onRunAnalysis(origin, destination, selectedScenario)
  }

  const isFormValid = origin && destination && origin !== destination && selectedScenario

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2 pb-4">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
          AI Supply Chain Optimizer
        </h1>
        <p className="text-muted-foreground text-lg">
          Multi-Agent System for Intelligent Logistics Optimization
        </p>
      </div>

      {/* Configuration Panel */}
      <Card className="p-8 bg-gradient-to-br from-card to-card/50 border-2">
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
              <MapPin className="w-6 h-6 text-primary" />
              Route Configuration
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Origin */}
              <div>
                <label className="block text-sm font-medium mb-2 text-foreground">
                  Origin City <span className="text-red-500">*</span>
                </label>
                <select
                  value={origin}
                  onChange={(e) => setOrigin(e.target.value)}
                  disabled={loading}
                  className="w-full px-4 py-3 rounded-lg border-2 border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all disabled:opacity-50"
                >
                  <option value="">Select origin city</option>
                  {cities.map((city) => (
                    <option key={city.name} value={city.name}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Destination */}
              <div>
                <label className="block text-sm font-medium mb-2 text-foreground">
                  Destination City <span className="text-red-500">*</span>
                </label>
                <select
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  disabled={loading}
                  className="w-full px-4 py-3 rounded-lg border-2 border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all disabled:opacity-50"
                >
                  <option value="">Select destination city</option>
                  {cities.map((city) => (
                    <option key={city.name} value={city.name}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Scenario Selection */}
          <div>
            <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-primary" />
              Operational Scenario
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {scenarios.map((scenario) => (
                <button
                  key={scenario.id}
                  onClick={() => setSelectedScenario(scenario.name)}
                  disabled={loading}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    selectedScenario === scenario.name
                      ? "border-primary bg-primary/10 shadow-lg scale-105"
                      : "border-border hover:border-primary/50 hover:shadow"
                  } disabled:opacity-50`}
                >
                  <div className="font-semibold text-foreground mb-1">{scenario.name}</div>
                  <div className="text-xs text-muted-foreground space-y-1">
                    <div>Demand: {(scenario.config.demand_multiplier * 100).toFixed(0)}%</div>
                    <div>Cost: {(scenario.config.cost_multiplier * 100).toFixed(0)}%</div>
                    <div>
                      Risk: <Badge variant={scenario.config.risk_level === "High" ? "destructive" : scenario.config.risk_level === "Medium" ? "secondary" : "default"} className="text-xs">
                        {scenario.config.risk_level}
                      </Badge>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Run Button */}
          <div className="flex justify-center pt-4">
            <Button
              onClick={handleRunOptimization}
              disabled={!isFormValid || loading}
              size="lg"
              className="px-12 py-6 text-lg bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 disabled:opacity-50 shadow-lg hover:shadow-xl transition-all"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-3 h-6 w-6 animate-spin" />
                  Running AI Agents...
                </>
              ) : (
                <>
                  <Play className="mr-3 h-6 w-6" />
                  Run Optimization
                </>
              )}
            </Button>
          </div>
        </div>
      </Card>

      {/* Progressive Agent Execution */}
      {(loading || (agentProgress.length > 0 && !showFinalResults)) && (
        <ProgressiveAgents agents={agentProgress} />
      )}

      {/* Final Results Display */}
      {showFinalResults && analysisData && !loading && (
        <div className="space-y-6 animate-fade-in">
          {/* Success Message */}
          <Card className="p-6 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border-2 border-green-500/30 animate-scale-in">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <CheckCircle className="w-12 h-12 text-green-500 animate-bounce" />
                <div>
                  <h3 className="text-xl font-semibold text-green-700 dark:text-green-400">
                    ✨ All Agents Completed Successfully!
                  </h3>
                  <p className="text-muted-foreground">
                    5 AI agents have analyzed your supply chain and generated strategic insights
                  </p>
                </div>
              </div>
              <ExportButton data={analysisData} filename="supply-chain-analysis" />
            </div>
          </Card>

          {/* Strategic Recommendations - Enhanced */}
          <StrategicRecommendations
            reasoning={analysisData.crew_reasoning}
            confidence={analysisData.recommendations_confidence}
            executionTime={analysisData.execution_metadata.total_time_seconds}
          />

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="p-6 bg-gradient-to-br from-blue-500/10 to-blue-600/10 border-2 border-blue-500/30">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <MapPin className="w-8 h-8 text-blue-500" />
                  <Badge variant="secondary">Route</Badge>
                </div>
                <div className="text-2xl font-bold">{analysisData.route_info.distance_km.toFixed(0)} km</div>
                <div className="text-sm text-muted-foreground">
                  {analysisData.route_info.path[0]} → {analysisData.route_info.path[analysisData.route_info.path.length - 1]}
                </div>
                <div className="text-xs text-muted-foreground">Duration: {analysisData.route_info.duration}</div>
              </div>
            </Card>

            <Card className="p-6 bg-gradient-to-br from-green-500/10 to-green-600/10 border-2 border-green-500/30">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <DollarSign className="w-8 h-8 text-green-500" />
                  <Badge variant="secondary">Cost</Badge>
                </div>
                <div className="text-2xl font-bold">₹{(analysisData.best_price / 1000).toFixed(1)}K</div>
                <div className="text-sm text-muted-foreground">{analysisData.best_vendor}</div>
                {analysisData.best_price !== analysisData.original_price && (
                  <div className="text-xs text-green-600 dark:text-green-400">
                    Saved ₹{((analysisData.original_price - analysisData.best_price) / 1000).toFixed(1)}K
                  </div>
                )}
              </div>
            </Card>

            <Card className="p-6 bg-gradient-to-br from-purple-500/10 to-purple-600/10 border-2 border-purple-500/30">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <TrendingUp className="w-8 h-8 text-purple-500" />
                  <Badge variant="secondary">Demand</Badge>
                </div>
                <div className="text-2xl font-bold">{analysisData.forecast.toFixed(0)}</div>
                <div className="text-sm text-muted-foreground">Units forecasted</div>
                {analysisData.forecast !== analysisData.forecast_original && (
                  <div className="text-xs text-purple-600 dark:text-purple-400">
                    {((analysisData.forecast / analysisData.forecast_original - 1) * 100).toFixed(0)}% scenario impact
                  </div>
                )}
              </div>
            </Card>

            <Card className="p-6 bg-gradient-to-br from-orange-500/10 to-orange-600/10 border-2 border-orange-500/30">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <AlertTriangle className="w-8 h-8 text-orange-500" />
                  <Badge variant={analysisData.risk.risk_level.includes("High") ? "destructive" : "secondary"}>
                    Risk
                  </Badge>
                </div>
                <div className="text-2xl font-bold">{analysisData.risk.risk_level}</div>
                <div className="text-sm text-muted-foreground">{analysisData.risk.condition}</div>
                <div className="text-xs text-muted-foreground">
                  Confidence: {analysisData.recommendations_confidence.score}
                </div>
              </div>
            </Card>
          </div>


          {/* Agent Performance */}
          <Card className="p-6 border-2">
            <h3 className="text-xl font-semibold mb-4">Agent Performance</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(analysisData.execution_metadata.success_rates).map(([agent, success]) => (
                <div key={agent} className="flex items-center gap-2">
                  {success ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : (
                    <AlertTriangle className="w-5 h-5 text-orange-500" />
                  )}
                  <span className="text-sm capitalize">{agent.replace("_", " ")}</span>
                </div>
              ))}
            </div>
            <div className="mt-4 text-sm text-muted-foreground">
              Total execution time: {analysisData.execution_metadata.total_time_seconds.toFixed(2)}s
            </div>
          </Card>
        </div>
      )}

      {/* Initial State */}
      {!showResults && !loading && (
        <Card className="p-12 text-center border-2 border-dashed">
          <div className="max-w-md mx-auto space-y-4">
            <Play className="w-16 h-16 mx-auto text-muted-foreground" />
            <h3 className="text-xl font-semibold">Ready to Optimize</h3>
            <p className="text-muted-foreground">
              Select your route and scenario above, then click "Run Optimization" to start the AI agents
            </p>
          </div>
        </Card>
      )}

      {/* AI Chatbot */}
      <AIChatbot />
    </div>
  )
}

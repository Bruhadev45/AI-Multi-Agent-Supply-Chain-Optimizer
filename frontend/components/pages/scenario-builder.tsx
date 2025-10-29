"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ChevronRight, ChevronLeft, Loader2 } from "lucide-react"
import { Scenario, City } from "@/lib/api-client"

type Step = 1 | 2 | 3 | 4

interface ScenarioBuilderProps {
  scenarios: Scenario[]
  cities: City[]
  onRunAnalysis: (origin: string, destination: string, scenario: string) => Promise<void>
  loading: boolean
}

export function ScenarioBuilder({ scenarios, cities, onRunAnalysis, loading }: ScenarioBuilderProps) {
  const [step, setStep] = useState<Step>(1)
  const [formData, setFormData] = useState({
    scenarioType: scenarios[0]?.name || "🟢 Normal Operations",
    origin: "",
    destination: "",
    date: "",
    vendorConstraints: "",
    riskThreshold: 5,
  })

  const handleNext = () => {
    if (step < 4) setStep((step + 1) as Step)
  }

  const handlePrev = () => {
    if (step > 1) setStep((step - 1) as Step)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleRunAnalysis = async () => {
    if (!formData.origin || !formData.destination) {
      alert("Please select both origin and destination cities")
      return
    }
    await onRunAnalysis(formData.origin, formData.destination, formData.scenarioType)
  }

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Choose Scenario Type</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {scenarios.length > 0 ? (
                scenarios.map((scenario) => (
                  <button
                    key={scenario.id}
                    onClick={() => setFormData((prev) => ({ ...prev, scenarioType: scenario.name }))}
                    className={`p-4 rounded-lg border-2 transition-all text-left ${
                      formData.scenarioType === scenario.name
                        ? "border-primary bg-primary/10"
                        : "border-border hover:border-primary/50"
                    }`}
                  >
                    <p className="font-semibold text-foreground">{scenario.name}</p>
                    <p className="text-sm text-muted-foreground">
                      Demand: {(scenario.config.demand_multiplier * 100).toFixed(0)}% |
                      Cost: {(scenario.config.cost_multiplier * 100).toFixed(0)}% |
                      Risk: {scenario.config.risk_level}
                    </p>
                  </button>
                ))
              ) : (
                <p className="text-muted-foreground col-span-2">Loading scenarios...</p>
              )}
            </div>
          </div>
        )
      case 2:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Set Origin & Destination</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Origin City</label>
                <select
                  name="origin"
                  value={formData.origin}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">Select origin city</option>
                  {cities.map((city) => (
                    <option key={city.name} value={city.name}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Destination City</label>
                <select
                  name="destination"
                  value={formData.destination}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">Select destination city</option>
                  {cities.map((city) => (
                    <option key={city.name} value={city.name}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Date</label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            </div>
          </div>
        )
      case 3:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Vendor & Budget Constraints</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Vendor Constraints</label>
                <textarea
                  name="vendorConstraints"
                  value={formData.vendorConstraints}
                  onChange={handleInputChange}
                  placeholder="e.g., Exclude vendor X, prefer vendor Y"
                  rows={4}
                  className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Risk Threshold: {formData.riskThreshold}/10
                </label>
                <input
                  type="range"
                  name="riskThreshold"
                  min="1"
                  max="10"
                  value={formData.riskThreshold}
                  onChange={handleInputChange}
                  className="w-full"
                />
              </div>
            </div>
          </div>
        )
      case 4:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Review & Run</h3>
            <Card className="p-4 bg-muted/50 border border-border">
              <div className="space-y-2 text-sm">
                <p>
                  <span className="font-semibold text-foreground">Scenario:</span>{" "}
                  <span className="text-muted-foreground">{formData.scenarioType}</span>
                </p>
                <p>
                  <span className="font-semibold text-foreground">Route:</span>{" "}
                  <span className="text-muted-foreground">
                    {formData.origin} → {formData.destination}
                  </span>
                </p>
                <p>
                  <span className="font-semibold text-foreground">Date:</span>{" "}
                  <span className="text-muted-foreground">{formData.date}</span>
                </p>
                <p>
                  <span className="font-semibold text-foreground">Risk Threshold:</span>{" "}
                  <span className="text-muted-foreground">{formData.riskThreshold}/10</span>
                </p>
              </div>
            </Card>
            <Button
              onClick={handleRunAnalysis}
              disabled={loading || !formData.origin || !formData.destination}
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Running Analysis...
                </>
              ) : (
                "Run Optimization"
              )}
            </Button>
          </div>
        )
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Scenario Builder</h1>
        <p className="text-muted-foreground mt-1">Create and run supply chain optimization scenarios</p>
      </div>

      {/* Progress Indicator */}
      <div className="flex items-center justify-between">
        {[1, 2, 3, 4].map((s) => (
          <div key={s} className="flex items-center flex-1">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                s <= step ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
              }`}
            >
              {s}
            </div>
            {s < 4 && <div className={`flex-1 h-1 mx-2 ${s < step ? "bg-primary" : "bg-muted"}`} />}
          </div>
        ))}
      </div>

      {/* Form Card */}
      <Card className="p-8 bg-card border border-border">{renderStep()}</Card>

      {/* Navigation Buttons */}
      <div className="flex gap-4 justify-between">
        <Button
          onClick={handlePrev}
          disabled={step === 1}
          variant="outline"
          className="flex items-center gap-2 bg-transparent"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </Button>
        <Button
          onClick={handleNext}
          disabled={step === 4}
          className="flex items-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Next
          <ChevronRight className="w-4 h-4" />
        </Button>
      </div>
    </div>
  )
}

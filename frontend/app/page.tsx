"use client"

import { useState, useEffect, useCallback } from "react"
import { MainLayout } from "@/components/layout/main-layout"
import { MainOptimizer } from "@/components/pages/main-optimizer"
import { EnhancedAgentDetails } from "@/components/pages/enhanced-agent-details"
import { VendorRoutes } from "@/components/pages/vendor-routes"
import { ShipmentTracking } from "@/components/pages/shipment-tracking"
import apiClient, { AnalysisResponse, Scenario, City, formatAPIError } from "@/lib/api-client"
import { toast } from "@/hooks/use-toast"

type Page = "dashboard" | "agents" | "vendors" | "shipments"

export default function Home() {
  const [currentPage, setCurrentPage] = useState<Page>("dashboard")
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null)
  const [scenarios, setScenarios] = useState<Scenario[]>([])
  const [cities, setCities] = useState<City[]>([])
  const [loading, setLoading] = useState(false)
  const [apiConnected, setApiConnected] = useState<boolean | null>(null)

  // Check API connection on mount with retries for cold-start scenarios
  useEffect(() => {
    let cancelled = false
    const checkAPI = async () => {
      const maxRetries = 5
      const retryDelayMs = 3000
      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        if (cancelled) return
        try {
          await apiClient.healthCheck()
          if (!cancelled) setApiConnected(true)
          return
        } catch (error) {
          console.warn(`API health check attempt ${attempt}/${maxRetries} failed:`, error)
          if (attempt < maxRetries) {
            await new Promise(r => setTimeout(r, retryDelayMs))
          }
        }
      }
      if (!cancelled) {
        setApiConnected(false)
        toast({
          title: "API Connection Failed",
          description: "Make sure the backend server is running on port 8000",
          variant: "destructive",
        })
      }
    }
    checkAPI()
    return () => { cancelled = true }
  }, [])

  // Load scenarios and cities
  useEffect(() => {
    const loadConfig = async () => {
      try {
        const [scenariosData, citiesData] = await Promise.all([
          apiClient.getScenarios(),
          apiClient.getCities()
        ])
        setScenarios(scenariosData.scenarios)
        setCities(citiesData.cities)
      } catch (error) {
        console.error('Failed to load configuration:', error)
      }
    }

    if (apiConnected) {
      loadConfig()
    }
  }, [apiConnected])

  // Run analysis function
  const runAnalysis = useCallback(async (origin: string, destination: string, scenario: string) => {
    setLoading(true)
    try {
      const result = await apiClient.runAnalysis({
        origin,
        destination,
        scenario,
      })
      setAnalysisData(result)
      setCurrentPage("dashboard") // Switch to dashboard to show results
      toast({
        title: "Analysis Complete",
        description: `Successfully analyzed route from ${origin} to ${destination}`,
      })
    } catch (error) {
      console.error('Analysis failed:', error)
      toast({
        title: "Analysis Failed",
        description: formatAPIError(error),
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }, [])

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return (
          <MainOptimizer
            scenarios={scenarios}
            cities={cities}
            onRunAnalysis={runAnalysis}
            loading={loading}
            analysisData={analysisData}
          />
        )
      case "shipments":
        return <ShipmentTracking />
      case "agents":
        return <EnhancedAgentDetails analysisData={analysisData} />
      case "vendors":
        return <VendorRoutes analysisData={analysisData} />
      default:
        return (
          <MainOptimizer
            scenarios={scenarios}
            cities={cities}
            onRunAnalysis={runAnalysis}
            loading={loading}
            analysisData={analysisData}
          />
        )
    }
  }

  return (
    <MainLayout currentPage={currentPage} onPageChange={setCurrentPage}>
      {renderPage()}
    </MainLayout>
  )
}

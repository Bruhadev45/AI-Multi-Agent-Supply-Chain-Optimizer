"use client"

import { useState, useEffect, useCallback } from "react"
import { MainLayout } from "@/components/layout/main-layout"
import { MainOptimizer } from "@/components/pages/main-optimizer"
import { EnhancedAgentDetails } from "@/components/pages/enhanced-agent-details"
import { VendorRoutes } from "@/components/pages/vendor-routes"
import { ShipmentTracking } from "@/components/pages/shipment-tracking"
import { Dashboard } from "@/components/pages/dashboard"
import { Reports } from "@/components/pages/reports"
import { Settings } from "@/components/pages/settings"
import apiClient, { AnalysisResponse, Scenario, City, formatAPIError } from "@/lib/api-client"
import { toast } from "@/hooks/use-toast"

export type Page = "optimizer" | "analytics" | "agents" | "vendors" | "shipments" | "reports" | "settings"

export default function Home() {
  const [currentPage, setCurrentPage] = useState<Page>("optimizer")
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null)
  const [analysisHistory, setAnalysisHistory] = useState<Array<{ data: AnalysisResponse; timestamp: string }>>([])
  const [scenarios, setScenarios] = useState<Scenario[]>([])
  const [cities, setCities] = useState<City[]>([])
  const [loading, setLoading] = useState(false)
  const [apiConnected, setApiConnected] = useState<boolean | null>(null)

  useEffect(() => {
    const checkAPI = async () => {
      try {
        await apiClient.healthCheck()
        setApiConnected(true)
      } catch (error) {
        console.error('API connection failed:', error)
        setApiConnected(false)
        toast({
          title: "API Connection Failed",
          description: "Make sure the backend server is running on port 8000",
          variant: "destructive",
        })
      }
    }
    checkAPI()
  }, [])

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

  const runAnalysis = useCallback(async (origin: string, destination: string, scenario: string) => {
    setLoading(true)
    try {
      const result = await apiClient.runAnalysis({
        origin,
        destination,
        scenario,
      })
      setAnalysisData(result)
      setAnalysisHistory(prev => [
        { data: result, timestamp: new Date().toISOString() },
        ...prev.slice(0, 19)
      ])
      setCurrentPage("optimizer")
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
      case "optimizer":
        return (
          <MainOptimizer
            scenarios={scenarios}
            cities={cities}
            onRunAnalysis={runAnalysis}
            loading={loading}
            analysisData={analysisData}
          />
        )
      case "analytics":
        return <Dashboard analysisData={analysisData} loading={loading} />
      case "shipments":
        return <ShipmentTracking />
      case "agents":
        return <EnhancedAgentDetails analysisData={analysisData} />
      case "vendors":
        return <VendorRoutes analysisData={analysisData} />
      case "reports":
        return <Reports analysisData={analysisData} analysisHistory={analysisHistory} />
      case "settings":
        return <Settings apiConnected={apiConnected} />
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
    <MainLayout
      currentPage={currentPage}
      onPageChange={setCurrentPage}
      apiConnected={apiConnected}
      analysisData={analysisData}
    >
      {renderPage()}
    </MainLayout>
  )
}

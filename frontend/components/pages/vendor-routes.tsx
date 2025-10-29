"use client"

import { useState } from "react"
import dynamic from "next/dynamic"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { MapPin, Star } from "lucide-react"
import { AnalysisResponse } from "@/lib/api-client"

// Dynamically import RouteMap to avoid SSR issues
const RouteMap = dynamic(() => import("@/components/map/route-map").then((mod) => mod.RouteMap), {
  ssr: false,
  loading: () => (
    <div className="w-full h-96 bg-muted rounded-lg flex items-center justify-center">
      <p className="text-muted-foreground">Loading map...</p>
    </div>
  ),
})

interface VendorRoutesProps {
  analysisData: AnalysisResponse | null
}

// City coordinates mapping
const cityCoordinates: Record<string, [number, number]> = {
  Mumbai: [19.076, 72.8777],
  Delhi: [28.7041, 77.1025],
  Bangalore: [12.9716, 77.5946],
  Chennai: [13.0827, 80.2707],
  Kolkata: [22.5726, 88.3639],
  Hyderabad: [17.385, 78.4867],
  Pune: [18.5204, 73.8567],
  Ahmedabad: [23.0225, 72.5714],
  Jaipur: [26.9124, 75.7873],
  Lucknow: [26.8467, 80.9462],
  Kanpur: [26.4499, 80.3319],
  Nagpur: [21.1458, 79.0882],
  Indore: [22.7196, 75.8577],
  Bhopal: [23.2599, 77.4126],
}

const vendors = [
  { id: 1, name: "FastLogistics Inc", cost: "₹45,000", reliability: 98, sustainability: 85, rating: 4.8 },
  { id: 2, name: "EcoShip Solutions", cost: "₹42,000", reliability: 95, sustainability: 92, rating: 4.6 },
  { id: 3, name: "SpeedRoute Express", cost: "₹48,000", reliability: 99, sustainability: 78, rating: 4.9 },
  { id: 4, name: "GreenLogistics", cost: "₹44,000", reliability: 92, sustainability: 95, rating: 4.5 },
]

export function VendorRoutes({ analysisData }: VendorRoutesProps) {
  const [viewMode, setViewMode] = useState<"table" | "map">("table")
  const [mapKey, setMapKey] = useState(0)
  const [isMapLoading, setIsMapLoading] = useState(false)

  // Force map remount when switching to map view
  const handleViewChange = (mode: "table" | "map") => {
    if (mode === "map") {
      // Show loading state first
      setIsMapLoading(true)
      setViewMode(mode)
      // Delay map render to ensure clean state
      setTimeout(() => {
        setMapKey(Date.now())
        setIsMapLoading(false)
      }, 300)
    } else {
      setViewMode(mode)
      setIsMapLoading(false)
    }
  }

  // Extract route information from analysisData
  const getRouteInfo = () => {
    if (!analysisData || !analysisData.route_info) {
      return { origin: null, destination: null, distance: null, duration: null }
    }

    const path = analysisData.route_info.path || []
    const originName = path[0] || "Unknown"
    const destName = path[path.length - 1] || "Unknown"

    // Check if coordinates exist for the cities
    const originCoords = cityCoordinates[originName]
    const destCoords = cityCoordinates[destName]

    if (!originCoords || !destCoords) {
      console.warn(`Missing coordinates for ${originName} or ${destName}`)
      return { origin: null, destination: null, distance: null, duration: null }
    }

    return {
      origin: {
        name: originName,
        coordinates: originCoords as [number, number],
      },
      destination: {
        name: destName,
        coordinates: destCoords as [number, number],
      },
      distance: analysisData.route_info.distance_km,
      duration: analysisData.route_info.duration,
    }
  }

  const routeInfo = getRouteInfo()

  // Use real vendor data from API if available, fallback to mock data
  const displayVendors = (analysisData?.all_vendors && analysisData.all_vendors.length > 0)
    ? analysisData.all_vendors
    : vendors

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Vendors & Routes</h1>
          <p className="text-muted-foreground mt-1">Manage vendors and optimize routes</p>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={() => handleViewChange("table")}
            variant={viewMode === "table" ? "default" : "outline"}
            className={viewMode === "table" ? "bg-primary text-primary-foreground" : ""}
          >
            Table View
          </Button>
          <Button
            onClick={() => handleViewChange("map")}
            variant={viewMode === "map" ? "default" : "outline"}
            className={viewMode === "map" ? "bg-primary text-primary-foreground" : ""}
          >
            Map View
          </Button>
        </div>
      </div>

      {viewMode === "table" ? (
        <Card className="p-6 bg-card border border-border overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 font-semibold text-foreground">Vendor Name</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Cost</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Reliability</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Sustainability</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Rating</th>
                <th className="text-left py-3 px-4 font-semibold text-foreground">Action</th>
              </tr>
            </thead>
            <tbody>
              {displayVendors.map((vendor, index) => (
                <tr key={vendor.id || index} className="border-b border-border hover:bg-muted/50 transition-colors">
                  <td className="py-4 px-4 text-foreground font-medium">{vendor.name || vendor.vendor}</td>
                  <td className="py-4 px-4 text-foreground">
                    {typeof vendor.cost === "string"
                      ? vendor.cost
                      : vendor.total_cost
                      ? `₹${vendor.total_cost.toLocaleString()}`
                      : "N/A"}
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-muted rounded-full h-2 max-w-xs">
                        <div className="bg-success h-2 rounded-full" style={{ width: `${vendor.reliability}%` }} />
                      </div>
                      <span className="text-sm text-foreground">{vendor.reliability}%</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-muted rounded-full h-2 max-w-xs">
                        <div className="bg-accent h-2 rounded-full" style={{ width: `${vendor.sustainability}%` }} />
                      </div>
                      <span className="text-sm text-foreground">{vendor.sustainability}%</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-accent text-accent" />
                      <span className="text-foreground font-medium">{vendor.rating}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" className="text-xs">
                        View Details
                      </Button>
                      <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90 text-xs">
                        Select Vendor
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      ) : (
        <Card className="p-6 bg-card border border-border">
          <div className="w-full h-[600px]">
            {isMapLoading ? (
              <div className="w-full h-full flex items-center justify-center bg-muted rounded-lg">
                <div className="text-center">
                  <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-2"></div>
                  <p className="text-muted-foreground text-sm">Preparing map...</p>
                </div>
              </div>
            ) : routeInfo.origin && routeInfo.destination ? (
              <RouteMap
                key={`route-map-${mapKey}`}
                forceKey={mapKey}
                origin={routeInfo.origin}
                destination={routeInfo.destination}
                distance={routeInfo.distance || undefined}
                duration={routeInfo.duration || undefined}
              />
            ) : (
              <div className="w-full h-full bg-muted rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <MapPin className="w-12 h-12 text-muted-foreground mx-auto mb-2" />
                  <p className="text-muted-foreground">No route data available</p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Run an analysis from the Optimizer page to see route visualization
                  </p>
                </div>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Route Alternatives */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[
          { name: "Route A (Recommended)", distance: "1,240 km", time: "18h 30m", cost: "₹42,000", risk: "Low" },
          { name: "Route B (Fastest)", distance: "1,180 km", time: "16h 45m", cost: "₹48,500", risk: "Medium" },
        ].map((route, i) => (
          <Card key={i} className="p-6 bg-card border border-border">
            <h3 className="font-semibold text-foreground mb-4">{route.name}</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Distance</span>
                <span className="text-foreground font-medium">{route.distance}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Estimated Time</span>
                <span className="text-foreground font-medium">{route.time}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Cost</span>
                <span className="text-foreground font-medium">{route.cost}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Risk Level</span>
                <span className={`font-medium ${route.risk === "Low" ? "text-success" : "text-warning"}`}>
                  {route.risk}
                </span>
              </div>
            </div>
            <Button className="w-full mt-4 bg-primary text-primary-foreground hover:bg-primary/90">
              Use This Route
            </Button>
          </Card>
        ))}
      </div>
    </div>
  )
}

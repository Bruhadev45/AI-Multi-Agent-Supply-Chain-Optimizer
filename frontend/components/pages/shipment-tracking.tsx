"use client"

import { useState, useMemo } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Package, MapPin, Clock, CheckCircle, AlertTriangle, Truck, Info, Search, Filter } from "lucide-react"

// Sample shipments data
const shipmentsData = [
  {
    id: "SH001",
    order: "ORD-2024-001",
    origin: "Mumbai Warehouse",
    destination: "Delhi Hub",
    status: "in_transit",
    progress: 65,
    eta: "2 hours",
    carrier: "FastTrack Logistics",
    items: 45,
    weight: "1250 kg",
    lastUpdate: "10 mins ago",
    currentLocation: "Ahmedabad Checkpoint"
  },
  {
    id: "SH002",
    order: "ORD-2024-002",
    origin: "Bangalore DC",
    destination: "Chennai",
    status: "delivered",
    progress: 100,
    eta: "Delivered",
    carrier: "EcoFreight Solutions",
    items: 32,
    weight: "890 kg",
    lastUpdate: "1 hour ago",
    currentLocation: "Chennai - Delivered"
  },
  {
    id: "SH003",
    order: "ORD-2024-003",
    origin: "Delhi Hub",
    destination: "Jaipur",
    status: "pending",
    progress: 0,
    eta: "6 hours",
    carrier: "SpeedRoute Express",
    items: 28,
    weight: "670 kg",
    lastUpdate: "30 mins ago",
    currentLocation: "Delhi Hub - Awaiting Dispatch"
  },
  {
    id: "SH004",
    order: "ORD-2024-004",
    origin: "Kolkata Port",
    destination: "Bhubaneswar",
    status: "delayed",
    progress: 45,
    eta: "8 hours (Delayed 2hrs)",
    carrier: "CargoMaster",
    items: 67,
    weight: "2100 kg",
    lastUpdate: "5 mins ago",
    currentLocation: "Cuttack - Traffic Delay"
  },
  {
    id: "SH005",
    order: "ORD-2024-005",
    origin: "Pune Factory",
    destination: "Mumbai Port",
    status: "in_transit",
    progress: 80,
    eta: "45 mins",
    carrier: "GreenShip Co",
    items: 120,
    weight: "3400 kg",
    lastUpdate: "2 mins ago",
    currentLocation: "Approaching Mumbai Port"
  },
]

export function ShipmentTracking() {
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<string>("all")

  const getStatusColor = (status: string) => {
    switch (status) {
      case "delivered":
        return "bg-green-500/10 text-green-700 dark:text-green-400 border-green-500/20"
      case "in_transit":
        return "bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-500/20"
      case "delayed":
        return "bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20"
      case "pending":
        return "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 border-yellow-500/20"
      default:
        return "bg-gray-500/10 text-gray-700 dark:text-gray-400 border-gray-500/20"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "delivered":
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case "in_transit":
        return <Truck className="w-5 h-5 text-blue-500" />
      case "delayed":
        return <AlertTriangle className="w-5 h-5 text-red-500" />
      case "pending":
        return <Clock className="w-5 h-5 text-yellow-500" />
      default:
        return <Info className="w-5 h-5 text-gray-500" />
    }
  }

  // Filter shipments based on search query and status filter
  const filteredShipments = useMemo(() => {
    return shipmentsData.filter((shipment) => {
      const matchesSearch =
        searchQuery === "" ||
        shipment.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        shipment.order.toLowerCase().includes(searchQuery.toLowerCase()) ||
        shipment.origin.toLowerCase().includes(searchQuery.toLowerCase()) ||
        shipment.destination.toLowerCase().includes(searchQuery.toLowerCase()) ||
        shipment.carrier.toLowerCase().includes(searchQuery.toLowerCase())

      const matchesStatus =
        statusFilter === "all" || shipment.status === statusFilter

      return matchesSearch && matchesStatus
    })
  }, [searchQuery, statusFilter])

  const stats = {
    total: shipmentsData.length,
    inTransit: shipmentsData.filter(s => s.status === "in_transit").length,
    delivered: shipmentsData.filter(s => s.status === "delivered").length,
    delayed: shipmentsData.filter(s => s.status === "delayed").length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Shipment Tracking</h1>
        <p className="text-muted-foreground mt-1">Real-time tracking of all shipments</p>
      </div>

      {/* Search and Filter */}
      <Card className="p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search by ID, order, location, or carrier..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex gap-2">
            <Button
              variant={statusFilter === "all" ? "default" : "outline"}
              onClick={() => setStatusFilter("all")}
              size="sm"
            >
              All ({stats.total})
            </Button>
            <Button
              variant={statusFilter === "in_transit" ? "default" : "outline"}
              onClick={() => setStatusFilter("in_transit")}
              size="sm"
              className={statusFilter === "in_transit" ? "bg-blue-500" : ""}
            >
              In Transit ({stats.inTransit})
            </Button>
            <Button
              variant={statusFilter === "delivered" ? "default" : "outline"}
              onClick={() => setStatusFilter("delivered")}
              size="sm"
              className={statusFilter === "delivered" ? "bg-green-500" : ""}
            >
              Delivered ({stats.delivered})
            </Button>
            <Button
              variant={statusFilter === "delayed" ? "default" : "outline"}
              onClick={() => setStatusFilter("delayed")}
              size="sm"
              className={statusFilter === "delayed" ? "bg-red-500" : ""}
            >
              Delayed ({stats.delayed})
            </Button>
          </div>
        </div>
      </Card>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 border-2">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">Total Shipments</div>
              <div className="text-2xl font-bold mt-1">{stats.total}</div>
            </div>
            <Package className="w-8 h-8 text-primary" />
          </div>
        </Card>

        <Card className="p-4 border-2 bg-blue-500/5">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">In Transit</div>
              <div className="text-2xl font-bold mt-1">{stats.inTransit}</div>
            </div>
            <Truck className="w-8 h-8 text-blue-500" />
          </div>
        </Card>

        <Card className="p-4 border-2 bg-green-500/5">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">Delivered</div>
              <div className="text-2xl font-bold mt-1">{stats.delivered}</div>
            </div>
            <CheckCircle className="w-8 h-8 text-green-500" />
          </div>
        </Card>

        <Card className="p-4 border-2 bg-red-500/5">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-muted-foreground">Delayed</div>
              <div className="text-2xl font-bold mt-1">{stats.delayed}</div>
            </div>
            <AlertTriangle className="w-8 h-8 text-red-500" />
          </div>
        </Card>
      </div>

      {/* Shipments List */}
      <div className="space-y-4">
        {filteredShipments.length === 0 ? (
          <Card className="p-12 text-center">
            <Package className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Shipments Found</h3>
            <p className="text-muted-foreground">
              {searchQuery ? "Try adjusting your search query" : "No shipments match the selected filter"}
            </p>
          </Card>
        ) : (
          filteredShipments.map((shipment) => (
          <Card key={shipment.id} className="p-6 border-2 hover:shadow-lg transition-all">
            <div className="space-y-4">
              {/* Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                    {getStatusIcon(shipment.status)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-lg font-semibold">{shipment.id}</h3>
                      <Badge variant="outline" className="text-xs">
                        {shipment.order}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mt-0.5">
                      {shipment.carrier}
                    </p>
                  </div>
                </div>
                <Badge className={getStatusColor(shipment.status)} variant="outline">
                  {shipment.status.replace("_", " ").toUpperCase()}
                </Badge>
              </div>

              {/* Route */}
              <div className="flex items-center gap-2 text-sm">
                <MapPin className="w-4 h-4 text-primary" />
                <span className="font-medium">{shipment.origin}</span>
                <span className="text-muted-foreground">→</span>
                <span className="font-medium">{shipment.destination}</span>
              </div>

              {/* Progress Bar */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">{shipment.currentLocation}</span>
                  <span className="font-medium">{shipment.progress}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      shipment.status === "delivered"
                        ? "bg-green-500"
                        : shipment.status === "delayed"
                        ? "bg-red-500"
                        : "bg-blue-500"
                    }`}
                    style={{ width: `${shipment.progress}%` }}
                  />
                </div>
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-4 gap-4 pt-3 border-t">
                <div>
                  <div className="text-xs text-muted-foreground">ETA</div>
                  <div className="text-sm font-medium mt-1">{shipment.eta}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Items</div>
                  <div className="text-sm font-medium mt-1">{shipment.items} units</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Weight</div>
                  <div className="text-sm font-medium mt-1">{shipment.weight}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Last Update</div>
                  <div className="text-sm font-medium mt-1">{shipment.lastUpdate}</div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-2">
                <Button size="sm" variant="outline" className="text-xs">
                  View Details
                </Button>
                <Button size="sm" variant="outline" className="text-xs">
                  Track on Map
                </Button>
                {shipment.status === "delivered" && (
                  <Button size="sm" variant="outline" className="text-xs">
                    View POD
                  </Button>
                )}
              </div>
            </div>
          </Card>
        )))}
      </div>
    </div>
  )
}

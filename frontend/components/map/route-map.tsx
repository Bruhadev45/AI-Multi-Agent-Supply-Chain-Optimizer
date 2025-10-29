"use client"

import { useEffect, useRef, useState } from "react"
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from "react-leaflet"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

// Fix for default marker icons in Next.js
if (typeof window !== "undefined") {
  // remove cached icon retrieval to avoid broken icons on SSR/Next
  delete (L.Icon.Default.prototype as any)._getIconUrl
  L.Icon.Default.mergeOptions({
    iconRetinaUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
    iconUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
    shadowUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  })
}

interface RouteMapProps {
  origin?: { name: string; coordinates: [number, number] }
  destination?: { name: string; coordinates: [number, number] }
  routePath?: [number, number][]
  distance?: number
  duration?: string
  forceKey?: number | string
}

// Component to fit map bounds and ensure proper initialization
function MapBounds({ positions }: { positions: [number, number][] }) {
  const map = useMap()

  useEffect(() => {
    // Invalidate size to ensure proper rendering (small delay helps)
    const t = setTimeout(() => {
      try {
        map.invalidateSize()
      } catch (err) {
        // ignore
      }
    }, 100)

    if (positions.length > 0) {
      const bounds = L.latLngBounds(positions)
      try {
        map.fitBounds(bounds, { padding: [50, 50] })
      } catch (err) {
        // ignore
      }
    }

    return () => clearTimeout(t)
  }, [positions, map])

  return null
}

export function RouteMap({
  origin,
  destination,
  routePath,
  distance,
  duration,
  forceKey,
}: RouteMapProps) {
  const [mounted, setMounted] = useState(false)
  const wrapperRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    // small delay to avoid hydration / double-init problems in Next.js dev/StrictMode
    const timer = setTimeout(() => setMounted(true), 80)
    return () => {
      clearTimeout(timer)
      setMounted(false)
      // Cleanup Leaflet container to prevent "already initialized" errors
      try {
        const wrapper = wrapperRef.current
        if (wrapper) {
          // Find all leaflet containers and remove their IDs
          const containers = wrapper.querySelectorAll(".leaflet-container")
          containers.forEach((el: any) => {
            if (el._leaflet_id) {
              // Remove Leaflet's internal ID to allow re-initialization
              el._leaflet_id = undefined
            }
          })
        }
      } catch (err) {
        // ignore cleanup errors
      }
    }
  }, [])

  if (!mounted) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-muted rounded-lg">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-2" />
          <p className="text-muted-foreground text-sm">Loading map...</p>
        </div>
      </div>
    )
  }



  // Default to India center if no coordinates
  const defaultCenter: [number, number] = [20.5937, 78.9629]
  const defaultZoom = 5

  // Get positions for bounds
  const positions: [number, number][] = []
  if (origin) positions.push(origin.coordinates)
  if (destination) positions.push(destination.coordinates)

  // Use route path if available, otherwise draw straight line
  const linePositions = routePath || (origin && destination ? [origin.coordinates, destination.coordinates] : [])

  // Use forceKey if provided, otherwise generate stable key from coordinates
  const mapKey = forceKey
    ? `map-${forceKey}`
    : `map-${origin?.name || "o"}-${destination?.name || "d"}-${Date.now()}`

  try {
    return (
      <div className="w-full h-full rounded-lg overflow-hidden relative" ref={wrapperRef}>
        <MapContainer
          key={mapKey}
          center={positions.length > 0 ? positions[0] : defaultCenter}
          zoom={defaultZoom}
          style={{ height: "100%", width: "100%", minHeight: "400px" }}
          className="z-0"
          scrollWheelZoom={true}
          attributionControl={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            maxZoom={19}
            minZoom={3}
          />

          {/* Origin Marker */}
          {origin && (
            <Marker position={origin.coordinates}>
              <Popup>
                <div className="text-center p-2">
                  <strong className="text-primary">Origin</strong>
                  <br />
                  <span className="font-medium">{origin.name}</span>
                </div>
              </Popup>
            </Marker>
          )}

          {/* Destination Marker */}
          {destination && (
            <Marker position={destination.coordinates}>
              <Popup>
                <div className="text-center p-2">
                  <strong className="text-success">Destination</strong>
                  <br />
                  <span className="font-medium">{destination.name}</span>
                  {distance && (
                    <>
                      <br />
                      <span className="text-sm text-muted-foreground">
                        Distance: {distance.toFixed(0)} km
                      </span>
                    </>
                  )}
                  {duration && (
                    <>
                      <br />
                      <span className="text-sm text-muted-foreground">Duration: {duration}</span>
                    </>
                  )}
                </div>
              </Popup>
            </Marker>
          )}

          {/* Route Line */}
          {linePositions.length > 1 && (
            <Polyline positions={linePositions} color="#ef4444" weight={4} opacity={0.8} dashArray="10, 5" />
          )}

          {/* Fit bounds to show all markers */}
          {positions.length > 0 && <MapBounds positions={positions} />}
        </MapContainer>
      </div>
    )
  } catch (err) {
    console.error("Map rendering error:", err)
    return (
      <div className="w-full h-full flex items-center justify-center bg-muted rounded-lg">
        <div className="text-center">
          <p className="text-destructive font-medium">Failed to load map</p>
          <p className="text-muted-foreground text-sm mt-1">Please try refreshing the page</p>
        </div>
      </div>
    )
  }
}
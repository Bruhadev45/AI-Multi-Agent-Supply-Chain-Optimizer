"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Key, Moon, Lock, CheckCircle, XCircle, Server, Globe, Cloud, Database, ExternalLink } from "lucide-react"

interface SettingsProps {
  apiConnected: boolean | null
}

export function Settings({ apiConnected }: SettingsProps) {
  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground mt-1">Configure system preferences and API connections</p>
      </div>

      {/* System Status */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
          <Server className="w-5 h-5 text-primary" />
          System Status
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50">
            <div className="flex items-center gap-3">
              {apiConnected === true ? (
                <CheckCircle className="w-5 h-5 text-emerald-500" />
              ) : apiConnected === false ? (
                <XCircle className="w-5 h-5 text-red-500" />
              ) : (
                <div className="w-5 h-5 rounded-full border-2 border-muted-foreground animate-pulse" />
              )}
              <div>
                <p className="text-sm font-medium text-foreground">Backend API</p>
                <p className="text-xs text-muted-foreground">http://localhost:8000</p>
              </div>
            </div>
            <Badge variant="outline" className={apiConnected === true ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20" : "bg-red-500/10 text-red-600 border-red-500/20"}>
              {apiConnected === true ? "Online" : apiConnected === false ? "Offline" : "Checking..."}
            </Badge>
          </div>
          <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50">
            <div className="flex items-center gap-3">
              <Globe className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-sm font-medium text-foreground">Frontend App</p>
                <p className="text-xs text-muted-foreground">http://localhost:3000</p>
              </div>
            </div>
            <Badge variant="outline" className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20">Online</Badge>
          </div>
        </div>
      </Card>

      {/* API Keys */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-1 flex items-center gap-2">
          <Key className="w-5 h-5 text-primary" />
          API Configuration
        </h3>
        <p className="text-xs text-muted-foreground mb-4">Optional — all APIs degrade gracefully without keys</p>
        <div className="space-y-4">
          {[
            { label: "OpenAI API Key", placeholder: "sk-...", desc: "Enables CrewAI strategic reasoning", icon: Cloud },
            { label: "Google Maps API Key", placeholder: "AIza...", desc: "Enables real-time route data", icon: Globe },
            { label: "Weather API Key", placeholder: "Your key...", desc: "Enables live weather risk assessment", icon: Cloud },
          ].map((item) => (
            <div key={item.label} className="flex items-start gap-4 p-4 rounded-lg bg-muted/30 border border-border/50">
              <item.icon className="w-5 h-5 text-muted-foreground mt-0.5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <label className="block text-sm font-medium text-foreground">{item.label}</label>
                <p className="text-xs text-muted-foreground mb-2">{item.desc}</p>
                <input
                  type="password"
                  placeholder={item.placeholder}
                  className="w-full px-3 py-2 text-sm rounded-md border border-border bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
              </div>
            </div>
          ))}
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90 text-sm">
            Save Configuration
          </Button>
        </div>
      </Card>

      {/* Preferences */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
          <Moon className="w-5 h-5 text-primary" />
          Preferences
        </h3>
        <div className="space-y-1">
          {[
            { label: "Dark Mode", desc: "Use dark theme across the application", defaultOn: true },
            { label: "Email Notifications", desc: "Receive email alerts for completed analyses", defaultOn: true },
            { label: "Real-time Alerts", desc: "Show in-app notifications for system events", defaultOn: true },
            { label: "Auto-save Results", desc: "Automatically save analysis results to local storage", defaultOn: false },
          ].map((pref) => (
            <div key={pref.label} className="flex items-center justify-between py-3 px-1">
              <div>
                <p className="text-sm font-medium text-foreground">{pref.label}</p>
                <p className="text-xs text-muted-foreground">{pref.desc}</p>
              </div>
              <Switch defaultChecked={pref.defaultOn} />
            </div>
          ))}
        </div>
      </Card>

      {/* About */}
      <Card className="p-6 bg-card border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
          <Database className="w-5 h-5 text-primary" />
          About
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-muted-foreground">Version</p>
            <p className="font-medium text-foreground">2.0.0</p>
          </div>
          <div>
            <p className="text-muted-foreground">Framework</p>
            <p className="font-medium text-foreground">FastAPI + Next.js</p>
          </div>
          <div>
            <p className="text-muted-foreground">AI Agents</p>
            <p className="font-medium text-foreground">5 Specialized</p>
          </div>
          <div>
            <p className="text-muted-foreground">Cities</p>
            <p className="font-medium text-foreground">14 Indian</p>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-border">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary hover:underline flex items-center gap-1"
          >
            View API Documentation <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </Card>
    </div>
  )
}

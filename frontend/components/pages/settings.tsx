"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Key, Moon, Lock, CheckCircle, XCircle } from "lucide-react"

interface SettingsProps {
  apiConnected: boolean | null
}

export function Settings({ apiConnected }: SettingsProps) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground mt-1">Manage your account and preferences</p>
      </div>

      {/* API Connection Status */}
      <Card className="p-6 bg-card border border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {apiConnected === true ? (
              <CheckCircle className="w-5 h-5 text-green-500" />
            ) : apiConnected === false ? (
              <XCircle className="w-5 h-5 text-red-500" />
            ) : (
              <div className="w-5 h-5 rounded-full border-2 border-gray-400 animate-pulse" />
            )}
            <div>
              <h3 className="text-lg font-semibold text-foreground">Backend API Status</h3>
              <p className="text-sm text-muted-foreground">
                {apiConnected === true
                  ? "Connected to http://localhost:8000"
                  : apiConnected === false
                  ? "Disconnected - Make sure backend is running"
                  : "Checking connection..."}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div
              className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                apiConnected === true
                  ? "bg-green-500/10 text-green-500"
                  : apiConnected === false
                  ? "bg-red-500/10 text-red-500"
                  : "bg-gray-500/10 text-gray-500"
              }`}
            >
              {apiConnected === true ? "Online" : apiConnected === false ? "Offline" : "Unknown"}
            </div>
          </div>
        </div>
      </Card>

      {/* API Keys */}
      <Card className="p-6 bg-card border border-border">
        <div className="flex items-center gap-3 mb-4">
          <Key className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">API Keys</h3>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">OpenAI API Key</label>
            <input
              type="password"
              placeholder="sk-..."
              className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Google Maps API Key</label>
            <input
              type="password"
              placeholder="AIza..."
              className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Save API Keys</Button>
        </div>
      </Card>

      {/* Preferences */}
      <Card className="p-6 bg-card border border-border">
        <div className="flex items-center gap-3 mb-4">
          <Moon className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Preferences</h3>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-foreground">Dark Mode</label>
            <input type="checkbox" defaultChecked className="w-5 h-5" />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-foreground">Email Notifications</label>
            <input type="checkbox" defaultChecked className="w-5 h-5" />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-foreground">Real-time Alerts</label>
            <input type="checkbox" defaultChecked className="w-5 h-5" />
          </div>
        </div>
      </Card>

      {/* Security */}
      <Card className="p-6 bg-card border border-border">
        <div className="flex items-center gap-3 mb-4">
          <Lock className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Security</h3>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Current Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">New Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 rounded-lg border border-border bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Update Password</Button>
        </div>
      </Card>
    </div>
  )
}

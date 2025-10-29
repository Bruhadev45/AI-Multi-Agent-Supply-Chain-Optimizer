/**
 * API Client for AI Supply Chain Optimizer
 * Centralized service for all backend API calls
 */

// ==================== Configuration ====================

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ==================== Types ====================

export interface AnalysisRequest {
  origin: string;
  destination: string;
  scenario: string;
  orders_csv?: string;
}

export interface RouteInfo {
  path: string[];
  distance_km: number;
  duration: string;
  source: string;
  polyline?: string;
  route_quality?: string;
}

export interface RiskInfo {
  condition: string;
  temp?: string;
  humidity?: string;
  wind?: string;
  risk_level: string;
  source: string;
  additional_risk?: string;
}

export interface VendorData {
  vendor: string;
  total_cost: number;
  cost_per_km: number;
  emission_per_km: number;
  reliability_score: number;
  delivery_speed: string;
  service_quality: number;
  customer_rating?: number;
  composite_score: number;
  rank: number;
  headquarters_city?: string;
  established_year?: number;
  fleet_size?: number;
  geographic_coverage?: string;
  specialization?: string;
  fuel_type?: string;
  tracking_system?: string;
  emergency_support?: string;
  insurance_coverage?: number;
  certification?: string;
  payment_terms?: string;
  contact_phone?: string;
  contact_email?: string;
  max_capacity_kg?: number;
}

export interface SystemHealth {
  overall_health: string;
  success_rate?: string;
  avg_response_time?: string;
  api_status?: Record<string, boolean>;
}

export interface ExecutionMetadata {
  total_time_seconds: number;
  success_rates: {
    demand: boolean;
    route: boolean;
    cost: boolean;
    risk: boolean;
  };
  timestamp: string;
  execution_log: Array<{
    timestamp: string;
    step: string;
    status: string;
    duration_seconds: number;
    data_summary?: string;
  }>;
  api_availability: Record<string, boolean>;
  ai_execution_mode: string;
}

export interface RecommendationsConfidence {
  score: string;
  level: string;
  component_success: {
    demand_forecasting: boolean;
    route_optimization: boolean;
    cost_analysis: boolean;
    risk_assessment: boolean;
  };
}

export interface AnalysisResponse {
  forecast: number;
  forecast_original: number;
  scenario_applied: string;
  route_info: RouteInfo;
  best_vendor: string;
  best_price: number;
  original_price: number;
  all_vendors?: VendorData[];
  risk: RiskInfo;
  crew_reasoning: string;
  execution_metadata: ExecutionMetadata;
  system_health: SystemHealth;
  recommendations_confidence: RecommendationsConfidence;
}

export interface ScenarioConfig {
  demand_multiplier: number;
  cost_multiplier: number;
  risk_level: string;
}

export interface Scenario {
  id: string;
  name: string;
  config: ScenarioConfig;
}

export interface City {
  name: string;
  coordinates: [number, number];
}

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  version: string;
  orchestrator_initialized: boolean;
  api_status?: Record<string, boolean>;
}

export interface SystemStatusResponse {
  status: string;
  timestamp: string;
  system_health: SystemHealth;
  execution_log: Array<{
    timestamp: string;
    step: string;
    status: string;
    duration_seconds: number;
    data_summary?: string;
  }>;
  api_availability: Record<string, boolean>;
}

// ==================== Error Handling ====================

export class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// ==================== Helper Functions ====================

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      error: 'Unknown error',
      message: response.statusText
    }));

    throw new APIError(
      errorData.message || errorData.detail || 'API request failed',
      response.status,
      errorData
    );
  }

  return response.json();
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    return handleResponse<T>(response);
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }

    // Network or other errors
    throw new APIError(
      `Failed to connect to API: ${error instanceof Error ? error.message : 'Unknown error'}`,
      undefined,
      error
    );
  }
}

// ==================== API Client Methods ====================

export const apiClient = {
  /**
   * Check API health status
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    return apiRequest<HealthCheckResponse>('/health');
  },

  /**
   * Initialize the system
   */
  async initialize(): Promise<{ status: string; message: string; timestamp: string }> {
    return apiRequest('/api/initialize', { method: 'POST' });
  },

  /**
   * Run comprehensive supply chain analysis
   */
  async runAnalysis(request: AnalysisRequest): Promise<AnalysisResponse> {
    return apiRequest<AnalysisResponse>('/api/analyze', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Get available scenarios
   */
  async getScenarios(): Promise<{ scenarios: Scenario[] }> {
    return apiRequest<{ scenarios: Scenario[] }>('/api/scenarios');
  },

  /**
   * Get available cities
   */
  async getCities(): Promise<{ cities: City[] }> {
    return apiRequest<{ cities: City[] }>('/api/cities');
  },

  /**
   * Get system status
   */
  async getSystemStatus(): Promise<SystemStatusResponse> {
    return apiRequest<SystemStatusResponse>('/api/system/status');
  },

  /**
   * Reset the system
   */
  async resetSystem(): Promise<{ status: string; message: string; timestamp: string }> {
    return apiRequest('/api/system/reset', { method: 'POST' });
  },
};

// ==================== Hooks for React Components ====================

/**
 * Custom hook for API calls with loading and error states
 */
export function useAPI() {
  return {
    ...apiClient,
    // You can add additional helper methods here if needed
  };
}

// ==================== Utility Functions ====================

/**
 * Format API error for display
 */
export function formatAPIError(error: unknown): string {
  if (error instanceof APIError) {
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
}

/**
 * Check if API is available
 */
export async function isAPIAvailable(): Promise<boolean> {
  try {
    await apiClient.healthCheck();
    return true;
  } catch {
    return false;
  }
}

export default apiClient;

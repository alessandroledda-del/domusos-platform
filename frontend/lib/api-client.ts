import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios'

import { useAuthStore, type AuthUser } from '@/store/authStore'

interface AuthResponse {
  access: string
  refresh?: string
}

class ApiClient {
  private client: AxiosInstance
  private baseURL: string

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api') {
    this.baseURL = baseURL
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.client.interceptors.request.use((config: InternalAxiosRequestConfig) => {
      const token = useAuthStore.getState().accessToken
      if (token) {
        config.headers.Authorization = ['Bearer', token].join(' ')
      }
      return config
    })

    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

        if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
          originalRequest._retry = true
          const { refreshToken, setTokens, clearAuth } = useAuthStore.getState()
          if (refreshToken) {
            try {
              const response = await axios.post<AuthResponse>(`${this.baseURL}/token/refresh/`, {
                refresh: refreshToken,
              })
              setTokens(response.data.access, response.data.refresh ?? refreshToken)
              originalRequest.headers.Authorization = ['Bearer', response.data.access].join(' ')
              return this.client(originalRequest)
            } catch {
              clearAuth()
              if (typeof window !== 'undefined') {
                window.location.href = '/login'
              }
            }
          }
        }

        return Promise.reject(error)
      },
    )
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/token/', { email, password })
    return response.data
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/token/refresh/', { refresh: refreshToken })
    return response.data
  }

  async getCurrentUser(): Promise<AuthUser> {
    const response = await this.client.get<AuthUser>('/users/me/')
    return response.data
  }

  async getUsers(page: number = 1) {
    const response = await this.client.get('/users/', { params: { page } })
    return response.data
  }

  async getUserById(id: number): Promise<AuthUser> {
    const response = await this.client.get<AuthUser>(`/users/${id}/`)
    return response.data
  }

  async createUser(userData: Partial<AuthUser> & { password: string }) {
    const response = await this.client.post('/users/', userData)
    return response.data
  }

  async updateUser(id: number, userData: Partial<AuthUser>) {
    const response = await this.client.put(`/users/${id}/`, userData)
    return response.data
  }

  async deleteUser(id: number) {
    await this.client.delete(`/users/${id}/`)
  }

  async setPassword(id: number, password: string) {
    const response = await this.client.post(`/users/${id}/set_password/`, { password })
    return response.data
  }

  async getCompanies(page: number = 1) {
    const response = await this.client.get('/companies/', { params: { page } })
    return response.data
  }

  async getCompanyById(id: number) {
    const response = await this.client.get(`/companies/${id}/`)
    return response.data
  }

  async createCompany(companyData: Record<string, unknown>) {
    const response = await this.client.post('/companies/', companyData)
    return response.data
  }

  async updateCompany(id: number, companyData: Record<string, unknown>) {
    const response = await this.client.put(`/companies/${id}/`, companyData)
    return response.data
  }

  async deleteCompany(id: number) {
    await this.client.delete(`/companies/${id}/`)
  }

  async getCompanyProperties(id: number) {
    const response = await this.client.get(`/companies/${id}/properties/`)
    return response.data
  }

  async getProperties(page: number = 1, companyId?: number) {
    const params: Record<string, number> = { page }
    if (companyId) {
      params.company_id = companyId
    }
    const response = await this.client.get('/properties/', { params })
    return response.data
  }

  async getPropertyById(id: number) {
    const response = await this.client.get(`/properties/${id}/`)
    return response.data
  }

  async createProperty(propertyData: Record<string, unknown>) {
    const response = await this.client.post('/properties/', propertyData)
    return response.data
  }

  async updateProperty(id: number, propertyData: Record<string, unknown>) {
    const response = await this.client.put(`/properties/${id}/`, propertyData)
    return response.data
  }

  async deleteProperty(id: number) {
    await this.client.delete(`/properties/${id}/`)
  }

  async updatePropertyScore(id: number, domusScore: number) {
    const response = await this.client.post(`/properties/${id}/update_score/`, { domus_score: domusScore })
    return response.data
  }

  async updatePropertyStatus(id: number, status: string) {
    const response = await this.client.post(`/properties/${id}/update_status/`, { status })
    return response.data
  }

  async getPropertiesByCompany(companyId: number) {
    const response = await this.client.get('/properties/by_company/', { params: { company_id: companyId } })
    return response.data
  }
}

export const apiClient = new ApiClient()
export type { AuthResponse, AuthUser as User }

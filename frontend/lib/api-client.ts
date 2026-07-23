import axios, { AxiosError, AxiosInstance } from 'axios';

interface AuthResponse {
  access: string;
  refresh: string;
}

interface ApiErrorPayload {
  code?: string;
  message?: string;
  details?: unknown;
  trace_id?: string;
  detail?: string;
}

interface User {
  id: number;
  email: string;
  nome: string;
  cognome: string;
  telefono: string;
  ruolo: string;
  stato: string;
}

export function getApiErrorMessage(error: unknown, fallback: string): string {
  if (!axios.isAxiosError(error)) {
    return fallback;
  }

  const data = error.response?.data as ApiErrorPayload | undefined;
  return data?.message || data?.detail || fallback;
}

class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config;

        if (
          error.response?.status === 401 &&
          originalRequest &&
          !originalRequest.url?.includes('/token/refresh/')
        ) {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await axios.post(`${this.baseURL}/token/refresh/`, {
                refresh: refreshToken,
              });

              localStorage.setItem('access_token', response.data.access);
              originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
              return this.client(originalRequest);
            } catch {
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              window.location.href = '/login';
            }
          }
        }

        return Promise.reject(error);
      }
    );
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post('/token/', { email, password });
    return response.data;
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    const response = await this.client.post('/token/refresh/', { refresh: refreshToken });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get('/users/me/');
    return response.data;
  }

  async getUsers(page: number = 1) {
    const response = await this.client.get('/users/', { params: { page } });
    return response.data;
  }

  async getUserById(id: number): Promise<User> {
    const response = await this.client.get(`/users/${id}/`);
    return response.data;
  }

  async createUser(userData: Partial<User> & { password: string }) {
    const response = await this.client.post('/users/', userData);
    return response.data;
  }

  async updateUser(id: number, userData: Partial<User>) {
    const response = await this.client.put(`/users/${id}/`, userData);
    return response.data;
  }

  async deleteUser(id: number) {
    await this.client.delete(`/users/${id}/`);
  }

  async setPassword(id: number, password: string) {
    const response = await this.client.post(`/users/${id}/set_password/`, { password });
    return response.data;
  }

  async getCompanies(page: number = 1) {
    const response = await this.client.get('/companies/', { params: { page } });
    return response.data;
  }

  async getCompanyById(id: number) {
    const response = await this.client.get(`/companies/${id}/`);
    return response.data;
  }

  async createCompany(companyData: Record<string, unknown>) {
    const response = await this.client.post('/companies/', companyData);
    return response.data;
  }

  async updateCompany(id: number, companyData: Record<string, unknown>) {
    const response = await this.client.put(`/companies/${id}/`, companyData);
    return response.data;
  }

  async deleteCompany(id: number) {
    await this.client.delete(`/companies/${id}/`);
  }

  async getCompanyProperties(id: number) {
    const response = await this.client.get(`/companies/${id}/properties/`);
    return response.data;
  }

  async getProperties(page: number = 1, companyId?: number) {
    const params: Record<string, number> = { page };
    if (companyId) {
      params.company_id = companyId;
    }
    const response = await this.client.get('/properties/', { params });
    return response.data;
  }

  async getPropertyById(id: number) {
    const response = await this.client.get(`/properties/${id}/`);
    return response.data;
  }

  async createProperty(propertyData: Record<string, unknown>) {
    const response = await this.client.post('/properties/', propertyData);
    return response.data;
  }

  async updateProperty(id: number, propertyData: Record<string, unknown>) {
    const response = await this.client.put(`/properties/${id}/`, propertyData);
    return response.data;
  }

  async deleteProperty(id: number) {
    await this.client.delete(`/properties/${id}/`);
  }

  async updatePropertyScore(id: number, domusScore: number) {
    const response = await this.client.post(`/properties/${id}/update_score/`, { domus_score: domusScore });
    return response.data;
  }

  async updatePropertyStatus(id: number, status: string) {
    const response = await this.client.post(`/properties/${id}/update_status/`, { status });
    return response.data;
  }

  async getPropertiesByCompany(companyId: number) {
    const response = await this.client.get('/properties/by_company/', { params: { company_id: companyId } });
    return response.data;
  }
}

export const apiClient = new ApiClient();
export type { AuthResponse, User };
